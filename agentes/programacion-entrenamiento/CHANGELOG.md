# Changelog — Asistente de Programación de Entrenamiento

## v0.14.1 — 2026-09-16

- **Embarazo/RED-S solo para perfil mujer:** decisión de producto del usuario tras v0.14.0 — `parq_pregnant_or_possible`/`parq_menstrual_change_or_stress_fracture` dejan de ser obligatorias para hombre/otro (Bckbs las guarda `null`, no `false`, para no confundir "no aplica" con "se preguntó y dijo que no"). Nuevo campo `genero` en `esquemas/perfil-cliente.schema.json`, validación condicional (`allOf`/`if`/`then`) en vez de `required` fijo. `contraindicaciones-medicas.md` sube a v0.3.0. Ocultar el campo en el formulario de la app para perfiles no-mujer queda fuera de Bckbs (frontend).

## v0.14.0 — 2026-09-16

Primera reconciliación real de `perfil-cliente.schema.json` contra el onboarding de Bckbs (antes nunca se había contrastado contra las tablas reales, solo diseñado por lógica). El usuario confirmó que el onboarding real de la app queda registrado en BD, lo que permitió comparar el esquema contra las columnas reales sin necesitar datos de ningún cliente.

- **`cribado_medico`:** cambia a los nombres de campo reales de `par_q_answers`. Se encontró que tres preguntas que el diseño ya asumía (embarazo/posibilidad, alteración menstrual/fractura por estrés, trastorno alimentario) nunca se preguntaban en el onboarding real — se añadieron a Bckbs esta misma fecha (`par_q_answers`, migración + validación + tests), y ahora también marcan `flagged_for_review`. Ver `modulos/contraindicaciones-medicas.md` v0.2.0 para el mapeo completo campo a campo.
- **`nivel_fuerza` → `experiencia_entrenamiento`:** el enum fijo (principiante/intermedio/avanzado) no existía como tal en la app — Bckbs guarda `training_experience_months`/`technique_level` (autoevaluados, con override de coach ya implementado y consumido por el motor de autorregulación vía `ConditionVariable::NIVEL_EXPERIENCIA`). El esquema ahora pide esos dos datos reales y deriva `nivel_fuerza` con una regla explícita — propuesta, pendiente de confirmar/ajustar con casos reales.
- **`disponibilidad`:** de días de la semana + minutos exactos (que el onboarding nunca preguntó así) a un conteo de días/semana + franja preestablecida de duración (`training_days_per_week`/`session_duration_preference`, los campos reales). Ahora también editable por el cliente sin repetir el onboarding completo — nuevo endpoint `POST training-availability-update` en Bckbs.
- **`system-prompt.md` (v0.10.0):** Paso 1, puntos 4 y 6, actualizados con los campos reales y la aclaración de que los días concretos de la semana los decide el Productor, no el cliente.

## v0.13.0 — 2026-09-15

Preparación para el nuevo Agente de Programación de Nutrición (`agentes/programacion-nutricion/`), que lee `restricciones_dieteticas` de este mismo esquema en vez de duplicar el intake.

- **`esquemas/perfil-cliente.schema.json`:** `restricciones_dieteticas` pasa de `string[]` a objetos estructurados con `tipo` (alergia/intolerancia/aversión/preferencia ética-religiosa) y `severidad` obligatoria cuando `tipo: alergia` — mismo patrón de bloqueo duro que ya tiene `restricciones_salud`/`lesion_localizada`, para no repetir con alergias el mismo error de ambigüedad que expuso el caso de Toni con lesiones.

## v0.12.0 — 2026-09-14

Cuarta y última fase de las mejoras identificadas tras el caso real de Toni: el razonamiento del Paso 2 pasa de narración efímera en el chat a dato persistido y auditable.

- **`esquemas/log-registro.schema.json`:** nuevo campo obligatorio `razonamiento` (texto libre, no vacío) — traza completa del Chain-of-Thought del Paso 2: módulos activos y por qué, conflictos detectados, resolución según la jerarquía universal, y la consulta del catálogo de ejercicios (Fase 3 de esta misma serie de mejoras).
- **`system-prompt.md` (v0.8.0):** el Paso 2 indica explícitamente que ese razonamiento se guarda en este campo, no solo se narra.
- **`docs/roadmap.md`:** la fila de memoria episódica menciona ahora `razonamiento` junto a `historial_ciclos`.

