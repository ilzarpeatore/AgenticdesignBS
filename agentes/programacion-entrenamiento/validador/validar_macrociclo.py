#!/usr/bin/env python3
"""Validador determinista de PROGRESIÓN de un macrociclo (varios mesociclos seguidos del mismo cliente).

Complementa a `validar_programa.py` (Paso 3, comprueba UN `.xlsx` de UN mesociclo contra el formato) con lo
que ese validador no puede ver por diseño: si el conjunto de mesociclos de un macrociclo realmente PROGRESA
de uno al siguiente. Ver `modulos/biomecanica-programacion-hipertrofia.md` sección 9bis para la regla completa
y el caso real que expuso el hueco -- un macrociclo puede tener estructura y onda intra-mesociclo perfectas
(lo que ya comprueba `validar_programa.py`) y aun así tener el volumen semanal total plano o decreciente mes a
mes, o el mismo rango de reps las 4-6 semanas de cada mesociclo. Nada mecánico lo detectaba antes de este script.

Uso:
    python3 validar_macrociclo.py <carpeta-o-archivos.xlsx> \
        [--agrupar-hombro] \
        [--patron-seguro REGEX --reps-min-seguro N --rir-min-seguro N] \
        [--texto]

Los archivos se procesan **en el orden dado** (orden alfabético del glob, o el orden literal de la lista si
se pasan archivos sueltos) -- ese orden se trata como el orden real de los mesociclos del macrociclo. Si el
`titulo`/`descripcion` de la hoja "Programa" de un archivo contiene "Mesociclo N" o "M<N>", se usa como
verificación cruzada (advertencia si no coincide con la posición), nunca como única fuente de verdad -- este
repo no impone ninguna convención de nombres de título a los clientes.

Salida: informe JSON por stdout con `aprobado`, `errores`, `advertencias` (mismo contrato que
`validar_programa.py`) y un campo adicional `tablas` con el detalle legible por humano de cada regla --
pásalo por `--texto` para imprimir solo ese detalle en texto plano en vez de JSON, si lo vas a enseñar
directamente al coach. Código de salida 0 si aprobado, 1 si no.

Usa `lectura_programa.py` (el lector compartido, extraído en v0.7.0) para abrir cada `.xlsx` -- así este
validador interpreta el formato de columnas exactamente igual que `validar_programa.py` y `control-producto`,
en vez de parsearlo por su cuenta y divergir con el tiempo si el formato cambia.
"""

from __future__ import annotations

import argparse
import glob
import io
import json
import os
import re
import sys
import unicodedata
from collections import defaultdict
from dataclasses import dataclass, field

import openpyxl

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lectura_programa import HOJA_PROGRAMA, HOJA_PROGRAMACION, LecturaProgramaError, leer_programa  # noqa: E402

# En consolas Windows sin codepage UTF-8, stdout por defecto no es utf-8 y json.dumps(ensure_ascii=False) con
# tildes/ñ rompe al redirigir a archivo o pipe -- fuerza UTF-8 explícitamente, no asumas el entorno.
if (sys.stdout.encoding or "").lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# Grupos de estabilidad/prehab: no se les exige subida ESTRICTA mesociclo a mesociclo (V1), solo no-decreciente
# -- su progresión es de resistencia y control, no de acumulación de volumen (ver progresion-carga.md).
GRUPOS_ESTABILIDAD = {"Manguito y escápula", "Cuello y escápula", "Cardio"}
GRUPOS_HOMBRO = {"Deltoide lateral", "Deltoide posterior", "Hombros (press)", "Manguito y escápula"}

# Patrones de ejercicio que se consideran de rango FIJO por diseño (no se les exige V3: cambiar de rango de
# reps semana a semana) -- prehab de hombro/cuello, core, gemelo, cardio y movilidad. Amplía este patrón si el
# catálogo de un cliente concreto tiene otros ejercicios de rango fijo por diseño (isométricos, por tiempo...).
RANGO_FIJO = re.compile(
    r"movilidad|isom[eé]tric|y-t-w|flexiones|el[ií]ptica|\bcorrer\b|cinta|rotaci[oó]n (externa|interna)|"
    r"face pull|gemelo|pantorrilla|talones|crunch|pallof|abdom|plancha|piernas colgado",
    re.I,
)


