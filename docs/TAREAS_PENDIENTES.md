# Tareas pendientes — sistema de agentes (consolidado)

> Único documento de tareas del proyecto. Antes esto vivía repartido entre `docs/roadmap.md` (sección "Backlog abierto"), `AGENTE_IMPORTADOR.md` en Bckbs y un encargo aparte (`BRIEF_registro_alergias_intolerancias.md`) — se consolida aquí para no mantener la misma tarea descrita en varios sitios a la vez. `roadmap.md` sigue siendo el documento de arquitectura/diseño; este es el documento de seguimiento de trabajo pendiente.
>
> **Última actualización:** 2026-09-17 (sesión con acceso real a `bestronger-vps`: 1.2 confirmada ya aplicada en producción; 2.3 parcial — Borja resuelto, Toni sigue abierto a propósito; 1.1 esperando un catálogo `.xlsx` nuevo del usuario para cerrarse; además, en paralelo, 2.6 resuelto — repo privado `ilzarpeatore/bstronger-memoria-clientes` creado; 2.7 resuelto — módulo `habitos-prioritarios.md` en el agente de nutrición)

## Cómo leer esta tabla

| Columna | Significado |
|---|---|
| Estado | 🔒 Bloqueada (no se puede avanzar desde esta sesión) · 🟡 Requiere el usuario (dato/decisión que solo puede dar él) · ⏸️ Pospuesta a propósito (no se escribe por completitud especulativa) · 🟢 Mejora opcional (no bloqueante) |
| Bloqueador | Qué hace falta exactamente para desbloquearla |

---

## 1. Bloqueadas por acceso a BD/VPS real (`bestronger-vps`)

**(2026-09-17)** Esta sesión sí tuvo acceso SSH real a `bestronger-vps` (`/var/www/testapp`, `APP_ENV=production`, BD `bestronger_test`, la BD real de `testapp.bestronger.es` pese al nombre). 1.2 estaba marcada como bloqueada aquí y **ya no lo estaba** — alguien la aplicó ya en producción, probablemente durante el trabajo de integración de onboarding del 2026-09-16/17. 1.1 se verificó parcialmente. Detalle en cada fila.

| # | Tarea | Estado | Bloqueador | Detalle completo |
|---|---|---|---|---|
| 1.1 | Verificar contra BD real todo lo mergeado a `main` de Bckbs (`--json`, `programs:assign-client`, `POST program-import`, hotfix `fail()`→`reportFailure()`, y ahora también `--confidence-gate`/`--check-integrity`, ver 4.1/4.2) | 🟡 (parcial — ver nota) | **(2026-09-17) Verificado parcialmente contra BD real:** `programs:import excel --dry-run --json` corrió limpio contra los dos catálogos ya presentes en `storage/imports/` del VPS (`mesociclo_toni.xlsx`, `BeStronger_M1_Entrenamiento.xlsx`) — ambos ya estaban importados (`training_program #48` y `#50`, detectados correctamente por hash de contenido `source_id`, buena señal de la lógica de dedupe). `--confidence-gate` no se pudo probar de verdad porque el flujo se corta en el "ya existe" antes de llegar a la lógica de gate — necesita un catálogo nuevo sin importar. `programs:check-integrity` (sin `--fix`) corrió limpio contra las 207 filas reales: "Sin referencias rotas". **No se ejecutó** import real ni `programs:assign-client` — no había catálogo nuevo que justificara escribir, y la regla del propio proyecto (`AGENTE_IMPORTADOR.md` sección 8, "nunca escribir en producción sin revisión humana") exige un caso concreto con `review_required` visto por un humano antes de escribir, no probarlo por probarlo. Falta: un `.xlsx` nuevo (no importado aún) para ejercitar de punta a punta creación real + `--confidence-gate` con casos ambiguos de verdad + `assign-client` | `Bckbs/docs/AGENTE_IMPORTADOR.md`, sección "Tarea pendiente" |
| 1.2 | Construir el registro estructurado de severidad de alergias/intolerancias en Bckbs (`client_limitations`: columna `severity`, ampliar `type`, validación 422 si `type=allergy` sin `severity`, tests) | ✅ Resuelto — ver "Ya resuelto" | — | `BRIEF_registro_alergias_intolerancias.md` |
| 1.3 | Etiquetado de alérgenos por ingrediente/receta en Bckbs (`ingredients`/`recipes` no tienen columna tipo `contiene_gluten`) | 🔒 | Depende de 1.2 (ya resuelta) — sigue sin escribirse porque no hay un caso real que lo necesite todavía, no por bloqueo técnico | `agentes/programacion-nutricion/formato-salida/entrega-bckbs.md`, sección 4 (limitación documentada); `BRIEF_registro_alergias_intolerancias.md`, sección 6 ("fuera de alcance") |