## v0.11.0 — 2026-09-14

Tercera fase de las mejoras identificadas tras el caso real de Toni: la consulta del catálogo de ejercicios se formaliza como paso explícito, en vez de referencia pasiva.

- **`system-prompt.md` (v0.7.0):** nuevo punto 4 dentro del razonamiento del Paso 2 (Productor) — "Consulta del catálogo de ejercicios" (Tool Use, cap. 5). Para cada ejercicio, el Productor debe documentar el nombre buscado, el título del catálogo encontrado (si lo hay) y, ante una sustitución forzada por lesión o material, qué alternativa del catálogo mantiene el mismo patrón y vector de resistencia. Refleja el uso real que ya se le dio al catálogo al generar el programa de Toni (Press banca con mancuernas, sustitución de Hack Squat por Prensa de piernas, etc.), ahora como paso explícito y no como consulta implícita sin rastro.
- **`docs/roadmap.md`:** la descripción del Paso 2 en la tabla de arquitectura menciona ahora la consulta activa del catálogo (Tool Use) junto al razonamiento Chain-of-Thought.

## v0.10.0 — 2026-09-14

Segunda fase de las mejoras identificadas tras el caso real de Toni: el intake de lesiones pasa de advisory a bloqueante.

- **`esquemas/perfil-cliente.schema.json`:** para `restricciones_salud` con `categoria: lesion_localizada`, ahora son obligatorios `gesto_doloroso`, `fase` (`aguda`/`en_recuperacion`/`cronica_controlada`) y `empeora_con_actividad_o_impacto`; `autorizacion_profesional` pasa a ser obligatorio también cuando `fase: aguda` (antes solo para `contraindicacion_relativa`). Aplicado con `if`/`then` de JSON Schema, no solo como descripción.
- **`system-prompt.md` (v0.6.0):** el Paso 1 apartado 5 y la lista "NO debes" declaran explícitamente que no se genera nada, ni siquiera un borrador preliminar, sin estos cuatro datos ante una lesión localizada. El caso límite "información vaga sobre una molestia" deja de decir "pide especificidad" (tono de recomendación) y pasa a "bloqueante, no un matiz a resolver sobre la marcha".
- **`modulos/seleccion-ejercicios-sustitucion-lesion.md` (v0.2.0):** el guardrail duro ("lesión activa → excluir por completo") se redefine en términos del campo `fase` en vez de la palabra ambigua "activa"; se documenta el caso real que expuso la tensión (lesión de manguito rotador sin especificidad forzó una decisión de juicio del Productor).

## v0.9.0 — 2026-09-14

Primera fase de las mejoras identificadas tras el caso real de Toni: el validador determinista (Paso 3) deja de ser un backlog histórico ("hoy es prosa que se lee a ojo", desde v0.1.0) y pasa a ser código real, probado contra un archivo real.

- **Nueva carpeta `validador/`:**
  - `validar_programa.py` — comprueba mecánicamente el `.xlsx` final (formato de `formato-salida/formato-excel.md`): hojas y columnas exactas, `semanas` declaradas vs. semanas realmente escritas (y sin huecos), `ejercicio`/`series`/`reps` obligatorias por fila salvo descanso, filas de descanso sin columnas de ejercicio rellenas, `nombre_dia` consistente dentro del mismo día, `dia` en rango 1-7, y una lista opcional de ejercicios excluidos por cliente (lesión, material no disponible). `rir`+`rpe` simultáneos y un ejercicio ausente del catálogo quedan como advertencia, no error, tal como ya especificaba `formato-excel.md`.
  - `tests/` — 13 pruebas. El fixture principal es el programa real entregado a Toni (`Mesociclo_1_TONI_Septiembre.xlsx`), no un ejemplo sintético; el resto son copias de ese mismo archivo mutadas para provocar cada fallo uno a uno.
  - `README.md` — qué comprueba, qué es solo advertencia y por qué, uso de la CLI.
