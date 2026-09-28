# Formato Excel detallado de revisión (coach) — BeFit / Bckbs

Este documento describe el `.xlsx` **de revisión humana** que el Productor entrega en el Paso 5 cuando genera el detalle semana a semana de uno o varios mesociclos completos (no un esqueleto). Es distinto de `formato-salida/formato-excel.md`, que sigue siendo el único formato que se **importa** a BeFit (`php artisan programs:import`).

**Procedencia (2026-09-27):** formaliza como formato general reutilizable la **estructura/tabla** del Excel real de un cliente de Be Stronger (citado como caso único en `CHANGELOG.md` v0.16.0), tras pedir el usuario que se generaran los 6 mesociclos de un cliente nuevo (Carlos Palomar) "para poder revisar todo" y comparar el resultado contra ese Excel real. **Aclaración explícita del usuario el mismo día:** se generaliza la tabla (hojas por mesociclo, semanas en columnas, columnas Sets×Reps/RIR/Nota técnica, clasificación ancla/variable/nuevo) — NUNCA los valores numéricos concretos de progresión, regresión o descarga de ese cliente, que siguen siendo individualizados por caso (ver `progresion-carga.md` v0.2.1).

## Relación con `formato-excel.md` — dos documentos, dos momentos

1. **Este documento (`formato-excel-detallado.md`):** se genera primero, para que el coach lo revise. Una hoja por mesociclo con el detalle semana a semana en formato ancho (semanas en columnas), clasificación ancla/variable/nuevo, patrones de reps, RIR por serie, y una hoja de visión general que cruza todos los mesociclos. **No se importa nunca directamente a BeFit** — sus columnas no coinciden con el esquema de `workout_template_exercises`.
2. **`formato-excel.md`:** se genera después, mesociclo a mesociclo según toque, **traduciendo** el contenido ya aprobado por el coach de este documento al formato de importación (una fila = un ejercicio de una semana de UN mesociclo). El Productor no inventa nada nuevo en esa traducción — solo cambia de forma (ancho → largo) lo que ya está aprobado aquí.

No generes el segundo sin que el coach haya revisado el primero (mismo principio de Human-in-the-Loop del Paso 5, `system-prompt.md`).

## Qué debes devolver

Un archivo `.xlsx` con:

1. Una hoja **`M1`, `M2`, ... `Mn`** — una por cada mesociclo de `plan-macro.json` (si existe) o del alcance pedido, en el mismo orden. El número de semanas de cada hoja es el `semanas` de ese mesociclo en `plan-macro.json` — **no una cifra fija de 6**, cámbialo según el caso (periodizacion-por-calendario.md v0.3.0).
2. Una hoja **`Visión general`** que cruza todos los mesociclos generados, con el volumen (nº de series) por sesión y semana de un vistazo.
3. Una hoja **`Leyenda y metodología`** — estática, misma estructura en todos los clientes, describe el sistema (ver más abajo).
4. Opcional, no obligatorio: una hoja `📊 DASHBOARD` con gráficos (ver la sección dedicada más abajo) — si se omite, no es un error, pero recomendada cuando el coach vaya a revisar el macrociclo completo de una vez.

---

## Hoja `Mn` (una por mesociclo)

### Cabecera (filas 1-2, libres)

- Fila 1: `<Cliente> — <objetivo_general del macrociclo, resumido> · Mn · Volumen: S1 → S2 → ... → Sn sets` (volumen total en nº de series de esa sesión ancla, semana a semana — ayuda a ver de un vistazo la curva de carga).
- Fila 2 (opcional): técnicas usadas en el mesociclo si aplica (bisets, rest-pause, drop sets, cluster sets...) — solo si el Productor las prescribe explícitamente en alguna nota técnica, no por defecto.

### Cabecera de columnas (filas 3-4)

