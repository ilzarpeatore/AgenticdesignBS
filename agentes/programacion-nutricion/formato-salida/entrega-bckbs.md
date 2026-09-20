# Formato de entrega real hacia Bckbs

Este documento describe cómo el borrador aprobado del Asistente de Programación de Nutrición se traduce en datos reales dentro de `ilzarpeatore/Bckbs` — el análogo, para nutrición, de `agentes/programacion-entrenamiento/formato-salida/formato-excel.md`.

**ACTUALIZADO 2026-09-20 -- cambio real que afecta a todo este documento:** el recetario local (`recipes`, `ingredients`) se vació por completo el 2026-09-19 (la nutrición de los ingredientes existentes no estaba bien calculada) y se está repoblando desde cero vía una integración nueva con **FatSecret Platform API**. Hoy mismo `recipes` tiene 0 filas -- si el Productor sigue el flujo de búsqueda original de este documento (`GET recipe-filter-list`), no encontrará nada. Ver sección 2-bis más abajo para el flujo real a partir de ahora, y `Bckbs::docs/FATSECRET_INTEGRATION.md` para el diseño completo (por qué se eligió un proxy en vivo y no importar el catálogo de FatSecret de forma permanente, límites legales de su API, etc.).

**A diferencia del agente de entrenamiento, aquí no hace falta construir nada nuevo del lado del backend.** Al revisar el código de Bckbs (solo lectura, sin acceso a la BD) se encontró que la API completa ya existía y está en producción — y ahora, tras la integración de FatSecret (2026-09-20), sigue siendo así: los endpoints nuevos ya están construidos y probados en producción, el trabajo pendiente sigue siendo que el agente los use bien.

## 1. Cadena de datos (ya existe, no se toca)

```
meal_plan_templates          ← plantilla de plan de comidas (título, type: sequential|weekday)
  └─ meal_plan_template_items ← 1 fila por (día, tipo de comida): day_key, meal_type,
                                  recipe_id (receta propia) O fatsecret_recipe_id (receta de FatSecret)
                                  -- EXACTAMENTE UNA de las dos, nunca las dos ni ninguna
                                  + calories/protein/fats/carbs (copiados de la receta al añadir el item)

daily_plans                  ← plan real de un cliente en una fecha concreta (user_id, date, objetivos del día)
  └─ daily_plan_recipes      ← receta asignada a una comida de ese día real (mismo recipe_id/
                                  fatsecret_recipe_id excluyentes que arriba)
```

**`fatsecret_recipe_id` es nuevo (2026-09-20)** -- antes de esa fecha, `recipe_id` era la única forma de referenciar una comida y era obligatorio. Si el Productor construyó su lógica leyendo una versión anterior de este documento o del código, tiene que revisar cualquier sitio donde asuma que `recipe_id` siempre viene relleno.

`meal_plan_templates.type`:
- **`sequential`**: "Día 0", "Día 1"... sin longitud fija — para un plan de N días que no se repite semana a semana.
- **`weekday`**: "monday".."sunday" — se repite cada semana. Usa esto por defecto salvo que el cliente tenga un patrón que varíe semana a semana (más parecido a la periodización por evento del agente de entrenamiento, que si aplica no debería mapearse a `weekday`).

## 2. Endpoints reales (todos bajo el grupo `auth:sanctum`, mismo patrón que `training-program-*`)