- **`system-prompt.md` (v0.5.0):** el Paso 3/4 ahora referencia el código real; un borrador no avanza a Crítico/revisión humana si `validar_programa.py` devuelve errores.
- **`docs/roadmap.md`:** eliminado del backlog el ítem ya resuelto.

## v0.8.0 — 2026-09-14

Se integra el formato de entrega real hacia el sistema BeFit — hasta ahora el "formato de salida" del agente era solo interno (JSON de esquemas); ahora hay un formato de entrega final real, que es lo que de verdad se importa a producción.

- **Nueva carpeta `formato-salida/`:**
  - `formato-excel.md` — especificación completa del `.xlsx` de dos hojas (`Programa` + `Programación`), 19 columnas, reglas de días de descanso implícitos, progresión explícita semana a semana, notación de bloques/superseries.
  - `catalogo-ejercicios.xlsx` — catálogo real de 1.505 ejercicios ya existentes en la base de datos (id + título) — usar estos nombres al escribir la columna `ejercicio` siempre que exista coincidencia razonable, para que el matcher de BeFit reutilice el ejercicio en vez de crear un duplicado.
  - `ejemplo-programa.xlsx` — programa de referencia completo y correctamente relleno (hipertrofia full body, 5 sesiones, 4 semanas con deload).
- **`system-prompt.md` (v0.4.0):** el Paso 5 (revisión humana) ya no termina en el JSON interno — termina en este archivo `.xlsx`, listo para `php artisan programs:import`.

## v0.7.0 — 2026-09-14

Relectura completa de los capítulos del libro todavía no aplicados (Routing, Resource-Aware Optimization, Reasoning Techniques, Prioritization, Parallelization) y actualización del `system-prompt.md` en consecuencia (v0.3.0).

- **Nuevo Paso 2 explícito — Productor con razonamiento (Chain-of-Thought, cap. 17):** antes de generar el borrador, el Productor debe listar por escrito los módulos activos, los conflictos detectados entre ellos y cómo los resuelve según la jerarquía universal. Antes esto ocurría implícitamente sin dejar rastro auditable.
- **Precisión terminológica (Routing, cap. 2):** el Paso 0 se documenta explícitamente como enrutamiento *multi-etiqueta* (varios módulos activos a la vez), distinto del enrutamiento clásico excluyente. La elección entre `periodizacion-orientada-evento.md` y `periodizacion-por-calendario.md` se documenta como enrutamiento determinista por regla (existe `fecha_evento` o no) — nunca una decisión que el Productor deba razonar.
- **Nueva sección "Asignación de modelo por paso" (Resource-Aware Optimization, cap. 16):** modelo rápido/económico para Paso 0, Paso 1 y Paso 4 (Crítico); el modelo más capaz disponible reservado para el Paso 2 (Productor), que es donde un error cuesta más caro.
- **Regla de prioridad para `requiere_revision` concurrentes (Prioritization, cap. 20):** cuando coinciden varios motivos de revisión, se ordenan por la jerarquía universal (seguridad primero), no se mezclan sin indicar cuál es más urgente.
- **Parallelization (cap. 3):** revisado — no se encontró una aplicación real a esta escala (la cadena de 6 pasos es secuencial por dependencia; el validador determinista ya es código, no LLM). Sin cambios; se deja anotado por si Mesociclo 1 introduce generación por lotes de varios clientes a la vez.
- Referencias cruzadas de sección corregidas en todos los módulos tras la renumeración del `system-prompt.md`.

## v0.6.0 — 2026-09-14

Se pospone el módulo de embarazo (sin cliente real que lo necesite ahora) y se prioriza cerrar huecos de base que afectan a todos los clientes.

