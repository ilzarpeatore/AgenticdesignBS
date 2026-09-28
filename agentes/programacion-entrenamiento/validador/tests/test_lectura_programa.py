"""Pruebas del lector compartido (extraído de validar_programa.py v0.6.0
para que agentes/control-producto/ lea el mismo formato exactamente igual).

Mismo fixture real que test_validar_programa.py -- este módulo no debe
comportarse distinto según quién lo llame.
"""

import os
import sys
import unittest

import openpyxl

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lectura_programa import LecturaProgramaError, leer_programa  # noqa: E402

DIR_FIXTURES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")
TONI_XLSX = os.path.join(DIR_FIXTURES, "Mesociclo_1_TONI_Septiembre.xlsx")


def _copiar_y_mutar(ruta_origen, ruta_destino, mutador):
    wb = openpyxl.load_workbook(ruta_origen)
    mutador(wb)
    wb.save(ruta_destino)


class TestLecturaDelProgramaRealDeToni(unittest.TestCase):
    def test_lee_filas_y_columnas_en_orden_estandar(self):
        lectura = leer_programa(TONI_XLSX)
        self.assertTrue(lectura.orden_estandar)
        self.assertTrue(lectura.tiene_columna_semanas)
        self.assertGreater(len(lectura.filas), 0)

    def test_val_accede_a_columnas_reales(self):
        lectura = leer_programa(TONI_XLSX)
        primera_fila_ejercicio = next(
            f for f in lectura.filas if not lectura.val(f, "es_descanso") and lectura.val(f, "ejercicio")
        )
        self.assertIsNotNone(lectura.val(primera_fila_ejercicio, "series"))
        self.assertIsNotNone(lectura.val(primera_fila_ejercicio, "reps"))

    def test_semanas_declaradas_coincide_con_el_valor_real(self):
        lectura = leer_programa(TONI_XLSX)
        self.assertEqual(lectura.semanas_declaradas, 3)


class TestLecturaProgramaErrorEnFormasInvalidas(unittest.TestCase):
    def setUp(self):
        self.ruta_tmp = os.path.join(DIR_FIXTURES, f"_tmp_{self._testMethodName}.xlsx")

    def tearDown(self):
        if os.path.exists(self.ruta_tmp):
            os.remove(self.ruta_tmp)

    def test_falta_hoja_programacion_lanza_error_con_mensaje_real(self):
        def mutar(wb):
            del wb["Programación"]
        _copiar_y_mutar(TONI_XLSX, self.ruta_tmp, mutar)
        with self.assertRaises(LecturaProgramaError) as ctx:
            leer_programa(self.ruta_tmp)
        self.assertTrue(any("Programación" in e for e in ctx.exception.errores))

    def test_falta_columna_obligatoria_lanza_error(self):
        def mutar(wb):
            ws = wb["Programación"]
            ws["J1"] = "no_es_series"  # renombra la columna 'series'
        _copiar_y_mutar(TONI_XLSX, self.ruta_tmp, mutar)
        with self.assertRaises(LecturaProgramaError) as ctx:
            leer_programa(self.ruta_tmp)
        self.assertTrue(any("Faltan columnas obligatorias" in e for e in ctx.exception.errores))


if __name__ == "__main__":
    unittest.main()