| Endpoint | Para qué |
|---|---|
| `GET recipe-filter-list` | Buscar en el recetario **propio** — soporta `title`, `meal_type[]`, `recipe_category_ids[]`, `recipe_tag_ids[]`, `start_calories`/`end_calories`, `start_protein`/`end_protein`, `start_carbs`/`end_carbs`, `start_fats`/`end_fats`, `min_preparation_time`/`max_preparation_time`. **Hoy (2026-09-20) devuelve 0 resultados siempre** -- `recipes` está vacía. Sigue siendo el camino correcto en cuanto el recetario propio se repueble (filtrado por rango de macros real, no solo texto) -- no está deprecado, solo temporalmente sin datos. |
| `GET recipe-detail/{id}` | Ficha completa de una receta **propia**: ingredientes (`recipeIngredients`, cada uno con `ingredient_id` y macros), pasos, categorías, tags. Mismo estado que la de arriba: correcta, sin datos por ahora. |
| `GET admin/fatsecret/recipes/search?q=...&page=N` | **Nuevo (2026-09-20).** Busca en el catálogo de FatSecret -- ver sección 2-bis, es el sustituto real de `recipe-filter-list` mientras `recipes` esté vacía. |
| `GET admin/fatsecret/recipes/{fatsecret_recipe_id}` | **Nuevo.** Detalle completo de una receta de FatSecret (pasos, ingredientes, nutrición) -- sustituto de `recipe-detail/{id}` para este origen. |
| `POST meal-plan-templates` | Crear la plantilla del plan (`title`, `type`). Sin cambios. |
| `POST meal-plan-templates/{id}/items` | Añadir una comida a un día (`day_key`, `meal_type`, y **exactamente uno** de `recipe_id` o `fatsecret_recipe_id`). Repetir por cada comida del plan. |
| `POST meal-plan-templates/{id}/import-to-calendar` | Asignar la plantilla ya construida al calendario real de un cliente (`client_id`, `start_date`, `weeks` si es `weekday`) — crea `daily_plans`/`daily_plan_recipes` reales (con `fatsecret_recipe_id` si el item lo tenía) y notifica al cliente. Es el análogo exacto de `programs:assign-client`/`POST training-program-assign-client` del agente de entrenamiento. |
| `GET client-limitation-list?client_id=X&type=allergy` (y `intolerance`/`aversion`/`ethical_religious_preference` una vez existan, ver más abajo) | Cribado de seguridad — Paso 1, apartado 0. Sin cambios. |

No hace falta construir un comando artisan nuevo tipo `programs:import`: el flujo completo (crear plantilla → añadir items → asignar a calendario) ya es HTTP, con el mismo token de coach que usa el resto del panel.

## 2-bis. FatSecret -- diferencias reales con `recipe-filter-list` que el Productor tiene que conocer

`admin/fatsecret/recipes/search` **NO admite los filtros de rango de macros** que sí tenía `recipe-filter-list` (`start_calories`/`end_calories`, `start_protein`/`end_protein`, etc.) -- es una limitación real de la API de FatSecret, no algo que se pueda arreglar en Bckbs, su método `recipes.search` solo acepta un texto libre (`q`) + paginación. Esto cambia el paso 2 del flujo (sección 3):

- Antes: "busca desayunos con 400-500 kcal y ≥30g proteína" era un filtro de servidor exacto.
- Ahora: hay que buscar con un texto descriptivo razonable (ej. `q=high protein breakfast`, `q=grilled chicken salad`) y **filtrar los candidatos devueltos en el propio razonamiento del Productor**, comparando `calories`/`protein`/`fat`/`carbs` de cada resultado (ya vienen embebidos en la búsqueda, sin llamada aparte) contra el rango objetivo de esa comida. Si ningún resultado de la primera búsqueda encaja, prueba otro texto de búsqueda antes de relajar el rango objetivo.

**ACTUALIZADO 2026-09-21: `admin/fatsecret/recipes/{id}` ya devuelve `name`/`directions`/`ingredients[].description` TRADUCIDOS al español** (DeepL, implementado y probado en real -- ver `Bckbs::docs/FATSECRET_INTEGRATION.md` sección 10). El Productor no tiene que hacer nada distinto para esto, llega ya en español en los mismos campos de siempre; el inglés original, si hiciera falta compararlo, está en `name_en`/`directions_en`/`ingredients_en` del mismo objeto. **`admin/fatsecret/recipes/search` (la búsqueda, no el detalle) sigue devolviendo `name`/`description` en inglés sin traducir** -- decisión deliberada de coste/latencia (hasta 50 resultados por búsqueda), documentar la elección de receta con el nombre en inglés de la búsqueda es normal, el nombre final que verá el cliente (vía el detalle) ya sale en español.