def _normalizar(texto: str | None) -> str:
    if not texto:
        return ""
    sin_acentos = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return re.sub(r"\s+", " ", sin_acentos).strip().lower()


def grupo_muscular(nombre: str) -> str:
    """Clasifica un nombre de ejercicio en español (convención del catálogo real de BeFit/Bckbs) por grupo
    muscular principal. Es heurística por nombre, no un campo estructurado del catálogo -- si un ejercicio
    legítimo cae en "Otros" (que no se comprueba en V1/V2b, así que nunca hace fallar el validador por error,
    pero tampoco se beneficia de la regla), amplía las listas de abajo; no es un fallo del programa, es un
    hueco de esta función. Ver el caso real de "Trituradora de cráneos" (tríceps) y "Encogimientos" (espalda)
    en `CHANGELOG.md` v0.24.0."""
    n = _normalizar(nombre)
    if "pallof" in n:
        return "Core"
    if "movilidad" in n or ("isom" in n and "cervical" in n):
        return "Cuello y escápula"
    if "y-t-w" in n or "flexiones" in n:
        return "Manguito y escápula"
    if "eliptica" in n or n.strip() == "correr" or "cinta" in n:
        return "Cardio"
    if "fondos (dips) en maquina" in n:
        return "Triceps"
    if ("face pull" in n or "trasera" in n or "trasero" in n or "pajaros" in n
            or "deltoides posterior" in n or "deltoide posterior" in n):
        return "Deltoide posterior"
    if "rotacion externa" in n or "rotacion interna" in n:
        return "Manguito y escápula"
    if "elevacion lateral" in n:
        return "Deltoide lateral"
    if "press de hombro" in n or "press militar" in n or "press arnold" in n:
        return "Hombros (press)"
    if ("press de pecho" in n or "pec deck" in n or "apertura" in n or "press banca" in n
            or "press de banca" in n or "press inclinado" in n or "fondos" in n or "cruce de poleas" in n):
        return "Pecho"
    if "jalon" in n or "lat pulldown" in n or "remo" in n or "dominada" in n or "encogimiento" in n:
        return "Espalda"
    if "triceps" in n or "press frances" in n or "skull" in n or "trituradora" in n:
        return "Triceps"
    if "leg curl" in n or "curl femoral" in n or "curl de piernas" in n or "isquiotibial" in n or "peso muerto" in n:
        return "Isquios"
    if "curl" in n:
        return "Biceps"
    if "bulgara" in n or "hip thrust" in n or "abduccion" in n or "aduccion" in n or "hiperextension" in n or "gluteo" in n:
        return "Glúteo y cadera"
    if "gemelo" in n or "pantorrilla" in n or "talones" in n:
        return "Gemelos"
    if "prensa" in n or "hack" in n or "sentadilla" in n or "cuadriceps" in n or "zancada" in n:
        return "Cuádriceps"
    if "crunch" in n or "plancha" in n or "abdominal" in n or "elevacion de piernas" in n:
        return "Core"
    return "Otros"


def _rango_reps(reps) -> tuple[int, int] | None:
    """'8-10' -> (8, 10); '12' -> (12, 12); None si no es un rango/valor numérico (ejercicio por tiempo, etc.)."""
    m = re.match(r"^\s*(\d+)\s*(?:-\s*(\d+))?\s*$", str(reps or ""))
    if not m:
        return None
    lo = int(m.group(1))
    return lo, int(m.group(2) or lo)


def _rir_minimo(valor) -> float | None:
    m = re.match(r"^\s*([\d.]+)", str(valor or ""))
    return float(m.group(1)) if m else None