- **Nuevo módulo general:** `modulos/calentamiento-activacion.md` — protocolo RAMP, series de aproximación (3-5, cercanas al peso de trabajo cuanto más exigente la carga), estiramiento estático solo al final de la sesión (nunca antes de fuerza/potencia si supera 60s), versión reducida para sesiones con poco tiempo. Referencias: Jeffreys 2007 (RAMP); Behm et al. 2019 (estiramiento estático agudo).
- **Nuevo módulo general:** `modulos/monitorizacion-fatiga-bienestar.md` — RPE de sesión (método Foster) para calcular carga de entrenamiento real, cuestionario de bienestar diario (Hooper-Mackinnon: sueño, fatiga, dolor muscular, estrés), y cómo usar ambos para ajustar sesiones puntuales o adelantar un deload. Da herramientas concretas a las "señales de fatiga" que `gestion-fatiga-deload.md` solo describía de forma genérica.
- **`esquemas/log-registro.schema.json`:** nuevos campos `rpe_sesion`, `carga_sesion` y `bienestar_diario`.
- **Conflictos anotados** en `gestion-fatiga-deload.md`, `pliometria-rigidez-tendinosa.md`.
- **Backlog limpiado:** ítems ya resueltos eliminados de `docs/roadmap.md`; módulos de población/deporte específicos (fútbol, embarazo, patología concreta) quedan explícitamente pospuestos hasta que exista un cliente real que los necesite.

## v0.5.0 — 2026-09-14

Cierra la mitad que faltaba de "carga y volumen": `progresion-carga.md` solo cubría carga (peso); ahora `biomecanica-programacion-hipertrofia.md` añade cómo debe progresar el volumen (número de series) dentro de un mesociclo.

- **`biomecanica-programacion-hipertrofia.md` (v0.2.0):** nueva sección 9, "Progresión de volumen dentro del mesociclo" — marco MEV/MAV/MRV (Israetel/RP Strength), esquema de progresión de 1-2 series/semana, regla de no subir carga y volumen agresivamente a la vez, y nota de nivel de certeza (marco práctico de la industria, no consenso académico cerrado sobre acumulación de fatiga). Referencias añadidas: Israetel et al.; *Mesocycle Progression in Hypertrophy: Volume Versus Intensity* (S&C Journal, 2020).
- **Conflictos anotados** en `progresion-carga.md` y `gestion-fatiga-deload.md` para reflejar la interacción carga/volumen y cómo el MRV teórico se ajusta con señales reales de fatiga.

## v0.4.0 — 2026-09-14

Respuesta a control de calidad: el agente no bajaba a nivel de biomecánica ni de programación fina de carga/volumen para hipertrofia — solo manejaba el contexto de déficit/recomposición. Deep search y nuevo módulo general para cerrar ese hueco.

- **Nuevo módulo general:** `modulos/biomecanica-programacion-hipertrofia.md` — perfiles de resistencia (curvas de fuerza), rango de movimiento e hipertrofia mediada por estiramiento, proximidad al fallo (RIR), rango de repeticiones, descansos entre series, orden de ejercicios, enfoque atencional, peso libre vs. máquina, unilateral vs. bilateral. Referencias: Warneke et al. 2023; Schoenfeld 2021 (continuo de repeticiones); Singer/Wolf/Generoso/Schoenfeld 2024 (descansos); meta-análisis de orden de ejercicios 2020; investigación de enfoque atencional; meta-análisis peso libre vs. máquina 2023.
- **`hipertrofia-recomposicion-corporal.md` (v0.2.0):** se reorganiza para no duplicar contenido — ahora se apoya en el módulo nuevo para el "cómo" (RIR, ROM, descansos) y se queda solo con el "cuánto y en qué contexto energético" (déficit, viabilidad por nivel, periodización). Declarado que ambos módulos se activan siempre juntos.

## v0.3.0 — 2026-09-14

Integración de contraindicaciones médicas reales (ACSM, PAR-Q+, ACOG, RED-S), siguiendo el proceso de `CONTRIBUTING.md`.

