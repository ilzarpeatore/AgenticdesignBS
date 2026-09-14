"""Pruebas del validador determinista (Paso 3).

Usan como fixture principal el programa real generado para Toni
(`fixtures/Mesociclo_1_TONI_Septiembre.xlsx`) — no un ejemplo sintético — y
copias de ese mismo archivo mutadas deliberadamente para provocar cada
fallo, así el validador se prueba contra el mismo tipo de archivo que
generará el Productor, no contra una maqueta.
"""

import copy
import os
import sys
import unittest

import openpyxl

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from validar_programa import validar_programa  # noqa: E402

DIR_FIXTURES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")
TONI_XLSX = os.path.join(DIR_FIXTURES, "Mesociclo_1_TONI_Septiembre.xlsx")
CATALOGO_XLSX = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "formato-salida", "catalogo-ejercicios.xlsx",
)


def _copiar_y_mutar(ruta_origen, ruta_destino, mutador):
    wb = openpyxl.load_workbook(ruta_origen)
    mutador(wb)
    wb.save(ruta_destino)


class TestProgramaRealDeToni(unittest.TestCase):
    """El caso base: el archivo real entregado debe aprobar sin errores."""

    def test_aprueba_sin_catalogo_ni_exclusiones(self):
        informe = validar_programa(TONI_XLSX, semanas_esperadas=3)
        self.assertEqual(informe.errores, [])
        self.assertTrue(informe.aprobado)

    def test_aprueba_con_catalogo_real(self):
        informe = validar_programa(TONI_XLSX, ruta_catalogo=CATALOGO_XLSX, semanas_esperadas=3)
        self.assertEqual(informe.errores, [])
        # Todos los ejercicios de Toni existen literalmente en el catálogo real,
        # así que tampoco debería haber advertencias de "ejercicio nuevo".
        advertencias_catalogo = [a for a in informe.advertencias if "catálogo" in a or "catalogo" in a]
        self.assertEqual(advertencias_catalogo, [])

    def test_detecta_ejercicios_excluidos_del_caso_real(self):
        # Toni tiene lesión de manguito rotador y no dispone de Hack Squat:
        # comprobar que si esos nombres SÍ aparecieran, el validador los marcaría.
        informe = validar_programa(TONI_XLSX, ejercicios_excluidos=["Press banca con mancuernas"])
        self.assertFalse(informe.aprobado)
        self.assertTrue(any("Press banca con mancuernas" in e for e in informe.errores))

    def test_semanas_esperadas_incorrectas_falla(self):
        informe = validar_programa(TONI_XLSX, semanas_esperadas=4)
        self.assertFalse(informe.aprobado)
        self.assertTrue(any("Faltan semanas" in e for e in informe.errores))


