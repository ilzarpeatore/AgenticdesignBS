# Validador determinista (Paso 3)

Código real, no prosa — comprueba mecánicamente el plan que el Productor va a
enviar a la API real de Bckbs (`meal_plan_templates`/`meal_plan_template_items`,
ver `../formato-salida/entrega-bckbs.md`) antes de que llegue al Crítico
(Paso 4) o al humano (Paso 5).

## Qué comprueba

- `template.type` es `sequential` o `weekday`, y cada `day_key` es coherente con ese tipo.
- Cada item tiene `day_key`, `meal_type` (uno de `breakfast`/`lunch`/`dinner`/`snacks`) y **exactamente uno** de `recipe_id` (receta propia) o `fatsecret_recipe_id` (receta de FatSecret) como entero — nunca los dos, nunca ninguno. Mismo bloqueo (422) que exige `meal-plan-templates/{id}/items` en Bckbs desde el 2026-09-20, ver `../formato-salida/entrega-bckbs.md`.
- **Ninguna alergia declarada sin `severidad`** — bloquea la validación completa del plan, no solo un item, siguiendo el guardrail de `modulos/alergias-intolerancias.md`.
- **Ningún ingrediente de ninguna receta coincide con una exclusión de tipo alergia/intolerancia** — comprobación por texto (título del ingrediente), no semántica. Ver la limitación real en `../formato-salida/entrega-bckbs.md`, sección 4: Bckbs no etiqueta alérgenos por ingrediente todavía, así que esto solo detecta coincidencias literales de nombre, no derivados ni trazas.
- **Macros diarios dentro de ±10% del objetivo** (`objetivo_diario`) — misma tolerancia que ya usa `DailyPlanTrait::calculateDailyPlan()` en producción.

Lo que **no** es error, solo advertencia:
- Un item sin lista de `ingredientes` (no se pudo cribar, pero no se asume que esté mal).
- Una receta repetida en el mismo `day_key`/`meal_type`.
- Ausencia de `objetivo_diario` (no se puede comprobar tolerancia, pero el resto de comprobaciones sí corren).

## Uso

```bash
python3 validar_plan.py plan.json --tolerancia 0.10
```

Formato de entrada — ver `tests/test_validar_plan.py::plan_base()` para un ejemplo completo:

```json
{
  "template": {"title": "...", "type": "weekday"},
  "objetivo_diario": {"calories": 2000, "protein": 150, "fats": 65, "carbs": 220},
  "restricciones_dieteticas": [
    {"descripcion": "Frutos secos", "tipo": "alergia", "severidad": "grave_anafilaxia"}
  ],
  "items": [
    {"day_key": "monday", "meal_type": "breakfast", "recipe_id": 101,
     "calories": 500, "protein": 35, "fats": 15, "carbs": 55,
     "ingredientes": ["avena", "leche", "platano"]},
    {"day_key": "monday", "meal_type": "lunch", "fatsecret_recipe_id": 987654,
     "calories": 700, "protein": 55, "fats": 25, "carbs": 75,
     "ingredientes": ["grilled chicken breast", "brown rice", "broccoli"]}
  ]
}
```

`ingredientes` no es un campo que la API de Bckbs reciba — es información que el
Productor añade a su representación interna (tras consultar `GET
recipe-detail/{id}` para una receta propia, o `GET admin/fatsecret/recipes/{id}`
para una de FatSecret) para que este validador pueda cribar alérgenos antes de
llamar a `POST meal-plan-templates/{id}/items`.

**Ojo con `fatsecret_recipe_id`:** los ingredientes de FatSecret vienen en inglés
(ver `../formato-salida/entrega-bckbs.md`, sección 2-bis) y el cribado de este
validador es coincidencia de texto literal contra las exclusiones en español —
"frutos secos" nunca va a coincidir con "peanuts". Por eso, siempre que un item
FatSecret tenga alguna exclusión activa en `restricciones_dieteticas`, el
validador emite una advertencia explícita de que el cribado automático no es
fiable para ese item, aunque el plan "apruebe" — la revisión humana es
obligatoria ahí, no opcional.

## Pruebas

```bash
python3 -m unittest discover -s tests
```

**A diferencia del validador del agente de entrenamiento** (probado contra el
archivo real entregado a Toni), aquí todavía no existe ningún caso real de
cliente — los fixtures de `tests/test_validar_plan.py` son sintéticos,
construidos a mano para representar el shape real de la API. Sustituir por un
caso real en cuanto exista uno.
