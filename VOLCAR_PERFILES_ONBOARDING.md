# Volcar perfiles de onboarding a la memoria real — instrucciones para consola

> Pega esto como mensaje a una sesión de Claude Code en consola con acceso SSH real a `bestronger-vps` y a los repos `Bckbs` y `bstronger-memoria-clientes`. Esta sesión sandbox no tiene esa salida de red (verificado) — por eso el volcado en sí tiene que ejecutarse desde ahí. El mapeo de abajo ya está verificado contra el código real de Bckbs (modelos/migraciones en `main`), no inventado.

## Objetivo

Antes de generar ninguna rutina o plan de nutrición, crear en `ilzarpeatore/bstronger-memoria-clientes` un `clientes/<cliente_id>/perfil-cliente.json` + `perfil-nutricional.json` **por cada cliente que ya completó el onboarding real**, poblados con sus datos reales — no plantillas vacías. Es **solo lectura contra Bckbs**: esto no escribe nada en producción, solo lee y vuelca a otro repo.

## 0. Qué usuarios procesar

Un usuario tiene onboarding completo para este propósito si existen filas en `par_q_answers` Y `training_questionnaire_answers` para su `user_id` (join 1:1 por `user_id`, ambas tablas tienen `unique('user_id')`). Si además existe fila en `nutrition_questionnaire_answers`, genera también `perfil-nutricional.json`; si no, genera solo `perfil-cliente.json` y anótalo como pendiente.

**No proceses ni inventes datos para un usuario con onboarding incompleto.** Lístalos aparte (ver sección 5).

`cliente_id` = `"<users.id>-<slug>"`, slug derivado de `first_name`/`last_name` en minúsculas sin acentos (ej. `101-borja-betanzos`). Debe ser estable — no lo cambies una vez creado.

## 1. Mapeo — `perfil-cliente.json`

