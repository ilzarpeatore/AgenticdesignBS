# Changelog — Asistente de Programación de Nutrición

## v0.6.0 — 2026-09-17

Memoria persistente por cliente (mismo cambio que v0.15.0 del agente de entrenamiento, mismo caso real como origen — ver ese CHANGELOG para el detalle completo).

- Intake (Paso 1, punto 7) lee `contexto_vida` del esquema compartido de entrenamiento — un horario laboral nocturno cambia directamente cuándo se reparten las comidas, no es un dato solo relevante para el otro agente.
- Nueva sección "Memoria del cliente" en el Paso 1: lee `log-nutricion.schema.json` y el nuevo `checkpoint-fisico.schema.json` (compartido, vive en `agentes/programacion-entrenamiento/esquemas/`) antes de generar.
- Pendiente explícito, igual que en entrenamiento: la capa de "hábitos prioritarios" del caso real no tiene equivalente aquí.

## v0.5.0 — 2026-09-16

Primera reconciliación de `perfil-nutricional.schema.json` contra el onboarding real de Bckbs, posible porque el usuario confirmó que el onboarding de la app queda registrado en BD — se pudo comparar el esquema contra las columnas reales sin necesitar datos de ningún cliente.

- **`disponibilidad_cocina` (nuevo en Bckbs):** el campo era requerido por este esquema desde v0.1.0, pero `NutritionQuestionnaireAnswer` nunca lo preguntaba — sin datos de tiempo/habilidad de cocina, el Productor no podía saber si una receta de 45 minutos era viable. Añadidas `cooking_minutes_per_meal`/`cooking_skill_level`/`cooks_for_others` a Bckbs (migración + validación + tests).
- **`gustos_y_aversiones` reestructurado:** la app recoge gustos por categoría (`favorite_meats`/`favorite_fish`/`favorite_fruits_vegetables`/`favorite_combined_dishes`), no una lista genérica como asumía el esquema. Se añade también `descripcion_dia_tipo` (contexto cualitativo real, antes no capturado) y `numero_comidas_actual` junto al ya existente `numero_comidas_preferido`.
- **`system-prompt.md` (v0.5.0), Paso 2 punto 4:** se aclara explícitamente que los gustos favoritos son semillas para orientar la búsqueda del recetario, no una lista cerrada — el Productor debe aportar variedad real más allá de lo que el cliente listó de memoria en el onboarding, mientras que `alimentos_a_evitar` sigue siendo exclusión dura.

## v0.4.0 — 2026-09-15

Cierra dos de los pendientes que la sección 9 del `system-prompt.md` dejaba explícitos: contenido de rendimiento/superávit y deep-search clínico de alergias.

- **Nuevo módulo específico `rendimiento-deportivo-resistencia.md`:** carga de carbohidrato antes de eventos >90 min (8-12 g/kg/día, 1-3 días, coordinado con el taper de `periodizacion-orientada-evento.md` del agente de entrenamiento), fueling pre-evento (1-4 g/kg, 1-4h antes) y durante el evento (30-60 g/h desde los 60-90 min, mezclas glucosa+fructosa para tasas altas), expectativa realista de mejora (2-3%). Cross-referencia explícita con `running-economia-carrera.md` (agente de entrenamiento) y `timing-nutricional-entrenamiento.md` para no duplicar hidratación/electrolitos.
- **Nuevo módulo específico `ganancia-muscular-superavit.md`:** hasta ahora la ganancia de peso/superávit solo tenía una mención breve dentro de `recomposicion-corporal-nutricion.md` — este módulo le da lógica propia porque el dimensionamiento es inverso al de un déficit: superávit mayor para principiantes (hasta ~500 kcal/día) y menor para avanzados (200-300 kcal/día), ritmo objetivo de ganancia de peso 0.25-0.5%/semana como indicador real (no solo las kcal teóricas), proteína 1.6-2.2 g/kg y grasa 0.6-1.0 g/kg. Declarado explícitamente mutuamente excluyente con `recomposicion-corporal-nutricion.md` para un mismo bloque.
- **`alergias-intolerancias.md` (v0.2.0):** deja de estar pendiente el deep-search de evidencia clínica declarado en v0.1.0. Incorpora la lista de nueve alérgenos mayores FDA/NIAID (incluido sésamo desde 2023), reglas prácticas de contaminación cruzada para severidad grave (utensilios, orden de preparación, almacenamiento), síndrome de alergia oral/reactividad cruzada polen-alimento (abedul↔manzana/fruta de hueso, ambrosía↔plátano/melón/calabacín/pepino) y fuentes ocultas de alérgenos (lecitina de soja, derivados de trigo en salsas/rebozados).
- **"Poblaciones específicas" sigue pospuesto** (embarazo, patologías) — mismo criterio de no escribir por completitud especulativa que ya se aplicó en el agente de entrenamiento; se retoma solo si aparece un cliente real que lo necesite.
- **`system-prompt.md` (v0.4.0)** y `docs/roadmap.md`: índice de módulos e histórico actualizados.