- **Nuevo módulo, capa de seguridad transversal:** `modulos/contraindicaciones-medicas.md` — cribado obligatorio tipo PAR-Q+, contraindicaciones absolutas (cardiovasculares, aneurisma, retinopatía proliferativa, hernia sintomática, embarazo de riesgo, trastorno alimentario activo/RED-S) y relativas (hipertensión, diabetes no controlada, osteoporosis, anticoagulantes, cardiopatía estable, embarazo sin contraindicación absoluta) con su protocolo de actuación. Referencias: ACSM Guidelines for Exercise Testing and Prescription; PAR-Q+; ACOG; Mountjoy et al. (RED-S); Retina Today (2021).
- **`system-prompt.md` (v0.2.0):** el cribado de este módulo pasa a ser el primer paso del Paso 1, obligatorio antes de la selección de módulos (Paso 0). Si detecta contraindicación absoluta, el pipeline se detiene sin generar nada.
- **`esquemas/perfil-cliente.schema.json`:** nuevo campo obligatorio `cribado_medico` (respuestas PAR-Q+); `restricciones_salud` ahora distingue `categoria` (lesión localizada vs. contraindicación relativa/absoluta) para enrutar cada caso al módulo correcto.
- **Conflictos anotados** en `seleccion-ejercicios-sustitucion-lesion.md` (precedencia: contraindicaciones médicas se resuelven antes) y en `hipertrofia-recomposicion-corporal.md` (RED-S/trastorno alimentario bloquea la activación del módulo, no solo el déficit calórico).

## v0.2.0 — 2026-09-14

Deep search de evidencia científica para el módulo de recomposición corporal (pendiente desde v0.1.0), siguiendo el proceso de `CONTRIBUTING.md`.

- **Nuevo módulo específico:** `modulos/hipertrofia-recomposicion-corporal.md` — viabilidad por nivel de entrenamiento, condiciones energéticas/proteicas (para dimensionar el entrenamiento, no para prescribir), volumen y frecuencia, progresión de carga en déficit, periodización macro/meso/micro, cardio concurrente, coordinación con diet breaks/refeeds. Referencias: Barakat et al. 2020; Murphy & Koehler 2022; Roth et al. 2023; Schoenfeld et al. 2016/2017; Grgic et al. 2017; Morton et al. 2018; Garthe et al.; editorial Frontiers in Physiology 2024.
- **Nuevo módulo general:** `modulos/periodizacion-por-calendario.md` — formaliza como módulo independiente la estructura macro/meso/micro que hasta ahora solo vivía como tabla narrativa en `docs/roadmap.md`.
- **Conflictos anotados** en `fuerza-maxima-potencia.md`, `progresion-carga.md` y `gestion-fatiga-deload.md` para reflejar su interacción con el módulo nuevo (Paso 4 del proceso de mantenimiento).

## v0.1.0 — 2026-09-14

Importación inicial. Se parte del agente original (v1.0, 2026-09-07), especializado en fuerza/pliometría para corredores de media maratón — que a su vez era la reescritura completa de un agente anterior de hipertrofia/pérdida de grasa (ya no conservado).

Se descompone el contenido en:

- `system-prompt.md` — marco fijo generalizado: rol, alcance, protocolo de redirección y protocolo de intake, sin asumir ningún deporte u objetivo concreto.
- `modulos/fuerza-maxima-potencia.md` — general (de la sección 3.2 y 3.8 del original)
- `modulos/pliometria-rigidez-tendinosa.md` — general (sección 3.3)
- `modulos/progresion-carga.md` — general (sección 3.5)
- `modulos/seleccion-ejercicios-sustitucion-lesion.md` — general (principios de la sección 3.4)
- `modulos/gestion-fatiga-deload.md` — general (sección 3.6)
- `modulos/periodizacion-orientada-evento.md` — general, condicional a fecha de evento (sección 3.7, generalizada de "carrera" a "evento")
- `modulos/running-economia-carrera.md` — específico (sección 3.1, prioridades de la 3.4, y las notas de casos frecuentes de running)

Motivo del cambio de arquitectura: el agente original se reescribía por completo cada vez que cambiaba el tipo de cliente (un solo documento activo). Eso no escala a atender simultáneamente objetivos distintos (recomposición, rendimiento deportivo, patología). La base de conocimiento modular permite que el Productor combine varios módulos por cliente sin encasillarlo en una categoría fija.

**Pendiente:**
- Módulo de Hipertrofia y recomposición corporal (no existe versión previa — se escribe de cero).
- Revisar si parte de las "prioridades de selección de ejercicios" de `running-economia-carrera.md` debería extraerse a un módulo general de demandas de tren inferior en deportes de impacto/cambio de dirección.
- Automatizar la checklist "verificable mecánicamente" de cada módulo como validador determinista real (hoy es una lista que se lee a ojo).