| Campo del esquema | Fuente real (Bckbs) | Nota |
|---|---|---|
| `cliente_id` | `users.id` + slug | — |
| `genero` | `users.gender` | Valores reales `male`/`female`/`other` → traduce a `hombre`/`mujer`/`otro`. `null` si no está. |
| `cribado_medico.parq_*` (7 campos booleanos) | `par_q_answers.parq_heart_condition`, `parq_chest_pain_activity`, `parq_chest_pain_rest_last_month`, `parq_dizziness_balance`, `parq_bone_joint_problem`, `parq_bp_or_heart_medication`, `parq_reason_not_to_exercise` | Copia directa. |
| `cribado_medico.parq_pregnant_or_possible` / `parq_menstrual_change_or_stress_fracture` | mismas columnas | Si `genero` es `hombre`/`otro` y el valor es `null` → correcto, no aplica, no lo marques como pendiente. Si `genero` es `mujer` y es `null` → onboarding anterior al 2026-09-16, **márcalo como pendiente de preguntar** (no lo dejes `null` sin más). |
| `cribado_medico.parq_eating_disorder_history` | misma columna | `null` en cualquier género → pendiente de preguntar (onboarding anterior al 2026-09-16). |
| `cribado_medico.parq_medical_history` | `par_q_answers.parq_medical_history` | Texto libre, copia tal cual. |
| `cribado_medico.resultado` | **Derivar, no copiar** — ver sección 2 | No hay columna directa. |
| `objetivos[0].categoria` | `training_questionnaire_answers.goal_type` (`lose_fat`/`gain_muscle`/`recomposition`/`maintain`) | Traduce a categoría en español si quieres homogeneidad con el resto del esquema (ej. `recomposicion_corporal`), o deja el valor real — no hay una traducción ya decidida, usa criterio y sé consistente entre todos los clientes. |
| `objetivos[0].detalle` | `training_questionnaire_answers.realistic_goal` (texto libre) | — |
| `experiencia_entrenamiento.experiencia_meses` | `training_questionnaire_answers.training_experience_months_coach ?? training_experience_months` | Usa el valor "efectivo" — mismo criterio que `TrainingQuestionnaireAnswer::effectiveExperienceMonths()`. |
| `experiencia_entrenamiento.tecnica_autoevaluada` | `technique_level_coach ?? technique_level` | Igual, `effectiveTechniqueLevel()`. |
| `experiencia_entrenamiento.nivel_fuerza` | **Derivar con la regla provisional** (ver `esquemas/perfil-cliente.schema.json`, campo `nivel_fuerza`: avanzado si meses≥36 y técnica≥7; principiante si meses<12 o técnica≤3; intermedio el resto) | Es una regla **pendiente de confirmar por el usuario (ítem 2.4)**, no definitiva. Aplícala pero añade `"_provisional": ["nivel_fuerza pendiente de confirmar, ver 2.4"]` en el perfil — no la presentes como decidida. |
| `disponibilidad.dias_por_semana` | `training_questionnaire_answers.training_days_per_week` | — |
| `disponibilidad.duracion_sesion_preferida` | `session_duration_preference` | Ya viene como `"30"`/`"45"`/`"60"`/`"90"`/`"90_plus"`, coincide con el enum del esquema. |
| `restricciones_salud` | `client_limitations` donde `client_id = user.id` y `type` en (`injury`,`limitation`,`medical_condition`) | El esquema pide campos granulares (`gesto_doloroso`, `fase`, `empeora_con_actividad_o_impacto`, `autorizacion_profesional`) que **no existen en `client_limitations`** — vuelca lo que haya (`title`/`description`) como `descripcion` y deja el resto para el archivo manual del coach. Añádelo a `_pendiente_revision_coach` si hay alguna fila aquí. |
| `restricciones_dieteticas` | `client_limitations` donde `type` en (`allergy`,`intolerance`,`aversion`,`ethical_religious_preference`) | Si no hay fila estructurada pero `nutrition_questionnaire_answers.allergies_intolerances` tiene texto real (no "ninguna"), vuelca ese texto en `descripcion` con `tipo` sin decidir la severidad — márcalo en `_pendiente_revision_coach` (mismo caso que Toni/Borja, ítem 2.3). **Nunca inventes `severidad`.** |
| `actividad_principal`, `contexto_vida`, `material_disponible`, `preferencias`, `referencias_carga` | Sin fuente en el onboarding real | Deja los valores por defecto de la plantilla (`_plantilla/perfil-cliente.json`) y añade `"_pendiente_manual": ["contexto_vida", "actividad_principal", ...]` — esto es justo lo que rellenará el archivo que el usuario va a entregar por cliente. |
| `datos_fisicos.peso_kg` / `.altura_cm` / `.edad` | `user_profiles.weight` / `.height` / `.age` (join por `user_id`, **no** por `par_q_answers`/`training_questionnaire_answers`/`nutrition_questionnaire_answers` — ninguna de las tres tiene estos campos) | **Añadido 2026-09-20** tras un caso real: sin esto el agente de nutrición no puede calcular TDEE (Mifflin-St Jeor). `user_profiles` es `nullable` y puede no existir para un usuario con onboarding v2 completo (fallo de red en `Bckbs::OnboardingController::complete()`, que no verifica esta etapa) o si la cuenta es anterior al 29-08-2026 (pantalla de registro antigua sin este paso) — en ese caso deja los tres campos `null` y añádelo a `_pendiente_manual`, no lo bloquees ni lo inventes. |
| `datos_fisicos.fecha_referencia` | `user_profiles.updated_at` (solo fecha, `YYYY-MM-DD`) | **No** uses la fecha en la que ejecutas el volcado — usa la fecha real de la fila. Si `user_profiles` no existe, deja `null` junto con los tres campos anteriores. |

## 2. Regla para `cribado_medico.resultado`

No es un cálculo mecánico simple — ver `agentes/programacion-entrenamiento/modulos/contraindicaciones-medicas.md`, secciones 2 y 3, en `AgenticdesignBS`.

- Si **todas** las respuestas booleanas relevantes son `false`/`null`-correcto (según género y fecha, ver tabla de arriba) → `"resultado": "limpio"`.
- Si **cualquiera** es `true` → **no lo clasifiques tú** como relativa/absoluta (eso exige leer `parq_medical_history` y criterio clínico) — deja `"resultado": "requiere_revision_coach"` (valor fuera del enum del esquema, a propósito, para que no se confunda con una clasificación real) y añade el motivo a `_pendiente_revision_coach`. Nunca generes un borrador de entrenamiento para estos clientes hasta que el coach clasifique el resultado real.

## 3. Mapeo — `perfil-nutricional.json`