## v0.3.0 — 2026-09-15

Trabajo que se podía hacer sin acceso a BD/VPS, mientras se resuelve por otra vía el registro estructurado de alergias (ver `BRIEF_registro_alergias_intolerancias.md`, entregado al usuario).

- **`formato-salida/entrega-bckbs.md` (nuevo):** al revisar Bckbs (solo lectura) se encontró que la API real de nutrición ya existe completa y en producción — `recipes`/`ingredients` (catálogo, con `Recipe::scopeRecipeFilter` filtrando por macros/categoría/tiempo de preparación), `meal_plan_templates`/`meal_plan_template_items` (plantilla reutilizable, análogo de `workout_templates`), `daily_plans`/`daily_plan_recipes` (asignación real al calendario del cliente, análogo de `program_day_assignments`), todo vía endpoints HTTP ya wireados (`recipe-filter-list`, `recipe-detail/{id}`, `meal-plan-templates`, `.../items`, `.../import-to-calendar`). No hizo falta construir nada nuevo del lado del backend — a diferencia del agente de entrenamiento, aquí el "formato de salida real" ya estaba resuelto sin saberlo.
- **`necesidades-energeticas-macronutrientes.md` (v0.2.0) y `recomposicion-corporal-nutricion.md` (v0.2.0):** reconciliados con la implementación real de Bckbs (`app/Traits/DailyPlanTrait.php`) — Mifflin-St Jeor confirmado como lo que ya usa producción, y el déficit/superávit es un % del TDEE (`FITNESS_GOAL`), no kcal fijas como se había escrito inicialmente. El guardrail de "nunca >500 kcal/día" ahora se comprueba sobre el resultado en kcal absolutas del preset elegido, no sobre el porcentaje.
- **`esquemas/log-nutricion.schema.json` (nuevo):** memoria episódica, mismo patrón que `log-registro.schema.json` del agente de entrenamiento (incluido el campo `razonamiento` obligatorio desde el primer día, sin repetir el hueco que ese agente tuvo que cerrar después).
- **`validador/validar_plan.py` (nuevo, Paso 3):** código real, no prosa. Comprueba severidad obligatoria en alergias, cribado de alérgenos por ingrediente (limitación documentada: solo coincidencia de texto, Bckbs no etiqueta alérgenos todavía), estructura de items, y tolerancia de macros diarios (±10%, la misma banda que ya usa `DailyPlanTrait::calculateDailyPlan()`). 16 tests — con fixtures sintéticos, declarado explícitamente que no hay todavía un caso real de cliente como el de Toni para este agente.
- **`system-prompt.md` (v0.3.0):** Paso 2 punto 4, Paso 6 y Paso 7 actualizados con los endpoints reales; sección 9 ya no lista el recetario ni el formato de salida como pendientes.

## v0.2.0 — 2026-09-15

Deep search basado en ciencia para las tres piezas de contenido más básicas, siguiendo el proceso de `CONTRIBUTING.md` (evidencia convertida a regla operativa, no cita narrativa).