**Verificación de ingredientes/alergias para una receta de FatSecret:** `GET admin/fatsecret/recipes/{id}` devuelve `ingredients` (array de `{description, food_id, number_of_units, measurement_description}`) -- mismo tipo de revisión manual de texto que ya se hacía con `recipeIngredients` de una receta propia (ver sección 4), solo que la fuente del texto cambia. `food_id` ahí es el id de FatSecret, no tiene relación con `ingredients.id` de la tabla propia.

**No busques comida por comida en un plan largo -- reutiliza `type: "weekday"` para no disparar cientos de llamadas.** Un plan de 1 mes con 4 comidas/día NO son 120 búsquedas (30 días × 4): con `meal_plan_templates.type: "weekday"`, la plantilla se construye como una sola semana modelo (7 `day_key` × 4 `meal_type` = como mucho 28 items) y `POST .../import-to-calendar` con `weeks: 4` repite esa misma semana el mes entero -- no crees 30 días sueltos con `type: "sequential"` salvo que el cliente realmente necesite un patrón que varíe semana a semana (ver sección 1). Dentro de esos ~28 items, si varias comidas del mismo `meal_type` comparten un rango de macros parecido (ej. varios desayunos ~500 kcal/35g proteína para dar variedad sin repetir receta), una sola búsqueda que devuelve hasta 50 candidatos ya alcanza para elegir varios de golpe y repartirlos entre esos días -- no repitas la búsqueda por cada día si el rango objetivo no cambia. Pide el detalle de ingredientes (`GET admin/fatsecret/recipes/{id}`) solo para las recetas que de verdad eliges, nunca para todos los candidatos que descartaste al filtrar por macros.

## 3. Flujo del Productor (Paso 2) usando estos endpoints

1. Calcula el objetivo calórico/macros del cliente (`necesidades-energeticas-macronutrientes.md`) y decide `day_key`/`meal_type` por día según `timing-nutricional-entrenamiento.md`.
2. Para cada comida, primero intenta `GET recipe-filter-list` con los rangos de macros que le corresponden (recetario propio, filtro exacto de servidor) -- **hoy siempre vacío**, así que en la práctica el paso real es: busca en `GET admin/fatsecret/recipes/search?q=...` con un texto descriptivo de esa comida (ver sección 2-bis) y filtra tú mismo los resultados devueltos por rango de macros, ya que esta búsqueda no acepta filtros de servidor. En cuanto `recipe-filter-list` vuelva a tener datos, es preferible a FatSecret para lo que sí cubra (evita el problema de idioma y el filtrado manual) -- combina ambas fuentes, no descartes la propia solo porque hoy esté vacía.
3. Antes de fijar una receta candidata: si es propia, pide `GET recipe-detail/{id}` y revisa `recipeIngredients`; si es de FatSecret, pide `GET admin/fatsecret/recipes/{id}` y revisa `ingredients` (mismo criterio de exclusiones del cribado de alergias, Paso 1 apartado 0 -- ver limitación de la sección 4, en ambos casos es revisión manual del texto, no un filtro automático).
4. Documenta en el razonamiento (Paso 2, punto 4 del `system-prompt.md`): qué se buscó, en qué fuente (propia o FatSecret), qué filtros/criterio se usaron, qué receta se eligió y por qué -- igual que el agente de entrenamiento documenta la búsqueda en el catálogo de ejercicios.
5. Solo tras la aprobación humana (Paso 5): crear la plantilla (`POST meal-plan-templates`), añadir cada item (`POST .../items`, con `recipe_id` o `fatsecret_recipe_id` según la fuente elegida en el paso 2), y asignar al cliente (`POST .../import-to-calendar`).

## 4. Limitación real, no resuelta todavía: sin etiquetado de alérgenos por ingrediente