@dataclass
class InformeMacrociclo:
    errores: list[str] = field(default_factory=list)
    advertencias: list[str] = field(default_factory=list)
    tablas: list[str] = field(default_factory=list)

    @property
    def aprobado(self) -> bool:
        return not self.errores

    def to_dict(self) -> dict:
        return {"aprobado": self.aprobado, "errores": self.errores, "advertencias": self.advertencias, "tablas": self.tablas}


def _titulo_y_descripcion(ruta: str) -> tuple[str, str]:
    """Lee solo la fila 2 de la hoja 'Programa' (titulo/descripcion) -- `lectura_programa.leer_programa` no
    los expone (no los necesita para su propio contrato), así que este validador los lee aparte, únicamente
    para la advertencia de cruce "Mesociclo N" del título."""
    wb = openpyxl.load_workbook(ruta, data_only=True, read_only=True)
    try:
        if HOJA_PROGRAMA not in wb.sheetnames:
            return "", ""
        ws = wb[HOJA_PROGRAMA]
        cab = [c.value for c in next(ws.iter_rows(min_row=1, max_row=1))]
        fila = [c.value for c in next(ws.iter_rows(min_row=2, max_row=2))] if ws.max_row >= 2 else []
        titulo = fila[cab.index("titulo")] if "titulo" in cab and cab.index("titulo") < len(fila) else ""
        descripcion = fila[cab.index("descripcion")] if "descripcion" in cab and cab.index("descripcion") < len(fila) else ""
        return str(titulo or ""), str(descripcion or "")
    finally:
        wb.close()


def _cargar_mesociclos(paths: list[str], informe: InformeMacrociclo) -> list[dict]:
    """Devuelve una lista de mesociclos EN EL ORDEN DE LOS ARCHIVOS (ver docstring del módulo), cada uno con
    sus filas de 'Programación' ya parseadas vía `lectura_programa.leer_programa` (mismo lector que
    `validar_programa.py` y `control-producto`). No descarta un archivo por no encontrar 'Mesociclo N' en el
    título -- eso solo se usa como advertencia de cruce, nunca como filtro.

    Un `.xlsx` sin las hojas `Programa`/`Programación` se omite en silencio (no es un mesociclo -- p. ej. el
    Excel de revisión `formato-excel-detallado.md` suele vivir en la misma carpeta que los de importación).
    Uno que SÍ tiene esas hojas pero está mal formado por dentro (falta una columna obligatoria, sin filas de
    datos) sí se registra como error real en `informe` y se omite del resto de reglas -- eso no es "otro tipo
    de archivo", es un mesociclo roto."""
    files: list[str] = []
    for p in paths:
        if os.path.isdir(p):
            files += sorted(f for f in glob.glob(os.path.join(p, "*.xlsx")) if not os.path.basename(f).startswith("~$"))
        elif not os.path.basename(p).startswith("~$"):
            files.append(p)

    mesociclos = []
    for orden, f in enumerate(files, start=1):
        wb_check = openpyxl.load_workbook(f, read_only=True)
        try:
            tiene_hojas = HOJA_PROGRAMA in wb_check.sheetnames and HOJA_PROGRAMACION in wb_check.sheetnames
        finally:
            wb_check.close()
        if not tiene_hojas:
            continue

        try:
            lectura = leer_programa(f)
        except LecturaProgramaError as e:
            informe.errores.append(f"{os.path.basename(f)}: {'; '.join(e.errores)}")
            continue

        titulo, descripcion = _titulo_y_descripcion(f)
        m = re.search(r"mesociclo\s*(\d+)|\bM(\d+)\b", f"{titulo} {descripcion}", re.I)
        numero_declarado = int(m.group(1) or m.group(2)) if m else None

        filas = []
        for r in lectura.filas:
            semana, ejercicio = lectura.val(r, "semana"), lectura.val(r, "ejercicio")
            if semana is None or ejercicio is None:
                continue
            filas.append(dict(semana=int(semana), dia=int(lectura.val(r, "dia")), ejercicio=str(ejercicio),
                               series=int(lectura.val(r, "series") or 0), reps=lectura.val(r, "reps"), rir=lectura.val(r, "rir")))
        mesociclos.append(dict(archivo=f, orden=orden, numero_declarado=numero_declarado, titulo=titulo, filas=filas))
    return mesociclos