- **Nuevo módulo general `necesidades-energeticas-macronutrientes.md`:** estimación de TDEE (Mifflin-St Jeor + factor de actividad), rangos de proteína por contexto (ISSN Position Stand: 1.4-2.0 g/kg general, 1.6-2.0 fuerza, 1.0-1.6 resistencia, 2.3-3.1 en déficit), mínimo de grasa por salud hormonal (0.5-1 g/kg, ≥20% calorías), carbohidrato por diferencia, y el umbral de seguridad de disponibilidad energética (RED-S: <30 kcal/kg de masa libre de grasa/día = baja disponibilidad) como guardrail duro para cualquier déficit. Nota breve sobre micronutrientes de riesgo (hierro, vitamina D, calcio, fibra) como señal de alerta, no diagnóstico.
- **Nuevo módulo general `timing-nutricional-entrenamiento.md`:** desmonta el mito de la "ventana anabólica" estrecha (Aragon & Schoenfeld 2013: ventana real de 4-6h, el total diario de proteína domina sobre el timing exacto), distribución de proteína por toma (~0.4 g/kg, mínimo ~0.25 g/kg para estímulo relevante), periodización simple de carbohidrato por tipo de día (entrenamiento vs. descanso, coordinado con lo que el agente de entrenamiento indique para esa semana), e hidratación (ACSM: pre/durante/electrolitos).
- **Nuevo módulo específico `recomposicion-corporal-nutricion.md`:** implementación numérica de lo que `hipertrofia-recomposicion-corporal.md` (agente de entrenamiento) ya usa como referencia — tamaño de déficit (300-500 kcal/día), proteína en déficit (2.3-3.1 g/kg), estructura práctica de diet breaks (1-2 semanas a mantenimiento recalculado al peso actual, cada 4-10 semanas) y refeeds (1-3 días, +carbohidrato, cada 7-14 días), coordinados con el deload de entrenamiento. Cross-referencia explícita en vez de duplicar cifras ya fijadas del lado de entrenamiento.
- **`system-prompt.md` (v0.2.0):** sección 9 actualizada para reflejar el estado real de contenido — ya no dice "solo existe la capa de seguridad".

## v0.1.0 — 2026-09-15

Primer borrador. Mismo marco arquitectónico que `agentes/programacion-entrenamiento/` (base de conocimiento modular, sin encasillar al cliente en una dieta fija), adaptado a nutrición y coordinado con el entrenamiento real del cliente.

- **Nuevo `system-prompt.md`:** rol y alcance (qué NO decide: ni entrenamiento, ni diagnóstico, ni suplementación de riesgo), Paso 0 (selección de módulos multi-etiqueta), Paso 1 con cribado de alergias obligatorio primero y coordinación explícita con el Asistente de Programación de Entrenamiento (Multi-Agent Collaboration — sequential handoff, cap. 7: lee `perfil-cliente.schema.json` y el razonamiento del Productor de ese agente en vez de regenerar el entrenamiento), Paso 2 con razonamiento CoT + consulta de recetario (Tool Use, cap. 5, pendiente de recetario real), jerarquía universal de conflictos, y una sección 9 explícita de lo que todavía no existe (recetario real, formato de salida real, validador determinista, log de nutrición) para no fingir que está resuelto.
- **Nuevo módulo `alergias-intolerancias.md`:** primer módulo real, capa de seguridad transversal. Aplica directamente la lección del intake de lesiones del otro agente (bloqueo duro ante datos de seguridad ambiguos, no una nota a mejorar después) — esta vez desde el primer borrador, no tras un incidente real. Sin deep-search de evidencia clínica todavía, declarado explícitamente como pendiente.
- **`agentes/programacion-entrenamiento/esquemas/perfil-cliente.schema.json` (v0.9.0 de ese agente):** `restricciones_dieteticas` pasa de lista de texto libre a objetos estructurados con `tipo` y `severidad` obligatoria si `tipo: alergia` — mismo patrón que `restricciones_salud`, para que el campo compartido llegue ya bien formado a este agente en vez de heredar la ambigüedad.
- **Nuevo `esquemas/perfil-nutricional.schema.json`:** solo los campos que no viven ya en el esquema compartido (objetivos nutricionales, gustos/aversiones, disponibilidad para cocinar, presupuesto, nº de comidas) — no duplica `cliente_id`, `restricciones_dieteticas` ni `disponibilidad`/`actividad_principal` de entrenamiento.

**Pendiente (declarado en la sección 9 del `system-prompt.md`, no oculto):**
- Recetario real contra el que el Paso 2 pueda buscar (equivalente a `catalogo-ejercicios.xlsx`).
- Formato de salida real hacia algún sistema de producción — no existe todavía, se define cuando haya un caso real que lo necesite.
- Validador determinista (Paso 3) — por ahora la checklist mecánica es prosa, igual que le pasó al agente de entrenamiento antes de `validador/validar_programa.py`.
- Deep-search de evidencia real para módulos de contenido (macros, timing, recomposición nutricional) — todavía no se ha escrito ninguno más allá de la capa de seguridad.
