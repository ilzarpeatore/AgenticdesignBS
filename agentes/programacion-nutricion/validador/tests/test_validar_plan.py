"""Pruebas del validador determinista (Paso 3) del Asistente de Programación de Nutrición.

A diferencia de `validador/validar_programa.py` del agente de entrenamiento
(probado contra el archivo real entregado a Toni), aquí **no existe todavía
ningún caso real de cliente** para este agente — ver `system-prompt.md`,
sección 9. Los fixtures de este archivo son sintéticos, construidos a mano
para representar el shape real de la API de Bckbs (`meal_plan_templates`/
`meal_plan_template_items`, ver `formato-salida/entrega-bckbs.md`), no un
plan que se haya generado ni entregado de verdad. Sustituir por un caso real
en cuanto exista uno (mismo criterio que llevó a usar el archivo de Toni en
el validador de entrenamiento).
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from validar_plan import validar_plan  # noqa: E402


def plan_base(**overrides):
    plan = {
        "template": {"title": "Plan sintético de prueba", "type": "weekday"},
        "objetivo_diario": {"calories": 2000, "protein": 150, "fats": 65, "carbs": 220},
        "restricciones_dieteticas": [
            {"descripcion": "Frutos secos", "tipo": "alergia", "severidad": "grave_anafilaxia"},
        ],
        "items": [
            {
                "day_key": "monday", "meal_type": "breakfast", "recipe_id": 101,
                "calories": 500, "protein": 35, "fats": 15, "carbs": 55,
                "ingredientes": ["avena", "leche", "platano"],
            },
            {
                "day_key": "monday", "meal_type": "lunch", "recipe_id": 102,
                "calories": 700, "protein": 55, "fats": 25, "carbs": 75,
                "ingredientes": ["pechuga de pollo", "arroz", "brocoli"],
            },
            {
                "day_key": "monday", "meal_type": "dinner", "recipe_id": 103,
                "calories": 600, "protein": 45, "fats": 20, "carbs": 70,
                "ingredientes": ["salmon", "patata", "espinacas"],
            },
            {
                "day_key": "monday", "meal_type": "snacks", "recipe_id": 104,
                "calories": 200, "protein": 15, "fats": 5, "carbs": 20,
                "ingredientes": ["yogur griego", "miel"],
            },
        ],
    }
    plan.update(overrides)
    return plan


class TestPlanSinteticoValido(unittest.TestCase):
    def test_plan_bien_formado_aprueba(self):
        informe = validar_plan(plan_base())
        self.assertEqual(informe.errores, [])
        self.assertTrue(informe.aprobado)


class TestGuardrailAlergias(unittest.TestCase):
    def test_alergia_sin_severidad_bloquea_todo_el_plan(self):
        plan = plan_base(restricciones_dieteticas=[{"descripcion": "Marisco", "tipo": "alergia"}])
        informe = validar_plan(plan)
        self.assertFalse(informe.aprobado)
        self.assertTrue(any("sin 'severidad'" in e for e in informe.errores))

    def test_ingrediente_alergeno_detectado(self):
        plan = plan_base()
        plan["items"][1]["ingredientes"] = ["pechuga de pollo", "arroz", "frutos secos"]
        informe = validar_plan(plan)
        self.assertFalse(informe.aprobado)
        self.assertTrue(any("frutos secos" in e for e in informe.errores))

    def test_intolerancia_tambien_bloquea_por_ingrediente(self):
        # El cribado es coincidencia de texto (título de ingrediente), no semántica --
        # "leche" no matchea contra "lactosa" (limitación real, ver entrega-bckbs.md
        # sección 4). Se usa el mismo término literal a propósito para probar el
        # camino de intolerancia sin fingir una capacidad que el código no tiene.
        plan = plan_base(restricciones_dieteticas=[{"descripcion": "Leche", "tipo": "intolerancia"}])
        plan["items"][0]["ingredientes"] = ["avena", "leche", "platano"]
        informe = validar_plan(plan)
        self.assertFalse(informe.aprobado)
        self.assertTrue(any("leche" in e.lower() for e in informe.errores))

    def test_aversion_no_bloquea_ni_avisa_como_seguridad(self):
        # aversion no es un TIPOS_EXCLUSION_DURA -- es adherencia, no seguridad.
        plan = plan_base(restricciones_dieteticas=[{"descripcion": "Coliflor", "tipo": "aversion"}])
        plan["items"][2]["ingredientes"] = ["salmon", "patata", "coliflor"]
        informe = validar_plan(plan)
        self.assertTrue(informe.aprobado)

    def test_sin_ingredientes_genera_advertencia_no_error(self):
        plan = plan_base()
        plan["items"][0].pop("ingredientes")
        informe = validar_plan(plan)
        self.assertTrue(informe.aprobado)
        self.assertTrue(any("sin lista de ingredientes" in a for a in informe.advertencias))


class TestEstructuraDeItems(unittest.TestCase):
    def test_meal_type_invalido(self):
        plan = plan_base()
        plan["items"][0]["meal_type"] = "brunch"
        informe = validar_plan(plan)
        self.assertFalse(informe.aprobado)
        self.assertTrue(any("meal_type" in e for e in informe.errores))

    def test_recipe_id_no_entero(self):
        plan = plan_base()
        plan["items"][0]["recipe_id"] = "ciento uno"
        informe = validar_plan(plan)
        self.assertFalse(informe.aprobado)
        self.assertTrue(any("recipe_id" in e for e in informe.errores))

    def test_day_key_invalido_para_weekday(self):
        plan = plan_base()
        plan["items"][0]["day_key"] = "lunes"  # en español, no vale para type=weekday
        informe = validar_plan(plan)
        self.assertFalse(informe.aprobado)
        self.assertTrue(any("día de la semana válido" in e for e in informe.errores))

    def test_day_key_negativo_invalido_para_sequential(self):
        plan = plan_base()
        plan["template"]["type"] = "sequential"
        for item in plan["items"]:
            item["day_key"] = "0"
        plan["items"][0]["day_key"] = "-1"
        informe = validar_plan(plan)
        self.assertFalse(informe.aprobado)
        self.assertTrue(any("sequential" in e for e in informe.errores))

    def test_type_de_plantilla_invalido(self):
        plan = plan_base()
        plan["template"]["type"] = "monthly"
        informe = validar_plan(plan)
        self.assertFalse(informe.aprobado)
        self.assertTrue(any("template.type" in e for e in informe.errores))

    def test_receta_duplicada_en_mismo_slot_es_advertencia(self):
        # Sin objetivo_diario para aislar el aviso de duplicado: duplicar un item
        # también desplaza los totales de macros del día, que con objetivo_diario
        # puesto haría fallar la comprobación de tolerancia (sección 7) -- eso es
        # comportamiento correcto, no lo que esta prueba quiere aislar.
        plan = plan_base()
        del plan["objetivo_diario"]
        plan["items"].append(dict(plan["items"][0]))
        informe = validar_plan(plan)
        self.assertTrue(informe.aprobado)
        self.assertTrue(any("repetida" in a for a in informe.advertencias))


class TestToleranciaDeMacros(unittest.TestCase):
    def test_macros_dentro_de_tolerancia_aprueba(self):
        informe = validar_plan(plan_base())
        self.assertTrue(informe.aprobado)

    def test_macros_fuera_de_tolerancia_falla(self):
        plan = plan_base(objetivo_diario={"calories": 1200, "protein": 150, "fats": 65, "carbs": 220})
        informe = validar_plan(plan)
        self.assertFalse(informe.aprobado)
        self.assertTrue(any("'calories' total" in e for e in informe.errores))

    def test_sin_objetivo_diario_es_advertencia_no_error(self):
        plan = plan_base()
        del plan["objetivo_diario"]
        informe = validar_plan(plan)
        self.assertTrue(informe.aprobado)
        self.assertTrue(any("objetivo_diario" in a for a in informe.advertencias))

    def test_tolerancia_personalizada(self):
        plan = plan_base(objetivo_diario={"calories": 2500, "protein": 150, "fats": 65, "carbs": 220})
        # 2000 real vs 2500 objetivo -> -20%, dentro de una tolerancia del 25% pero no del 10%
        self.assertFalse(validar_plan(plan, tolerancia=0.10).aprobado)
        self.assertTrue(validar_plan(plan, tolerancia=0.25).aprobado)


if __name__ == "__main__":
    unittest.main()