def validar_macrociclo(
    paths: list[str],
    agrupar_hombro: bool = False,
    patron_seguro: str | None = None,
    reps_min_seguro: int | None = None,
    rir_min_seguro: float | None = None,
) -> InformeMacrociclo:
    informe = InformeMacrociclo()
    mesos = _cargar_mesociclos(paths, informe)
    if len(mesos) < 2:
        informe.advertencias.append(
            f"Solo se encontraron {len(mesos)} mesociclo(s) con hojas 'Programa'/'Programación' válidas -- "
            "este validador compara progresión ENTRE mesociclos, con menos de 2 no hay nada que comparar "
            "(no es un error: puede que el resto del macrociclo todavía no se haya generado)."
        )
        return informe

    for m in mesos:
        if m["numero_declarado"] is not None and m["numero_declarado"] != m["orden"]:
            informe.advertencias.append(
                f"{m['archivo']}: el título/descripción sugiere mesociclo {m['numero_declarado']}, pero por "
                f"orden de archivo ocupa la posición {m['orden']} -- comprueba que los archivos estén en el "
                "orden real del macrociclo (o que el título esté equivocado)."
            )

    orden = [m["orden"] for m in mesos]
    etiqueta = {m["orden"]: os.path.basename(m["archivo"]) for m in mesos}

    def es_ultima_semana(m: dict, semana: int) -> bool:
        return semana == max(f["semana"] for f in m["filas"])

    # ---- V1: volumen entre mesociclos (semana 1 por grupo) y V2b: el pico semanal tampoco retrocede
    def grupo_de(nombre: str) -> str:
        g = grupo_muscular(nombre)
        if agrupar_hombro and g in GRUPOS_HOMBRO and g != "Manguito y escápula":
            return "Hombros"
        return g

    sem1: dict[int, dict[str, int]] = {m["orden"]: defaultdict(int) for m in mesos}
    pico: dict[int, dict[str, int]] = {m["orden"]: defaultdict(int) for m in mesos}
    for m in mesos:
        por_semana_grupo: dict[int, dict[str, int]] = defaultdict(lambda: defaultdict(int))
        for r in m["filas"]:
            g = grupo_de(r["ejercicio"])
            if r["semana"] == 1:
                sem1[m["orden"]][g] += r["series"]
            if not es_ultima_semana(m, r["semana"]):
                por_semana_grupo[r["semana"]][g] += r["series"]
        for g in {gg for pg in por_semana_grupo.values() for gg in pg}:
            pico[m["orden"]][g] = max(pg.get(g, 0) for pg in por_semana_grupo.values())

    grupos = sorted({g for m in orden for g in sem1[m]} | {g for m in orden for g in pico[m]})

    tabla_v1 = ["== V1 · series semanales por grupo (semana 1), mesociclo a mesociclo =="]
    for g in grupos:
        vals = [sem1[m].get(g, 0) for m in orden]
        no_decrece = all(b >= a for a, b in zip(vals, vals[1:]))
        if g in GRUPOS_ESTABILIDAD:
            ok = no_decrece
        elif len(vals) >= 3:
            # el último mesociclo puede quedarse en meseta (consolidación) SOLO si antes hubo subida estricta
            # real en todos los pasos previos -- con menos de 3 mesociclos no hay "antes" que lo justifique.
            hasta_penultimo = vals[:-1]
            estricto = all(b > a for a, b in zip(hasta_penultimo, hasta_penultimo[1:]))
            ok = estricto and vals[-1] >= vals[-2]
        else:
            ok = all(b > a for a, b in zip(vals, vals[1:]))
        tabla_v1.append(f"  {g}: {vals} -- {'ok' if ok else 'FALLA (plano o decreciente)'}")
        if not ok:
            informe.errores.append(f"V1 {g}: series de la semana 1 no suben de forma consistente entre mesociclos ({vals}).")
    informe.tablas.append("\n".join(tabla_v1))

    tabla_v2b = ["== V2b · pico semanal por grupo (excluida la descarga), mesociclo a mesociclo =="]
    for g in grupos:
        vals = [pico[m].get(g, 0) for m in orden]
        ok = all(b >= a for a, b in zip(vals, vals[1:]))
        tabla_v2b.append(f"  {g}: {vals} -- {'ok' if ok else 'FALLA (el pico retrocede)'}")
        if not ok:
            informe.errores.append(
                f"V2b {g}: el pico semanal retrocede de un mesociclo al siguiente aunque la base (V1) puede estar "
                f"subiendo ({vals}) -- revisa que la regla de onda se aplique igual en todos los mesociclos "
                "(ver biomecanica-programacion-hipertrofia.md sección 9bis)."
            )
    informe.tablas.append("\n".join(tabla_v2b))

    # ---- V2: onda y descarga dentro de cada mesociclo (ya cubierto en espíritu por progresion-carga.md,
    # se repite aquí porque valida el AGREGADO semanal, no ejercicio a ejercicio)
    tabla_v2 = ["== V2 · series totales por semana dentro de cada mesociclo =="]
    for m in mesos:
        por_sem = defaultdict(int)
        for r in m["filas"]:
            por_sem[r["semana"]] += r["series"]
        semanas = sorted(por_sem)
        vals = [por_sem[s] for s in semanas]
        cima = max(vals)
        idx_cima = vals.index(cima)
        ok = cima > vals[0] and vals[-1] < 0.8 * cima and idx_cima < len(semanas) - 1
        tabla_v2.append(f"  {etiqueta[m['orden']]}: {vals} -- {'ok' if ok else 'FALLA (sin pico claro o sin descarga real al final)'}")
        if not ok:
            informe.errores.append(f"V2 {etiqueta[m['orden']]}: la semana final no es una descarga real por debajo del 80% del pico ({vals}).")
    informe.tablas.append("\n".join(tabla_v2))

    # ---- V3: las reps cambian de rango semana a semana dentro de cada mesociclo, en ambos sentidos por sesión
    tabla_v3 = ["== V3 · evolución de reps dentro de cada mesociclo (primera semana de carga -> última antes del deload) =="]
    for m in mesos:
        semanas_de_carga = sorted({r["semana"] for r in m["filas"] if not es_ultima_semana(m, r["semana"])})
        if len(semanas_de_carga) < 2:
            tabla_v3.append(f"  {etiqueta[m['orden']]}: solo {len(semanas_de_carga)} semana(s) de carga, nada que comparar.")
            continue
        s_ini, s_fin = semanas_de_carga[0], semanas_de_carga[-1]
        por_ej: dict[tuple[int, str], dict[int, tuple[int, int] | None]] = defaultdict(dict)
        for r in m["filas"]:
            por_ej[(r["dia"], r["ejercicio"])][r["semana"]] = _rango_reps(r["reps"])
        progresion = [(k, v) for k, v in por_ej.items() if not RANGO_FIJO.search(k[1]) and v.get(s_ini) and v.get(s_fin)]
        cambian = [(k, v[s_ini], v[s_fin]) for k, v in progresion if v[s_ini][0] != v[s_fin][0]]
        suben = [c for c in cambian if c[2][0] > c[1][0]]
        bajan = [c for c in cambian if c[2][0] < c[1][0]]
        pct = 100 * len(cambian) / max(1, len(progresion))
        ok = pct >= 80
        tabla_v3.append(
            f"  {etiqueta[m['orden']]}: {len(cambian)}/{len(progresion)} ejercicios cambian de rango ({pct:.0f}%) "
            f"-- suben {len(suben)} / bajan {len(bajan)} -- {'ok' if ok else 'FALLA'}"
        )
        if not ok:
            informe.errores.append(
                f"V3 {etiqueta[m['orden']]}: solo {len(cambian)}/{len(progresion)} ejercicios de progresión cambian "
                "de rango de reps entre semanas de carga (mínimo esperado 80%)."
            )
        for dia in sorted({k[0] for k, _ in progresion}):
            s_dia = [c for c in suben if c[0][0] == dia]
            b_dia = [c for c in bajan if c[0][0] == dia]
            if not s_dia or not b_dia:
                tabla_v3.append(f"      día {dia}: sube {len(s_dia)} / baja {len(b_dia)} -- FALLA (falta uno de los dos sentidos en la sesión)")
                informe.errores.append(f"V3 {etiqueta[m['orden']]} día {dia}: la sesión no tiene ejercicios en los dos sentidos (sube {len(s_dia)}, baja {len(b_dia)}).")
    informe.tablas.append("\n".join(tabla_v3))

    # ---- V4 (opcional): mínimos de seguridad para un patrón de ejercicio marcado por el cliente
    if patron_seguro:
        patron = re.compile(patron_seguro, re.I)
        tabla_v4 = [f"== V4 · mínimos de seguridad para /{patron_seguro}/ (reps >= {reps_min_seguro}, RIR >= {rir_min_seguro}) =="]
        malos = 0
        for m in mesos:
            ultima = max(r["semana"] for r in m["filas"])
            for r in m["filas"]:
                if r["semana"] >= ultima or not patron.search(r["ejercicio"]):
                    continue
                rg, rr = _rango_reps(r["reps"]), _rir_minimo(r["rir"])
                viola_reps = reps_min_seguro is not None and rg and rg[0] < reps_min_seguro
                viola_rir = rir_min_seguro is not None and rr is not None and rr < rir_min_seguro
                if viola_reps or viola_rir:
                    malos += 1
                    tabla_v4.append(f"  {etiqueta[m['orden']]} S{r['semana']} {r['ejercicio']}: reps {r['reps']} RIR {r['rir']}")
        tabla_v4.append("ok" if malos == 0 else f"FALLA ({malos} filas por debajo del mínimo)")
        informe.tablas.append("\n".join(tabla_v4))
        if malos:
            informe.errores.append(f"V4: {malos} filas de ejercicios que matchean /{patron_seguro}/ están por debajo del mínimo de seguridad.")

    return informe


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("rutas", nargs="+", help="Carpeta con los .xlsx de los mesociclos, o los archivos sueltos en orden.")
    parser.add_argument("--agrupar-hombro", action="store_true",
                         help="Agrupa deltoide lateral/posterior y press de hombro en un único grupo 'Hombros' (como hace el catálogo real de BeFit).")
    parser.add_argument("--patron-seguro", default=None, help="Regex de ejercicios sujetos al mínimo de seguridad V4 (p. ej. una restricción de este cliente).")
    parser.add_argument("--reps-min-seguro", type=int, default=None)
    parser.add_argument("--rir-min-seguro", type=float, default=None)
    parser.add_argument("--texto", action="store_true", help="Imprime solo las tablas en texto plano (para enseñar al coach) en vez del JSON completo.")
    args = parser.parse_args()

    informe = validar_macrociclo(
        args.rutas,
        agrupar_hombro=args.agrupar_hombro,
        patron_seguro=args.patron_seguro,
        reps_min_seguro=args.reps_min_seguro,
        rir_min_seguro=args.rir_min_seguro,
    )
    if args.texto:
        print("\n\n".join(informe.tablas))
        print()
        print("RESULTADO: OK -- progresión conforme" if informe.aprobado else f"RESULTADO: NO CUMPLE ({len(informe.errores)} fallos)")
    else:
        print(json.dumps(informe.to_dict(), ensure_ascii=False, indent=2))
    return 0 if informe.aprobado else 1


if __name__ == "__main__":
    sys.exit(main())