- Columna A: `Ejercicio`. Columna B: `Pat.` (patrón de reps de ese ejercicio en este mesociclo — `A`, `B` o `C`, ver `progresion-carga.md`).
- A partir de la columna C, **3 columnas por semana**: `Sets×Reps`, `RIR`, `Nota técnica`. Fila 3 lleva el rótulo de la semana fusionado sobre esas 3 columnas (`S1 · RPE 7-7.5`, tomado de `progresion-carga.md`); fila 4 repite los 3 sub-encabezados.

### Filas de ejercicio

- Antes de cada bloque de un día nuevo, una fila con el nombre del día y la sesión (ej. `LUN — Torso A`), sin relleno de columnas de ejercicio.
- Una fila por ejercicio. `Sets×Reps` sigue el patrón de reps de esa fila (`progresion-carga.md`, sección "Patrones de reps"); `RIR` sigue el sistema de RIR por nº de series y si el ejercicio es seguro/no seguro; `Nota técnica` lleva la instrucción de progresión de esa semana (`SUBE X%` / `MANTÉN` / `BAJA` / instrucción de exploración técnica en S1 o de deload en la última semana) -- el `X%` concreto lo decide el Productor para ese cliente, no es un 5% fijo.
- **Clasificación ancla/variable/nuevo:** se marca con el **relleno de color de la celda del nombre del ejercicio** (columna A), no con mayúsculas/minúsculas (evita ambigüedad de mayúsculas por acentos/idioma):
  - Azul claro — ejercicio **ancla**: fijo durante todo el macrociclo, progresa en carga de mesociclo a mesociclo.
  - Sin relleno (blanco) — ejercicio **variable**: mismo patrón biomecánico, rota ~50% del roster de accesorios de un mesociclo al siguiente.
  - Verde claro — ejercicio **nuevo** (prefijo `🆕 ` en el nombre): sin carga de referencia previa, su S1 es siempre exploración técnica pura.
- **Nunca inventes una carga absoluta (kg).** Este formato es 100% relativo/autorregulado por RPE-RIR — `Nota técnica` lleva instrucciones porcentuales (`SUBE 5%`, `BAJA 30%`) o la regla de mantener, nunca un número de kg que el Productor no tiene forma de conocer. Si el cliente aporta `referencias_carga` reales, pueden citarse como referencia de la S1, no como cifra prescrita para el resto del mesociclo.

---

## Hoja `Visión general`

Cruza todos los mesociclos generados en una sola vista, para que el coach compare de un vistazo cómo evoluciona cada sesión mesociclo a mesociclo:

- Fila 1: título del macrociclo + leyenda corta (`MAYÚSCULAS`/`minúsculas`/`🆕` si se usa esa convención textual adicional, o referencia a la leyenda de color de la hoja `Leyenda y metodología`).
- Fila 3: un bloque de columnas por mesociclo (`M1  Vol S1:.. → Sn:..`), fusionado sobre sus N semanas.
- Fila 4: una columna por semana con el total de series de esa sesión ese día (`S1\n<N>s`).
- Filas siguientes: mismas filas de día/ejercicio que las hojas `Mn`, pero con una sola columna `Sets×Reps` por semana (sin RIR ni nota técnica — el detalle vive en la hoja del mesociclo correspondiente).

## Hoja `Leyenda y metodología`

Contenido estático (no cambia entre clientes, salvo el nombre/macrociclo del título):

1. **Clasificación de ejercicio** (color de celda): ancla / variable / nuevo, definiciones exactas de `progresion-carga.md`.
2. **RPE objetivo por semana** (S1..Sn, tabla de `progresion-carga.md`).
3. **Sistema de reps** (patrones A/B/C).
4. **Sistema de RIR** por nº de series y si el ejercicio se trata como seguro/no seguro para ESE cliente (criterio del Productor, no una lista universal, ver `progresion-carga.md`).
5. **Regla de progresión de carga** (sube 5% / mantén / baja, exploración técnica en ejercicios nuevos o sin referencia).
6. **Ejercicios excluidos**, si el perfil del cliente tiene alguno en `restricciones_salud`/`preferencias` — **específico de cada cliente, nunca copiado de otro** (ver nota de `progresion-carga.md` v0.2.0 sobre por qué las exclusiones del cliente original de Be Stronger no se generalizan).