---

## 2. Bloqueadas por datos o decisión del usuario (no técnicas)

| # | Tarea | Estado | Bloqueador | Detalle completo |
|---|---|---|---|---|
| 2.1 | Definir `perfil-cliente.schema.json`/`perfil-nutricional.schema.json` con datos reales de clientes actuales | 🟡 (parcial) | **(2026-09-16) La estructura ya se reconcilió** contra las columnas reales del onboarding (`par_q_answers`/`training_questionnaire_answers`/`nutrition_questionnaire_answers`) sin necesitar datos de ningún cliente — el usuario confirmó que el onboarding real queda en BD, así que se comparó el esquema contra el schema de esas tablas directamente. Queda pendiente contrastar con VALORES reales (no solo la forma) de 2-3 clientes actuales, para detectar patrones que la estructura por sí sola no revela | `agentes/programacion-entrenamiento/esquemas/perfil-cliente.schema.json`, `agentes/programacion-nutricion/esquemas/perfil-nutricional.schema.json` |
| 2.2 | Caso real de cliente de principio a fin para el Asistente de Nutrición (equivalente al caso de Toni en entrenamiento) | 🟡 | El usuario tiene que aportar uno de los recetarios por cliente que ya construye a mano | `agentes/programacion-nutricion/validador/README.md` (fixtures hoy sintéticos, sin caso real) |
| 2.3 | Migrar a `client_limitations` las alergias que hoy solo existen como texto libre en `nutrition_questionnaire_answers.allergies_intolerances` | 🟡 (parcial) | **(2026-09-17) Borja Betanzos (user_id 101) — resuelto.** El usuario confirmó `type: intolerance`, sin `severity` (no aplica a un tipo que no es `allergy`). Creada `client_limitations.id=2` contra el VPS real. **Toni Pérez Fernández (user_id 99) — sigue abierto, a propósito.** Texto original: "fruta/lactosa". El usuario avisó explícitamente: no asumir "leve" por defecto en alergias/intolerancias — una alergia a la fructosa (que es lo que "fruta" podría significar) puede ser grave, y no hay información suficiente en el texto libre para decidir `type`/`severity` sin adivinar. Necesita una conversación directa con Toni para aclarar exactamente a qué es alérgico/intolerante y con qué severidad — no crear la fila hasta entonces. `user_id 8` y `user_id 100` del listado original eran datos de prueba (demo, "prueba@prueba.com"), ignorados | `BRIEF_registro_alergias_intolerancias.md`, sección 5 |
| 2.4 | Confirmar o ajustar la regla de derivación de `nivel_fuerza` (principiante/intermedio/avanzado) a partir de `experiencia_meses`/`tecnica_autoevaluada` | 🟡 | Es un criterio de coach, no algo que se pueda derivar solo de la estructura de datos — la regla propuesta (2026-09-16) es un punto de partida, no una decisión final | `agentes/programacion-entrenamiento/esquemas/perfil-cliente.schema.json`, campo `experiencia_entrenamiento.nivel_fuerza` |
| 2.5 | Decidir qué hacer con clientes que completaron el onboarding antes del 2026-09-16 — se quedan con `parq_pregnant_or_possible`/`parq_menstrual_change_or_stress_fracture`/`parq_eating_disorder_history`/`disponibilidad_cocina` a `NULL` para siempre salvo que se les vuelva a preguntar | 🟡 | Decisión de producto (¿re-prompt en la app a los clientes existentes? ¿se asume el hueco hasta el próximo ciclo de cada uno?), no algo que el código pueda resolver solo | `Bckbs`, migraciones `2026_09_16_100000`/`2026_09_16_100001` |
| 2.6 | Decidir dónde viven físicamente los archivos reales de memoria por cliente (`log-registro`/`log-nutricion`/`checkpoint-fisico`) | ✅ Resuelto — ver "Ya resuelto" | — | `agentes/programacion-entrenamiento/system-prompt.md`, sección "Memoria del cliente" |
| 2.7 | Añadir una capa de "hábitos prioritarios" a alguno de los dos agentes | ✅ Resuelto — ver "Ya resuelto" | — | `agentes/programacion-nutricion/modulos/habitos-prioritarios.md` |