`ingredients` no tiene ninguna columna de alérgenos (`contiene_gluten`, `contiene_frutos_secos`, etc.) — la única forma de comprobar una alergia hoy es que el Productor (o un humano) lea el título de cada ingrediente en `recipe-detail/{id}` (propia) o `ingredients[].description` de `admin/fatsecret/recipes/{id}` (FatSecret) y lo compare a ojo con la exclusión. **Esto es un guardrail más débil de lo que exige `alergias-intolerancias.md` para `severidad: grave_anafilaxia`** (esa severidad exige comprobar también contaminación cruzada, imposible de verificar solo con títulos de ingrediente) -- y para FatSecret es, si cabe, más débil todavía: los títulos vienen en inglés y son de un catálogo externo que no controlamos, así que el margen de error de una lectura rápida es mayor que con el recetario propio. Hasta que exista etiquetado real:

- Para alergias `leve`/`moderada`: la revisión manual de títulos de ingrediente es aceptable.
- Para `grave_anafilaxia`: el borrador debe marcarse **siempre** para revisión humana explícita antes de asignar al calendario (ya lo exige el módulo de todos modos), y el humano debe verificar la receta por su cuenta, no confiar en que el Productor ya lo comprobó de forma fiable.

Ver también el encargo `BRIEF_registro_alergias_intolerancias.md` (entregado aparte) para el registro estructurado de severidad — el etiquetado de alérgenos por ingrediente es un encargo distinto, todavía sin escribir, que depende de este primero.

**Actualizado 2026-09-20:** el validador determinista (`validador/validar_plan.py`) ya emite una advertencia explícita cuando un item viene de `fatsecret_recipe_id` y el cliente tiene alguna exclusión activa — la coincidencia de texto no puede detectar un alérgeno si el ingrediente está en inglés (FatSecret) y la exclusión en español (ej. "peanuts" nunca coincide con "frutos secos"). El plan puede "aprobar" el validador sin que eso signifique que ese item concreto quedó cribado de verdad — la revisión humana es obligatoria ahí, no opcional, más todavía que con el recetario propio.

## 5. Alineación con el cálculo real de macros de la app

`app/Traits/DailyPlanTrait.php::calculateDailyPlan()` ya calcula BMR con Mifflin-St Jeor (coincide con `necesidades-energeticas-macronutrientes.md`, sección 1) y aplica:

- **Actividad** (`config('macro-nutrient.ACTIVITY_LEVEL')`): sedentary ×1.2, lightly_active ×1.375, moderate ×1.55, very_active ×1.725, athlete ×1.9.
- **Objetivo** (`config('macro-nutrient.FITNESS_GOAL')`): variación porcentual sobre el TDEE, no kcal absolutas — mantenimiento 0%, pérdida -10/-20/-40%, ganancia +10/+20/+40%.
- **Reparto de macros** (`config('macro-nutrient.MACRO_RATIO')`): presets en % de calorías (`balanced` 40/30/30 carbs/proteína/grasa, `low_fat` 40/40/20, `high_protein` 20/50/30, `high_carb` 55/25/20, `keto` 5/25/70), o `macro_type: custom` con `protein_pct`/`carbs_pct`/`fat_pct` explícitos.
- **Tolerancia:** cada macro objetivo ya se acompaña de un rango ±10% (`from`/`to`) — es el mismo criterio que debe usar el validador determinista (Paso 3) para decidir si un día está "dentro de objetivo".

**Importante para `recomposicion-corporal-nutricion.md`:** el déficit real que aplica la app es un **porcentaje del TDEE** (-10/-20/-40%), no una cifra fija en kcal. El guardrail de "nunca más de 500 kcal/día de déficit" (heredado de `hipertrofia-recomposicion-corporal.md` del agente de entrenamiento) hay que comprobarlo **después** de calcular qué kcal absolutas produce el porcentaje elegido para el TDEE real de ese cliente — un mismo -20% puede ser 400 kcal para un cliente sedentario y más de 700 kcal para uno muy activo. Si el preset más cercano se pasa del límite, usa `macro_type: custom` para fijar un porcentaje de calorías que sí lo respete, en vez de forzar el preset más próximo.