---

## Checklist antes de devolver el archivo

- [ ] Una hoja `Mn` por cada mesociclo de `plan-macro.json`, con tantas semanas como `semanas` tenga ese mesociclo — no forzado a 6.
- [ ] Clasificación ancla/variable/nuevo aplicada de forma consistente (mismo ejercicio = mismo color en todas las semanas de un mesociclo; puede cambiar de variable a variable-rotado en el siguiente mesociclo).
- [ ] Ningún `kg` inventado — solo instrucciones relativas (%, mantén, exploración técnica).
- [ ] Hoja `Visión general` presente si hay más de un mesociclo.
- [ ] Hoja `Leyenda y metodología` presente, con las exclusiones específicas de este cliente si las tiene.
- [ ] Advertencia explícita (en la hoja `Programa`-equivalente o en la fila 1/2 de cada `Mn` posterior al primero) de que los mesociclos aún no generados con datos reales de adherencia son una **proyección**, no un contrato fijo — mismo principio que `system-prompt.md` apartado 4bis.

## Hoja `📊 DASHBOARD` (opcional, con gráficos embebidos) — resuelto 2026-09-29

La limitación de abajo quedó resuelta: **`openpyxl` sí genera gráficos nativos de Excel** (`openpyxl.chart.LineChart`, `BarChart`, `RadarChart`) sin necesidad de construir a mano las partes OOXML de `xl/charts/`/`xl/drawings/` — basta con volcar los datos que alimentan cada gráfico en celdas normales de la misma hoja (una tabla pequeña, puede quedar fuera del área visible) y apuntar el gráfico a ese rango con `Reference` + `add_chart`. Probado en la generación real de 5 macrociclos completos (2026-09-28/29, ver `CHANGELOG.md` v0.24.0), sin adjuntar esos archivos a este repo por ser datos de cliente.

Si se añade esta hoja (recomendada cuando el coach vaya a revisar el macrociclo completo, no obligatoria para un mesociclo suelto):

1. **Tira de KPI** (fila superior, 4-6 celdas fusionadas con relleno de color): pico de series máximo del macrociclo y en qué semana, número de mesociclos y semanas totales, días/semana, variación de series de la semana 1 entre el primer y el último mesociclo, series totales del macrociclo.
2. **Gráfico de líneas**: series totales por semana, a lo largo de TODAS las semanas del macrociclo (eje X = `M1 S1`, `M1 S2`... `Mn Sn`) — el mejor gráfico único para ver de un vistazo si el volumen realmente sube o si hay un mesociclo plano/decreciente (exactamente lo que `validador/validar_macrociclo.py` V1/V2b comprueba por código; el gráfico es la versión visual para el coach).
3. **Gráfico de barras**: series de la semana 1 (o el pico) por mesociclo, una barra por mesociclo — hace evidente de un vistazo si algún mesociclo no sube respecto al anterior.
4. **Gráfico de radar**: series por grupo muscular, comparando el primer mesociclo contra el pico del último — muestra qué grupos crecieron más y cuáles se quedaron atrás en el macrociclo completo.
5. **Tabla de progresión por grupo y mesociclo** (semana 1, una fila por grupo muscular, una columna por mesociclo): con relleno de color condicional simple (verde si sube respecto al mesociclo anterior, amarillo si igual, rojo si baja) — es la versión tabular de V1, útil para que el coach vea el detalle exacto detrás del gráfico de radar.
6. Si el macrociclo corrige o sustituye un programa anterior del mismo cliente, una tabla **antes/después** con los indicadores más relevantes de ese caso concreto (nunca genérica — depende de qué estaba mal en el programa anterior).

Los datos que alimentan cada gráfico son los mismos que ya se calculan para las hojas `Mn` y `Visión general` — no dupliques la lógica, vuelca esas mismas cifras a una zona de datos de esta hoja y referencia esas celdas desde los objetos `Chart`.
