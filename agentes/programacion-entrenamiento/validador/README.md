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
