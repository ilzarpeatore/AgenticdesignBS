# Validador determinista (Paso 3)

Código real, no prosa: comprueba mecánicamente el `.xlsx` que el Productor
genera (formato descrito en `../formato-salida/formato-excel.md`) antes de
que llegue al Crítico (Paso 4) o al humano (Paso 5).

## Qué comprueba

- Hojas `Programa` y `Programación` presentes, con las 19 columnas
  obligatorias de `Programación`.
- `semanas` de la hoja `Programa` coincide con las semanas distintas
  realmente escritas; si se pasa `--semanas-esperadas`, también que sean
  exactamente esas y sin huecos.
- Cada fila de ejercicio tiene `ejercicio`, `series` y (`reps` o
  `duracion_seg`).
- Ninguna fila de descanso (`es_descanso=TRUE`) lleva columnas de ejercicio
  rellenas.
- `nombre_dia` es consistente dentro de la misma (semana, día).
- `dia` está en rango 1-7.
- Si se pasa `--excluidos`, ningún ejercicio de la lista aparece en el
  programa (uso: lesión activa o material no disponible de ese cliente
  concreto — ver `seleccion-ejercicios-sustitucion-lesion.md`).

Lo que **no** es error, solo advertencia (criterio ya explícito en
`formato-excel.md`, no una interpretación nueva de este código):

- `rir` y `rpe` rellenos a la vez en la misma fila (se usa `rpe`, no es un
  fallo).
- Un ejercicio que no coincide con ningún título de
  `../formato-salida/catalogo-ejercicios.xlsx` — puede ser un ejercicio
  nuevo legítimo; ver "Frontera de responsabilidad" en `formato-excel.md`
  para por qué esto nunca debe ser un error duro aquí.

## Uso

```bash
python3 validar_programa.py <programa.xlsx> \
    --catalogo ../formato-salida/catalogo-ejercicios.xlsx \
    --excluidos "Hack Squat" "Elevación lateral en máquina" \
    --semanas-esperadas 3
```

Devuelve un JSON (`aprobado`, `errores`, `advertencias`) por stdout y código
de salida 0/1. `aprobado_validador` en `esquemas/log-registro.schema.json`
se rellena con el valor de `aprobado`.

## Pruebas

```bash
python3 -m unittest discover -s tests
```

El fixture principal (`tests/fixtures/Mesociclo_1_TONI_Septiembre.xlsx`) es
el programa real entregado a un cliente real (lesión de manguito rotador,
sin Hack Squat ni elevación lateral en máquina), no un ejemplo sintético.
El resto de pruebas son copias de ese mismo archivo mutadas para provocar
cada fallo uno a uno, así el validador se prueba contra el mismo tipo de
archivo que genera el Productor.

## `validar_macrociclo.py` — progresión ENTRE mesociclos (2026-09-29)

`validar_programa.py` comprueba UN `.xlsx` contra el formato; no puede ver si el macrociclo completo
**progresa** de un mesociclo al siguiente, porque eso solo existe comparando varios archivos a la vez. Ver
`../modulos/biomecanica-programacion-hipertrofia.md` sección 9bis para la regla completa y el caso real que
expuso este hueco -- un macrociclo puede pasar `validar_programa.py` en los seis mesociclos y aun así tener
el volumen semanal total plano o decreciente mes a mes.

Corre esto además de `validar_programa.py` (por archivo) cuando generes o revises dos o más mesociclos
seguidos del mismo macrociclo — ver `system-prompt.md` sección 6:

```bash
python3 validar_macrociclo.py <carpeta-con-los-.xlsx-de-los-mesociclos> \
    --agrupar-hombro \
    --patron-seguro "press de pecho|press de hombro|fondos|apertura" --reps-min-seguro 8 --rir-min-seguro 2 \
    --texto
```

Comprueba mecánicamente: **V1** las series de la semana 1 de cada grupo muscular suben de mesociclo a
mesociclo; **V2b** el pico semanal de cada grupo (no solo la base) tampoco retrocede, aunque la base suba —
la forma más fácil de que esto falle en silencio es aplicar la onda intra-mesociclo de forma inconsistente
entre mesociclos; **V2** cada mesociclo tiene una descarga real (última semana por debajo del 80% de su
pico); **V3** el rango de reps cambia semana a semana dentro de cada mesociclo, con ambos sentidos
representados en cada sesión; **V4** (opcional, `--patron-seguro`) mínimos de reps/RIR para un patrón de
ejercicio marcado por la restricción de un cliente concreto — no hay ninguna lista de ejercicios "seguros"
hardcodeada, se pasa por CLI igual que `--excluidos` en `validar_programa.py`.

Los archivos se procesan en el orden en que se pasan (o el orden alfabético del glob de una carpeta) — ese
orden es el orden real de los mesociclos. Si el título de la hoja `Programa` de un archivo dice "Mesociclo N",
se usa solo como advertencia de cruce, nunca como filtro: este repo no impone ninguna convención de títulos.

Salida: mismo contrato que `validar_programa.py` (JSON con `aprobado`/`errores`/`advertencias`), más un campo
`tablas` con el detalle legible por humano de cada regla — usa `--texto` para imprimir solo ese detalle en
texto plano si lo vas a enseñar directamente al coach.

**Pruebas** (`tests/test_validar_macrociclo.py`): a diferencia del validador de un mesociclo, este comprueba
una propiedad matemática del conjunto de archivos, no algo específico de ningún cliente — las fixtures son
macrociclos sintéticos generados con `openpyxl` (correctos por diseño, mutados uno a uno para provocar cada
fallo), no un caso real adjunto. Probado además contra los macrociclos reales de 5 clientes distintos (6
mesociclos cada uno) durante su desarrollo, sin adjuntarlos a este repo por ser datos sensibles de cliente.