---

## 3. Pospuestas a propósito (no se escriben por completitud especulativa)

Mismo criterio en los dos agentes: un módulo de población/deporte específico solo se escribe cuando existe un cliente real que lo necesita, nunca por anticipado.

| # | Tarea | Agente | Estado |
|---|---|---|---|
| 3.1 | Módulos de población/deporte específicos (fútbol, otros deportes de equipo) | Entrenamiento | ⏸️ |
| 3.2 | Módulo de poblaciones específicas (embarazo, patologías concretas) | Entrenamiento | ⏸️ |
| 3.3 | Módulo de poblaciones específicas (embarazo, patologías concretas) | Nutrición | ⏸️ |

---

## 4. Mejoras opcionales no bloqueantes

Anotadas para no perderlas, pero ninguna es un hueco crítico hoy — el diseño actual (Human-in-the-Loop) ya cubre el riesgo que resolverían.

| # | Tarea | Estado | Nota |
|---|---|---|---|
| 4.1 | `programs:check-integrity` inmediato tras cada import real, no solo cron semanal | 🟢 (en `main`) | **(2026-09-16) Fusionado a `main`.** `--check-integrity` (CLI) / `check_integrity` (HTTP), opcional y retrocompatible. **(2026-09-17)** Ejecutado standalone (sin `--fix`) contra la BD real: "Sin referencias rotas. Todo correcto (207 filas revisadas)." Sigue faltando probarlo encadenado inmediatamente tras un import real (no hubo import real que disparara ninguno, ver 1.1). `Bckbs/docs/AGENTE_IMPORTADOR.md`, sección 7, punto 4 |
| 4.2 | Umbral de revisión humana configurable por nivel de confianza (hoy `review_required` ya separa A/B de C/D/E, pero la pausa la impone el LLM siguiendo el system-prompt, no la CLI) | 🟢 (en `main`) | **(2026-09-16) Fusionado a `main`.** `--confidence-gate` (CLI) / `confidence_gate` (HTTP): antes de un import real, corre un dry-run en memoria y aborta sin escribir si hay ejercicios sin revisar. 10 tests contra MySQL real local. **(2026-09-17)** Probado contra el VPS real con el flag activo, pero sin efecto observable — el único catálogo disponible ya estaba importado y el flujo corta antes de llegar a la lógica de gate. Sigue sin confirmarse con un caso real de match ambiguo (ver 1.1). `Bckbs/docs/AGENTE_IMPORTADOR.md`, sección 7, punto 5 |
| 4.3 | Comando/endpoint de importación de planes de nutrición a Bckbs (análogo a `programs:import`) | 🟢 (depende de 1.2) | `BRIEF_registro_alergias_intolerancias.md`, sección 6 ("fuera de alcance") — no hace falta hoy porque el Productor de nutrición ya escribe directo vía la API existente (`formato-salida/entrega-bckbs.md`) |

---

## Ya resuelto (referencia, no acción)