class TestMutacionesQueDebenFallar(unittest.TestCase):
    """Cada mutación introduce exactamente un tipo de fallo real del formato."""

    def setUp(self):
        self.ruta_tmp = os.path.join(DIR_FIXTURES, f"_tmp_{self._testMethodName}.xlsx")

    def tearDown(self):
        if os.path.exists(self.ruta_tmp):
            os.remove(self.ruta_tmp)

    def test_falta_hoja_programacion(self):
        def mutar(wb):
            del wb["Programación"]
        _copiar_y_mutar(TONI_XLSX, self.ruta_tmp, mutar)
        informe = validar_programa(self.ruta_tmp)
        self.assertFalse(informe.aprobado)
        self.assertTrue(any("Programación" in e for e in informe.errores))

    def test_semanas_declaradas_no_coincide(self):
        def mutar(wb):
            wb["Programa"]["C2"] = 99
        _copiar_y_mutar(TONI_XLSX, self.ruta_tmp, mutar)
        informe = validar_programa(self.ruta_tmp)
        self.assertFalse(informe.aprobado)
        self.assertTrue(any("semanas=99" in e for e in informe.errores))

    def test_fila_sin_series_ni_reps(self):
        def mutar(wb):
            ws = wb["Programación"]
            ws["J2"] = None  # 'series' de la primera fila de ejercicio
            ws["K2"] = None  # 'reps' de la primera fila de ejercicio
        _copiar_y_mutar(TONI_XLSX, self.ruta_tmp, mutar)
        informe = validar_programa(self.ruta_tmp)
        self.assertFalse(informe.aprobado)
        self.assertTrue(any("falta 'series'" in e for e in informe.errores))
        self.assertTrue(any("falta 'reps'" in e for e in informe.errores))

    def test_dia_fuera_de_rango(self):
        def mutar(wb):
            ws = wb["Programación"]
            ws["B2"] = 8  # 'dia' no puede ser 8
        _copiar_y_mutar(TONI_XLSX, self.ruta_tmp, mutar)
        informe = validar_programa(self.ruta_tmp)
        self.assertFalse(informe.aprobado)
        self.assertTrue(any("'dia' debe ser un entero entre 1 y 7" in e for e in informe.errores))

    def test_nombre_dia_inconsistente_dentro_del_mismo_dia(self):
        def mutar(wb):
            ws = wb["Programación"]
            ws["C3"] = "Nombre distinto"  # misma (semana, dia) que la fila 2, nombre_dia distinto
        _copiar_y_mutar(TONI_XLSX, self.ruta_tmp, mutar)
        informe = validar_programa(self.ruta_tmp)
        self.assertFalse(informe.aprobado)
        self.assertTrue(any("no coincide con el ya visto" in e for e in informe.errores))

    def test_fila_descanso_con_columnas_de_ejercicio_rellenas(self):
        def mutar(wb):
            ws = wb["Programación"]
            fila_nueva = 50
            ws.cell(row=fila_nueva, column=1, value=1)
            ws.cell(row=fila_nueva, column=2, value=5)
            ws.cell(row=fila_nueva, column=3, value="Descanso activo")
            ws.cell(row=fila_nueva, column=4, value=True)  # es_descanso
            ws.cell(row=fila_nueva, column=8, value="Sentadilla")  # 'ejercicio' no debería estar
        _copiar_y_mutar(TONI_XLSX, self.ruta_tmp, mutar)
        informe = validar_programa(self.ruta_tmp)
        self.assertFalse(informe.aprobado)
        self.assertTrue(any("es_descanso=TRUE pero tiene columnas de ejercicio rellenas" in e for e in informe.errores))

    def test_semana_con_hueco(self):
        def mutar(wb):
            ws = wb["Programación"]
            for fila in ws.iter_rows(min_row=2):
                if fila[0].value == 2:
                    fila[0].value = 4  # desplaza toda la semana 2 a la semana 4 -> hueco en 2-3
        _copiar_y_mutar(TONI_XLSX, self.ruta_tmp, mutar)
        informe = validar_programa(self.ruta_tmp)
        self.assertFalse(informe.aprobado)
        self.assertTrue(any("huecos" in e for e in informe.errores))


class TestAdvertenciasNoBloqueantes(unittest.TestCase):
    """rir+rpe simultáneos y ejercicio ausente del catálogo son advertencias, no errores."""

    def setUp(self):
        self.ruta_tmp = os.path.join(DIR_FIXTURES, f"_tmp_{self._testMethodName}.xlsx")

    def tearDown(self):
        if os.path.exists(self.ruta_tmp):
            os.remove(self.ruta_tmp)

    def test_rir_y_rpe_a_la_vez_es_advertencia(self):
        def mutar(wb):
            ws = wb["Programación"]
            ws["M2"] = 8  # 'rpe' además del 'rir' ya presente en L2
        _copiar_y_mutar(TONI_XLSX, self.ruta_tmp, mutar)
        informe = validar_programa(self.ruta_tmp)
        self.assertTrue(informe.aprobado)
        self.assertTrue(any("'rir' y 'rpe' rellenos a la vez" in a for a in informe.advertencias))

    def test_ejercicio_nuevo_no_esta_en_catalogo_es_advertencia(self):
        def mutar(wb):
            ws = wb["Programación"]
            ws["H2"] = "Ejercicio inventado que no existe en catálogo"
        _copiar_y_mutar(TONI_XLSX, self.ruta_tmp, mutar)
        informe = validar_programa(self.ruta_tmp, ruta_catalogo=CATALOGO_XLSX)
        self.assertTrue(informe.aprobado)
        self.assertTrue(any("no coincide exactamente con ningún título del catálogo" in a for a in informe.advertencias))


if __name__ == "__main__":
    unittest.main()
