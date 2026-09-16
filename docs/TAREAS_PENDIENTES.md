# Tareas pendientes — sistema de agentes (consolidado)

> Único documento de tareas del proyecto. Antes esto vivía repartido entre `docs/roadmap.md` (sección "Backlog abierto"), `AGENTE_IMPORTADOR.md` en Bckbs y un encargo aparte (`BRIEF_registro_alergias_intolerancias.md`) — se consolida aquí para no mantener la misma tarea descrita en varios sitios a la vez. `roadmap.md` sigue siendo el documento de arquitectura/diseño; este es el documento de seguimiento de trabajo pendiente.
>
> **Última actualización:** 2026-09-16 (reconciliación de los esquemas contra el onboarding real de Bckbs)

## Cómo leer esta tabla

| Columna | Significado |
|---|---|
| Estado | 🔒 Bloqueada (no se puede avanzar desde esta sesión) · 🟡 Requiere el usuario (dato/decisión que solo puede dar él) · ⏸️ Pospuesta a propósito (no se escribe por completitud especulativa) · 🟢 Mejora opcional (no bloqueante) |
| Bloqueador | Qué hace falta exactamente para desbloquearla |

---

## 1. Bloqueadas por acceso a BD/VPS real (`bestronger-vps`)

Ninguna de estas tres se puede ejecutar desde esta sesión — no hay red hacia el VPS de producción (confirmado con un test de conectividad real, no solo asumido). Requieren una sesión de Claude Code con acceso al VPS, o que el usuario las ejecute/facilite el acceso.

| # | Tarea | Estado | Bloqueador | Detalle completo |
|---|---|---|---|---|
| 1.1 | Verificar contra BD real todo lo mergeado a `main` de Bckbs (`--json`, `programs:assign-client`, `POST program-import`, hotfix `fail()`→`reportFailure()`, y ahora también `--confidence-gate`/`--check-integrity`, ver 4.1/4.2) | 🔒 | Acceso a datos del VPS `bestronger-vps` | `Bckbs/docs/AGENTE_IMPORTADOR.md`, sección "Tarea pendiente" |
| 1.2 | Construir el registro estructurado de severidad de alergias/intolerancias en Bckbs (`client_limitations`: columna `severity`, ampliar `type`, validación 422 si `type=allergy` sin `severity`, tests) | 🔒 (parcial — código en `main`) | **(2026-09-16) Fusionado a `main`** (migración + modelo + validación + 9 tests, probado contra un esquema MySQL real local). Falta: aplicar la migración en el VPS de producción, y la revisión humana de qué filas migrar a mano (sección 5 del BRIEF) — eso sigue requiriendo acceso al VPS | `BRIEF_registro_alergias_intolerancias.md` |
| 1.3 | Etiquetado de alérgenos por ingrediente/receta en Bckbs (`ingredients`/`recipes` no tienen columna tipo `contiene_gluten`) | 🔒 | Depende de 1.2 (no tiene sentido etiquetar ingredientes si todavía no hay severidad estructurada que consultar) | `agentes/programacion-nutricion/formato-salida/entrega-bckbs.md`, sección 4 (limitación documentada); `BRIEF_registro_alergias_intolerancias.md`, sección 6 ("fuera de alcance") |

---

## 2. Bloqueadas por datos o decisión del usuario (no técnicas)

