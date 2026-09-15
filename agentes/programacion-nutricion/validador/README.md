# Validador determinista (Paso 3)

Código real, no prosa — comprueba mecánicamente el plan que el Productor va a
enviar a la API real de Bckbs (`meal_plan_templates`/`meal_plan_template_items`,
ver `../formato-salida/entrega-bckbs.md`) antes de que llegue al Crítico
(Paso 4) o al humano (Paso 5).

## Qué comprueba

- `template.type` es `sequential` o `weekday`, y cada `day_key` es coherente con ese tipo.
- Cada item tiene `day_key`, `meal_type` (uno de `breakfast`/`lunch`/`dinner`/`snacks`) y `recipe_id` (entero).
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
     "ingredientes": ["avena", "leche", "platano"]}
  ]
}
```

`ingredientes` no es un campo que la API de Bckbs reciba — es información que el
Productor añade a su representación interna (tras consultar `GET
recipe-detail/{id}`) para que este validador pueda cribar alérgenos antes de
llamar a `POST meal-plan-templates/{id}/items`.

## Pruebas

```bash
python3 -m unittest discover -s tests
```

**A diferencia del validador del agente de entrenamiento** (probado contra el
archivo real entregado a Toni), aquí todavía no existe ningún caso real de
cliente — los fixtures de `tests/test_validar_plan.py` son sintéticos,
construidos a mano para representar el shape real de la API. Sustituir por un
caso real en cuanto exista uno.
