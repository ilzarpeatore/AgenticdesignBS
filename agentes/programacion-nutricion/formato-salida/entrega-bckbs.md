# Formato de entrega real hacia Bckbs

Este documento describe cómo el borrador aprobado del Asistente de Programación de Nutrición se traduce en datos reales dentro de `ilzarpeatore/Bckbs` — el análogo, para nutrición, de `agentes/programacion-entrenamiento/formato-salida/formato-excel.md`.

**A diferencia del agente de entrenamiento, aquí no hace falta construir nada nuevo del lado del backend.** Al revisar el código de Bckbs (solo lectura, sin acceso a la BD) se encontró que la API completa ya existe y está en producción — el trabajo pendiente es que el agente la use bien, no que alguien la construya.

## 1. Cadena de datos (ya existe, no se toca)

```
meal_plan_templates          ← plantilla de plan de comidas (título, type: sequential|weekday)
  └─ meal_plan_template_items ← 1 fila por (día, tipo de comida): day_key, meal_type, recipe_id
                                  + calories/protein/fats/carbs (copiados de la receta al añadir el item)

daily_plans                  ← plan real de un cliente en una fecha concreta (user_id, date, objetivos del día)
  └─ daily_plan_recipes      ← receta asignada a una comida de ese día real
```

`meal_plan_templates.type`:
- **`sequential`**: "Día 0", "Día 1"... sin longitud fija — para un plan de N días que no se repite semana a semana.
- **`weekday`**: "monday".."sunday" — se repite cada semana. Usa esto por defecto salvo que el cliente tenga un patrón que varíe semana a semana (más parecido a la periodización por evento del agente de entrenamiento, que si aplica no debería mapearse a `weekday`).

## 2. Endpoints reales (todos bajo el grupo `auth:sanctum`, mismo patrón que `training-program-*`)

| Endpoint | Para qué |
|---|---|
| `GET recipe-filter-list` | Buscar recetas — soporta `title`, `meal_type[]`, `recipe_category_ids[]`, `recipe_tag_ids[]`, `start_calories`/`end_calories`, `start_protein`/`end_protein`, `start_carbs`/`end_carbs`, `start_fats`/`end_fats`, `min_preparation_time`/`max_preparation_time`. Es el recetario real (Paso 2, punto 4 del `system-prompt.md`) — permite buscar "una receta de desayuno entre 400-500 kcal y ≥30g de proteína", no solo por nombre. |
| `GET recipe-detail/{id}` | Ficha completa de una receta: ingredientes (`recipeIngredients`, cada uno con `ingredient_id` y macros), pasos, categorías, tags. Necesario para verificar ingrediente a ingrediente contra las exclusiones de `alergias-intolerancias.md` — ver limitación en sección 4. |
| `POST meal-plan-templates` | Crear la plantilla del plan (`title`, `type`). |
| `POST meal-plan-templates/{id}/items` | Añadir una comida a un día (`day_key`, `meal_type` — uno de `breakfast`/`lunch`/`dinner`/`snacks`, `recipe_id`). Repetir por cada comida del plan. |
| `POST meal-plan-templates/{id}/import-to-calendar` | Asignar la plantilla ya construida al calendario real de un cliente (`client_id`, `start_date`, `weeks` si es `weekday`) — crea `daily_plans`/`daily_plan_recipes` reales y notifica al cliente. Es el análogo exacto de `programs:assign-client`/`POST training-program-assign-client` del agente de entrenamiento. |
| `GET client-limitation-list?client_id=X&type=allergy` (y `intolerance`/`aversion`/`ethical_religious_preference` una vez existan, ver más abajo) | Cribado de seguridad — Paso 1, apartado 0. |

No hace falta construir un comando artisan nuevo tipo `programs:import`: el flujo completo (crear plantilla → añadir items → asignar a calendario) ya es HTTP, con el mismo token de coach que usa el resto del panel.

## 3. Flujo del Productor (Paso 2) usando estos endpoints