- Los cinco bloqueantes originales del Agente Importador de Programas (`--json`, endpoint HTTP, `programs:assign-client`, `check-integrity` en cron, `review_required`).
- Formato de salida y recetario real del Asistente de Nutrición — la API de Bckbs (`meal_plan_templates`/`daily_plan_recipes`, `recipe-filter-list`) ya existía, no hizo falta construir nada nuevo.
- Deep search de contenido científico del Asistente de Nutrición: necesidades energéticas/macros, timing, recomposición corporal, superávit de ganancia muscular, rendimiento deportivo/resistencia, y evidencia clínica de alergias/intolerancias.
- **(2026-09-16) Cribado de seguridad faltante en el onboarding real** — `par_q_answers` no preguntaba embarazo/posibilidad, alteración menstrual/fractura por estrés (RED-S) ni trastorno alimentario, pese a que `contraindicaciones-medicas.md` lo asumía desde el diseño. Añadido a Bckbs (migración + validación + flag de revisión + tests).
- **(2026-09-16) `disponibilidad_cocina` en el onboarding de nutrición** — requerido por el esquema desde el primer borrador, nunca se preguntaba. Añadido a Bckbs.
- **(2026-09-16) Disponibilidad de entrenamiento editable post-onboarding** — nuevo endpoint `POST training-availability-update`, sin repetir todo el cuestionario.
- **(2026-09-17) Integración en la app de los tres cambios de onboarding** — el usuario confirmó que ya está integrado: las preguntas de embarazo/RED-S se muestran solo a perfil mujer, disponibilidad de cocina añadida a la etapa 4, y la pantalla de disponibilidad de entrenamiento editable. La PR `feature/onboarding-safety-and-preferences` de Bckbs está fusionada a `main` (verificado: 59 tests relevantes en verde, sin conflicto con el trabajo de otras sesiones — Panel de Tareas, readiness-scores).
- **(2026-09-17) 1.2 — severidad de alergias/intolerancias, confirmada en producción.** Verificado con acceso SSH real al VPS: migración `2026_09_16_090000_add_severity_to_client_limitations_table` en estado `Ran` (batch 36), columna `severity` presente en `client_limitations` (`SHOW COLUMNS`), `type` ampliado a `injury,limitation,medical_condition,allergy,intolerance,aversion,ethical_religious_preference`, `severity` restringido a `mild,moderate,severe_anaphylaxis`, y el controlador (`ClientLimitationController::store`/`update`) devuelve 422 si `type=allergy` sin `severity`. Esta tabla decía que seguía bloqueada pendiente de aplicar en el VPS — no era así, ya estaba aplicada (probablemente junto con el trabajo de integración de onboarding). Queda solo la parte humana (2.3).
- **(2026-09-17) 2.6 — ubicación de la memoria real por cliente, decidida.** El usuario confirmó que los campos de memoria (`observaciones_coach`, `razonamiento`, etc.) deben ser editables a mano, lo que descartó una tabla en Bckbs; entre repo privado de GitHub y Google Sheets, eligió el repo por no requerir integrar la API de Google antes de M1. Creado **`ilzarpeatore/bstronger-memoria-clientes`** (privado), con `clientes/<cliente_id>/` (`perfil-cliente.json`, `perfil-nutricional.json`, `checkpoints-fisicos.json`, `log-registro.json`, `log-nutricion.json`) y una plantilla en `_plantilla/`. Ambos `system-prompt.md` actualizados (entrenamiento v0.11.1, nutrición v0.6.1) con la ruta exacta. Sigue sin datos reales de ningún cliente todavía — la carpeta `clientes/` está vacía a propósito.
- **(2026-09-17) 2.7 — capa de "hábitos prioritarios", construida.** El usuario decidió construirla ya (caso real de Borja + práctica recurrente) y que viviera solo en el agente de nutrición (de los 5 hábitos del caso real, 3 eran nutricionales y 2 de estilo de vida, ninguno de programación de ejercicio). Nuevo módulo `agentes/programacion-nutricion/modulos/habitos-prioritarios.md` (siempre activo, tras fijar el plan) y nuevo campo `habitos_prioritarios` en `esquemas/log-nutricion.schema.json`. `system-prompt.md` de nutrición sube a v0.7.0.

---

## Nota (2026-09-16): entorno de pruebas local real

Esta sesión instaló MariaDB local (no Docker, no disponible en el sandbox) y corrió la suite completa de migraciones de Bckbs contra un esquema MySQL real — a diferencia de SQLite, que falla en una migración con sintaxis `ALTER TABLE ... MODIFY` específica de MySQL. Esto permite construir Y probar con tests de verdad cualquier cambio de código (migraciones, modelos, controladores) sin acceso al VPS, dejando solo "aplicarlo en producción" como el paso realmente bloqueado.

1.2, 4.1 y 4.2 se construyeron, probaron (19 tests nuevos en total, MySQL real local) y fusionaron a `main` de Bckbs en dos ramas (`feature/client-limitation-severity`, `feature/import-confidence-gate-check-integrity`), sin conflicto con trabajo de otra sesión que había avanzado `main` mientras tanto. Lo único que sigue bloqueado de verdad es la confirmación contra el VPS real (1.1, y para 1.2 además la migración de producción).

## Mantenimiento de este documento

- Cuando una tarea se resuelva, muévela a "Ya resuelto" con la fecha, no la borres — mismo criterio que los changelogs de cada agente.
- Si aparece una tarea nueva, añádela aquí primero — no crear un nuevo documento de pendientes suelto en otro sitio del repo.
- `docs/roadmap.md` y los `CHANGELOG.md` de cada agente siguen siendo la fuente de verdad de arquitectura e historial de cambios respectivamente; este documento es solo el estado actual de qué queda por hacer.