| # | Tarea | Estado | Bloqueador | Detalle completo |
|---|---|---|---|---|
| 2.1 | Definir `perfil-cliente.schema.json`/`perfil-nutricional.schema.json` con datos reales de clientes actuales | 🟡 (parcial) | **(2026-09-16) La estructura ya se reconcilió** contra las columnas reales del onboarding (`par_q_answers`/`training_questionnaire_answers`/`nutrition_questionnaire_answers`) sin necesitar datos de ningún cliente — el usuario confirmó que el onboarding real queda en BD, así que se comparó el esquema contra el schema de esas tablas directamente. Queda pendiente contrastar con VALORES reales (no solo la forma) de 2-3 clientes actuales, para detectar patrones que la estructura por sí sola no revela | `agentes/programacion-entrenamiento/esquemas/perfil-cliente.schema.json`, `agentes/programacion-nutricion/esquemas/perfil-nutricional.schema.json` |
| 2.2 | Caso real de cliente de principio a fin para el Asistente de Nutrición (equivalente al caso de Toni en entrenamiento) | 🟡 | El usuario tiene que aportar uno de los recetarios por cliente que ya construye a mano | `agentes/programacion-nutricion/validador/README.md` (fixtures hoy sintéticos, sin caso real) |
| 2.3 | Migrar a `client_limitations` las alergias que hoy solo existen como texto libre en `nutrition_questionnaire_answers.allergies_intolerances` | 🟡 (tras 1.2) | Es tarea humana a propósito — un parseo automático de texto libre no puede inferir severidad de forma fiable, así que no se automatiza | `BRIEF_registro_alergias_intolerancias.md`, sección 5 |
| 2.4 | Confirmar o ajustar la regla de derivación de `nivel_fuerza` (principiante/intermedio/avanzado) a partir de `experiencia_meses`/`tecnica_autoevaluada` | 🟡 | Es un criterio de coach, no algo que se pueda derivar solo de la estructura de datos — la regla propuesta (2026-09-16) es un punto de partida, no una decisión final | `agentes/programacion-entrenamiento/esquemas/perfil-cliente.schema.json`, campo `experiencia_entrenamiento.nivel_fuerza` |
| 2.5 | Decidir qué hacer con clientes que completaron el onboarding antes del 2026-09-16 — se quedan con `parq_pregnant_or_possible`/`parq_menstrual_change_or_stress_fracture`/`parq_eating_disorder_history`/`disponibilidad_cocina` a `NULL` para siempre salvo que se les vuelva a preguntar | 🟡 | Decisión de producto (¿re-prompt en la app a los clientes existentes? ¿se asume el hueco hasta el próximo ciclo de cada uno?), no algo que el código pueda resolver solo | `Bckbs`, migraciones `2026_09_16_100000`/`2026_09_16_100001` |

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
| 4.1 | `programs:check-integrity` inmediato tras cada import real, no solo cron semanal | 🟢 (en `main`) | **(2026-09-16) Fusionado a `main`.** `--check-integrity` (CLI) / `check_integrity` (HTTP), opcional y retrocompatible. Falta ejercitarlo una vez contra un import real en el VPS (se hará junto con 1.1). `Bckbs/docs/AGENTE_IMPORTADOR.md`, sección 7, punto 4 |
| 4.2 | Umbral de revisión humana configurable por nivel de confianza (hoy `review_required` ya separa A/B de C/D/E, pero la pausa la impone el LLM siguiendo el system-prompt, no la CLI) | 🟢 (en `main`) | **(2026-09-16) Fusionado a `main`.** `--confidence-gate` (CLI) / `confidence_gate` (HTTP): antes de un import real, corre un dry-run en memoria y aborta sin escribir si hay ejercicios sin revisar. 10 tests contra MySQL real local; falta confirmarlo contra el catálogo real del VPS (junto con 1.1). `Bckbs/docs/AGENTE_IMPORTADOR.md`, sección 7, punto 5 |
| 4.3 | Comando/endpoint de importación de planes de nutrición a Bckbs (análogo a `programs:import`) | 🟢 (depende de 1.2) | `BRIEF_registro_alergias_intolerancias.md`, sección 6 ("fuera de alcance") — no hace falta hoy porque el Productor de nutrición ya escribe directo vía la API existente (`formato-salida/entrega-bckbs.md`) |

---

## Ya resuelto (referencia, no acción)

- Los cinco bloqueantes originales del Agente Importador de Programas (`--json`, endpoint HTTP, `programs:assign-client`, `check-integrity` en cron, `review_required`).
- Formato de salida y recetario real del Asistente de Nutrición — la API de Bckbs (`meal_plan_templates`/`daily_plan_recipes`, `recipe-filter-list`) ya existía, no hizo falta construir nada nuevo.
- Deep search de contenido científico del Asistente de Nutrición: necesidades energéticas/macros, timing, recomposición corporal, superávit de ganancia muscular, rendimiento deportivo/resistencia, y evidencia clínica de alergias/intolerancias.
- **(2026-09-16) Cribado de seguridad faltante en el onboarding real** — `par_q_answers` no preguntaba embarazo/posibilidad, alteración menstrual/fractura por estrés (RED-S) ni trastorno alimentario, pese a que `contraindicaciones-medicas.md` lo asumía desde el diseño. Añadido a Bckbs (migración + validación + flag de revisión + tests).
- **(2026-09-16) `disponibilidad_cocina` en el onboarding de nutrición** — requerido por el esquema desde el primer borrador, nunca se preguntaba. Añadido a Bckbs.
- **(2026-09-16) Disponibilidad de entrenamiento editable post-onboarding** — nuevo endpoint `POST training-availability-update`, sin repetir todo el cuestionario.

---

## Nota (2026-09-16): entorno de pruebas local real

Esta sesión instaló MariaDB local (no Docker, no disponible en el sandbox) y corrió la suite completa de migraciones de Bckbs contra un esquema MySQL real — a diferencia de SQLite, que falla en una migración con sintaxis `ALTER TABLE ... MODIFY` específica de MySQL. Esto permite construir Y probar con tests de verdad cualquier cambio de código (migraciones, modelos, controladores) sin acceso al VPS, dejando solo "aplicarlo en producción" como el paso realmente bloqueado.

1.2, 4.1 y 4.2 se construyeron, probaron (19 tests nuevos en total, MySQL real local) y fusionaron a `main` de Bckbs en dos ramas (`feature/client-limitation-severity`, `feature/import-confidence-gate-check-integrity`), sin conflicto con trabajo de otra sesión que había avanzado `main` mientras tanto. Lo único que sigue bloqueado de verdad es la confirmación contra el VPS real (1.1, y para 1.2 además la migración de producción).

## Mantenimiento de este documento

- Cuando una tarea se resuelva, muévela a "Ya resuelto" con la fecha, no la borres — mismo criterio que los changelogs de cada agente.
- Si aparece una tarea nueva, añádela aquí primero — no crear un nuevo documento de pendientes suelto en otro sitio del repo.
- `docs/roadmap.md` y los `CHANGELOG.md` de cada agente siguen siendo la fuente de verdad de arquitectura e historial de cambios respectivamente; este documento es solo el estado actual de qué queda por hacer.