1. Calcula el objetivo calórico/macros del cliente (`necesidades-energeticas-macronutrientes.md`) y decide `day_key`/`meal_type` por día según `timing-nutricional-entrenamiento.md`.
2. Para cada comida: busca en `GET recipe-filter-list` con los rangos de macros que le corresponden a esa comida (no busques por nombre exacto de memoria — usa los filtros de calorías/macros reales, es lo que los distingue de una búsqueda de texto simple).
3. Antes de fijar una receta candidata, pide `GET recipe-detail/{id}` y revisa `recipeIngredients` contra las exclusiones del cribado de alergias (Paso 1, apartado 0) — ver limitación de la sección 4, hoy es una revisión manual del texto de cada ingrediente, no un filtro automático.
4. Documenta en el razonamiento (Paso 2, punto 4 del `system-prompt.md`): qué se buscó, qué filtros se usaron, qué receta se eligió y por qué, igual que el agente de entrenamiento documenta la búsqueda en el catálogo de ejercicios.
5. Solo tras la aprobación humana (Paso 5): crear la plantilla (`POST meal-plan-templates`), añadir cada item (`POST .../items`), y asignar al cliente (`POST .../import-to-calendar`).

## 4. Limitación real, no resuelta todavía: sin etiquetado de alérgenos por ingrediente

`ingredients` no tiene ninguna columna de alérgenos (`contiene_gluten`, `contiene_frutos_secos`, etc.) — la única forma de comprobar una alergia hoy es que el Productor (o un humano) lea el título de cada ingrediente en `recipe-detail/{id}` y lo compare a ojo con la exclusión. **Esto es un guardrail más débil de lo que exige `alergias-intolerancias.md` para `severidad: grave_anafilaxia`** (esa severidad exige comprobar también contaminación cruzada, imposible de verificar solo con títulos de ingrediente). Hasta que exista etiquetado real:

- Para alergias `leve`/`moderada`: la revisión manual de títulos de ingrediente es aceptable.
- Para `grave_anafilaxia`: el borrador debe marcarse **siempre** para revisión humana explícita antes de asignar al calendario (ya lo exige el módulo de todos modos), y el humano debe verificar la receta por su cuenta, no confiar en que el Productor ya lo comprobó de forma fiable.

Ver también el encargo `BRIEF_registro_alergias_intolerancias.md` (entregado aparte) para el registro estructurado de severidad — el etiquetado de alérgenos por ingrediente es un encargo distinto, todavía sin escribir, que depende de este primero.

## 5. Alineación con el cálculo real de macros de la app

`app/Traits/DailyPlanTrait.php::calculateDailyPlan()` ya calcula BMR con Mifflin-St Jeor (coincide con `necesidades-energeticas-macronutrientes.md`, sección 1) y aplica:

- **Actividad** (`config('macro-nutrient.ACTIVITY_LEVEL')`): sedentary ×1.2, lightly_active ×1.375, moderate ×1.55, very_active ×1.725, athlete ×1.9.
- **Objetivo** (`config('macro-nutrient.FITNESS_GOAL')`): variación porcentual sobre el TDEE, no kcal absolutas — mantenimiento 0%, pérdida -10/-20/-40%, ganancia +10/+20/+40%.
- **Reparto de macros** (`config('macro-nutrient.MACRO_RATIO')`): presets en % de calorías (`balanced` 40/30/30 carbs/proteína/grasa, `low_fat` 40/40/20, `high_protein` 20/50/30, `high_carb` 55/25/20, `keto` 5/25/70), o `macro_type: custom` con `protein_pct`/`carbs_pct`/`fat_pct` explícitos.
- **Tolerancia:** cada macro objetivo ya se acompaña de un rango ±10% (`from`/`to`) — es el mismo criterio que debe usar el validador determinista (Paso 3) para decidir si un día está "dentro de objetivo".

**Importante para `recomposicion-corporal-nutricion.md`:** el déficit real que aplica la app es un **porcentaje del TDEE** (-10/-20/-40%), no una cifra fija en kcal. El guardrail de "nunca más de 500 kcal/día de déficit" (heredado de `hipertrofia-recomposicion-corporal.md` del agente de entrenamiento) hay que comprobarlo **después** de calcular qué kcal absolutas produce el porcentaje elegido para el TDEE real de ese cliente — un mismo -20% puede ser 400 kcal para un cliente sedentario y más de 700 kcal para uno muy activo. Si el preset más cercano se pasa del límite, usa `macro_type: custom` para fijar un porcentaje de calorías que sí lo respete, en vez de forzar el preset más próximo.
