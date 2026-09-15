"""Validador determinista (Paso 3) del Asistente de Programación de Nutrición.

Comprueba mecánicamente, contra un JSON que representa el plan que el
Productor va a enviar a la API real de Bckbs (`meal_plan_templates` +
`meal_plan_template_items`, ver `formato-salida/entrega-bckbs.md`), todo lo
que NO requiere juicio — igual que `validador/validar_programa.py` del
Asistente de Programación de Entrenamiento hace con el `.xlsx`.

El JSON de entrada no es un formato que Bckbs reciba tal cual — es la
representación interna que el Productor construye ANTES de llamar a
`POST meal-plan-templates` / `.../items`, enriquecida con los campos que
este validador necesita y la API no (`ingredientes` por item, para el
cribado de alérgenos; `restricciones_dieteticas` y `objetivo_diario` del
cliente). Ver `tests/fixtures/` para un ejemplo completo.

Uso:
    python3 validar_plan.py <plan.json> [--tolerancia 0.10]

Salida: informe JSON por stdout con `aprobado`, `errores` y
`advertencias`, y código de salida 0 si aprobado, 1 si no.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from collections import defaultdict
from dataclasses import dataclass, field

TIPOS_EXCLUSION_DURA = {"alergia", "intolerancia"}
MEAL_TYPES_VALIDOS = {"breakfast", "lunch", "dinner", "snacks"}
WEEKDAYS_VALIDOS = {"monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"}
MACROS = ["calories", "protein", "fats", "carbs"]


@dataclass
class InformeValidacion:
    errores: list[str] = field(default_factory=list)
    advertencias: list[str] = field(default_factory=list)

    @property
    def aprobado(self) -> bool:
        return not self.errores

    def to_dict(self) -> dict:
        return {
            "aprobado": self.aprobado,
            "errores": self.errores,
            "advertencias": self.advertencias,
        }


def _normalizar(texto: str | None) -> str:
    if not texto:
        return ""
    sin_acentos = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return re.sub(r"\s+", " ", sin_acentos).strip().lower()


def _celda_vacia(valor) -> bool:
    return valor is None or (isinstance(valor, str) and valor.strip() == "")


def validar_plan(
    plan: dict,
    tolerancia: float = 0.10,
) -> InformeValidacion:
    informe = InformeValidacion()

    template = plan.get("template") or {}
    items = plan.get("items") or []
    restricciones = plan.get("restricciones_dieteticas") or []
    objetivo_diario = plan.get("objetivo_diario")

    # 1. Tipo de plantilla válido (mismo enum que meal_plan_templates.type en Bckbs).
    tipo = template.get("type")
    if tipo not in ("sequential", "weekday"):
        informe.errores.append(f"template.type debe ser 'sequential' o 'weekday' (valor: {tipo!r}).")
        return informe  # sin tipo válido no se puede comprobar day_key con fiabilidad

    if _celda_vacia(template.get("title")):
        informe.errores.append("template.title es obligatorio.")

    if not items:
        informe.errores.append("El plan no tiene ningún item (comida) definido.")
        return informe

    # 2. Construir el índice de exclusiones duras (alergia/intolerancia) a partir de
    #    restricciones_dieteticas, con la misma severidad de "leve/moderada/grave_anafilaxia"
    #    para alergias que exige agentes/programacion-nutricion/modulos/alergias-intolerancias.md.
    exclusiones: list[tuple[str, str, str | None]] = []  # (descripcion_normalizada, tipo, severidad)
    for r in restricciones:
        tipo_r = r.get("tipo")
        if tipo_r not in TIPOS_EXCLUSION_DURA:
            continue
        descripcion = r.get("descripcion")
        if _celda_vacia(descripcion):
            continue
        severidad = r.get("severidad")
        if tipo_r == "alergia" and _celda_vacia(severidad):
            informe.errores.append(
                f"Restricción de tipo 'alergia' sin 'severidad' ({descripcion!r}) — bloqueante, "
                "ver modulos/alergias-intolerancias.md. No se valida el plan hasta que se resuelva esto."
            )
            continue
        exclusiones.append((_normalizar(descripcion), tipo_r, severidad))

    if informe.errores:
        return informe  # una alergia sin severidad bloquea todo lo demás, no solo un item

    dias: dict[str, dict[str, float]] = defaultdict(lambda: {m: 0.0 for m in MACROS})
    vistos: set[tuple[str, str, int]] = set()

    for n, item in enumerate(items, start=1):
        day_key = item.get("day_key")
        meal_type = item.get("meal_type")
        recipe_id = item.get("recipe_id")

        # 3. Campos obligatorios (igual que exige meal-plan-templates/{id}/items en Bckbs).
        if _celda_vacia(day_key):
            informe.errores.append(f"Item {n}: falta 'day_key'.")
        if meal_type not in MEAL_TYPES_VALIDOS:
            informe.errores.append(f"Item {n}: 'meal_type' debe ser uno de {sorted(MEAL_TYPES_VALIDOS)} (valor: {meal_type!r}).")
        if not isinstance(recipe_id, int):
            informe.errores.append(f"Item {n}: 'recipe_id' debe ser un entero (valor: {recipe_id!r}).")

        # 4. day_key coherente con el tipo de plantilla.
        if not _celda_vacia(day_key):
            if tipo == "weekday" and _normalizar(day_key) not in WEEKDAYS_VALIDOS:
                informe.errores.append(f"Item {n}: day_key {day_key!r} no es un día de la semana válido para type=weekday.")
            elif tipo == "sequential":
                try:
                    if int(day_key) < 0:
                        raise ValueError
                except (TypeError, ValueError):
                    informe.errores.append(f"Item {n}: day_key {day_key!r} debe ser un entero >= 0 para type=sequential.")

        # 5. Duplicado exacto (mismo día, misma comida, misma receta) — probable error de generación.
        clave = (str(day_key), str(meal_type), recipe_id if isinstance(recipe_id, int) else -1)
        if clave in vistos:
            informe.advertencias.append(f"Item {n}: receta {recipe_id!r} repetida en el mismo day_key/meal_type ({day_key!r}/{meal_type!r}).")
        vistos.add(clave)

        # 6. Cribado de alérgenos — solo por título de ingrediente (limitación real, ver
        #    formato-salida/entrega-bckbs.md sección 4: Bckbs no etiqueta alérgenos por ingrediente).
        ingredientes = item.get("ingredientes") or []
        if not ingredientes:
            informe.advertencias.append(
                f"Item {n} (recipe_id={recipe_id!r}): sin lista de ingredientes para cribar — no se pudo "
                "verificar contra las exclusiones. Pide GET recipe-detail/{{id}} antes de fijar la receta."
            )
        else:
            ingredientes_norm = [_normalizar(i) for i in ingredientes]
            for descripcion_norm, tipo_r, severidad in exclusiones:
                if any(descripcion_norm in ing or ing in descripcion_norm for ing in ingredientes_norm):
                    etiqueta = f"{tipo_r}" + (f" ({severidad})" if severidad else "")
                    informe.errores.append(
                        f"Item {n} (recipe_id={recipe_id!r}): ingrediente coincide con exclusión de {etiqueta}: {descripcion_norm!r}."
                    )

        # Acumular macros del día para el punto 7.
        if not _celda_vacia(day_key):
            for m in MACROS:
                valor = item.get(m)
                if isinstance(valor, (int, float)):
                    dias[str(day_key)][m] += valor

    # 7. Macros diarios dentro de tolerancia (±10% por defecto — misma banda que
    #    DailyPlanTrait::calculateDailyPlan() en Bckbs, ver entrega-bckbs.md sección 5).
    if objetivo_diario:
        for day_key, totales in dias.items():
            for m in MACROS:
                objetivo = objetivo_diario.get(m)
                if objetivo is None:
                    continue
                minimo = objetivo * (1 - tolerancia)
                maximo = objetivo * (1 + tolerancia)
                real = totales[m]
                if not (minimo <= real <= maximo):
                    informe.errores.append(
                        f"Día {day_key!r}: '{m}' total ({real:.1f}) fuera de tolerancia ±{tolerancia:.0%} "
                        f"del objetivo ({objetivo}) — rango esperado [{minimo:.1f}, {maximo:.1f}]."
                    )
    else:
        informe.advertencias.append("No se proporcionó 'objetivo_diario' — no se pudo comprobar la tolerancia de macros.")

    return informe


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("plan", help="Ruta al archivo JSON del plan a validar.")
    parser.add_argument("--tolerancia", type=float, default=0.10, help="Tolerancia relativa de macros diarios (por defecto 0.10 = ±10%%, igual que Bckbs).")
    args = parser.parse_args()

    with open(args.plan, encoding="utf-8") as fh:
        plan = json.load(fh)

    informe = validar_plan(plan, tolerancia=args.tolerancia)
    print(json.dumps(informe.to_dict(), ensure_ascii=False, indent=2))
    return 0 if informe.aprobado else 1


if __name__ == "__main__":
    sys.exit(main())