| Campo | Fuente real | Nota |
|---|---|---|
| `cliente_id` | mismo que el perfil de entrenamiento | — |
| `objetivos_nutricionales[0].categoria` | `training_questionnaire_answers.goal_type` (mismo valor que el objetivo de entrenamiento, no hay campo nutricional separado) | Provisional — añade a `_pendiente_manual` que el coach puede matizar si el objetivo nutricional difiere del de entrenamiento. |
| `gustos_y_aversiones.favoritos_por_categoria.{carnes,pescados,frutas_y_verduras,platos_combinados}` | `nutrition_questionnaire_answers.{favorite_meats,favorite_fish,favorite_fruits_vegetables,favorite_combined_dishes}` | Copia directa, `null`→`""`. |
| `gustos_y_aversiones.alimentos_favoritos_general` | `liked_foods` | — |
| `gustos_y_aversiones.alimentos_a_evitar` | `disliked_foods` | — |
| `gustos_y_aversiones.descripcion_dia_tipo` | `typical_day_meals` | — |
| `disponibilidad_cocina.minutos_por_comida` | `cooking_minutes_per_meal` | Puede ser `null` si el onboarding es anterior al 2026-09-16 (ítem 2.5) — márcalo pendiente, no inventes un valor. |
| `disponibilidad_cocina.nivel_habilidad` | `cooking_skill_level` (`beginner`/`intermediate`/`advanced`) | Traduce a `principiante`/`intermedio`/`avanzado`. |
| `disponibilidad_cocina.cocina_para_mas_personas` | `cooks_for_others` | — |
| `numero_comidas_preferido` / `numero_comidas_actual` | `desired_meals_per_day` / `current_meals_per_day` | — |

`presupuesto`, `estilo_culinario`, `referencias_actuales`: sin fuente real, dejar vacío/`_pendiente_manual`.

## 4. Proceso paso a paso

1. Query de solo lectura contra la BD real: todos los `user_id` con fila en `par_q_answers` y `training_questionnaire_answers` (join, no dos queries sueltas que puedan desincronizarse). Añade un LEFT JOIN a `user_profiles` en la misma query para `datos_fisicos` — es opcional (puede no existir, ver tabla de arriba), por eso LEFT JOIN y no INNER JOIN.
2. Para cada uno, construye el JSON siguiendo las tablas de arriba, usando `_plantilla/perfil-cliente.json` y `_plantilla/perfil-nutricional.json` de `bstronger-memoria-clientes` como base de forma (no te saltes ningún campo requerido por el esquema).
3. Escribe en `clientes/<cliente_id>/perfil-cliente.json` (y `perfil-nutricional.json` si aplica) del repo `bstronger-memoria-clientes`. Si la carpeta del cliente ya existe con datos reales, no la sobrescribas sin más — compara primero, esto es un volcado inicial, no debería haber conflicto salvo que alguien ya lo hiciera a mano.
4. Repite para todos los clientes con onboarding completo.
5. Un solo commit (o uno por lote razonable, no uno por cliente) a `bstronger-memoria-clientes`, mensaje claro (ej. "volcado inicial de perfiles desde onboarding real, N clientes").

## 5. Al terminar, genera un resumen para el coach

Un archivo `clientes/_pendientes-volcado-<fecha>.md` (en `bstronger-memoria-clientes`, no en `AgenticdesignBS`) con:

- Lista de clientes procesados (cliente_id, nombre).
- Lista de clientes con onboarding **incompleto** (qué tabla les falta) — no procesados.
- Lista de clientes con `resultado: requiere_revision_coach` — necesitan que el coach lea `parq_medical_history` y clasifique.
- Lista de clientes con alergia/intolerancia en texto libre sin severidad estructurada (ítem 2.3 ampliado a todos los clientes, no solo Toni/Borja).
- Lista de clientes con campos `_pendiente_manual` (contexto_vida, actividad_principal, etc.) — son los candidatos a recibir el archivo que el usuario va a entregar por cliente.
- Lista de clientes sin `user_profiles` (o con `weight`/`height`/`age` a `null` ahí) — `datos_fisicos` queda incompleto y bloquea el cálculo de TDEE del agente de nutrición hasta que el cliente complete esa etapa del registro.

Actualiza también `docs/TAREAS_PENDIENTES.md` en `AgenticdesignBS` con una nota de que el volcado inicial se hizo, la fecha, y cuántos clientes quedaron pendientes de revisión — commit y push a ese repo también.

## Reglas que no cambian

- Nunca fabricar `severidad`, `resultado` de cribado, ni ningún campo de seguridad — mejor pendiente y explícito que inventado.
- Esto es lectura de Bckbs + escritura solo en `bstronger-memoria-clientes` — no se toca la BD de producción en ningún paso de este proceso.
- No mezclar este volcado con 1.1/2.3 (que sí requieren escribir en Bckbs) — son procesos independientes, aunque compartan el mismo acceso VPS.
