# -*- coding: utf-8 -*-
"""Pruebas unitarias del cálculo de Impuesto Único."""
import unittest

from calculos.impuesto_unico import calcular_impuesto_unico, obtener_tramo

TRAMOS = [
    {"tramo": 1, "desde_utm": 0, "hasta_utm": 13.5, "factor": 0.0, "rebaja_utm": 0.0},
    {"tramo": 2, "desde_utm": 13.5, "hasta_utm": 30, "factor": 0.04, "rebaja_utm": 0.54},
    {"tramo": 3, "desde_utm": 30, "hasta_utm": 50, "factor": 0.08, "rebaja_utm": 1.74},
    {"tramo": 4, "desde_utm": 50, "hasta_utm": None, "factor": 0.135, "rebaja_utm": 4.49},
]

VALOR_UTM = 65000


class TestImpuestoUnico(unittest.TestCase):
    def test_tramo_exento(self):
        base = 10 * VALOR_UTM  # 10 UTM, dentro del tramo exento
        impuesto = calcular_impuesto_unico(base, VALOR_UTM, TRAMOS)
        self.assertEqual(impuesto, 0.0)

    def test_impuesto_nunca_negativo(self):
        impuesto = calcular_impuesto_unico(100, VALOR_UTM, TRAMOS, monto_cargas_familiares=1_000_000)
        self.assertGreaterEqual(impuesto, 0.0)

    def test_calculo_progresivo(self):
        base = 20 * VALOR_UTM  # 20 UTM -> tramo 2
        impuesto = calcular_impuesto_unico(base, VALOR_UTM, TRAMOS)
        esperado = round(((20 * 0.04) - 0.54) * VALOR_UTM, 0)
        self.assertEqual(impuesto, esperado)

    def test_obtener_tramo_ultimo_sin_limite(self):
        tramo = obtener_tramo(1000, TRAMOS)
        self.assertEqual(tramo["tramo"], 4)

    def test_base_o_utm_cero(self):
        self.assertEqual(calcular_impuesto_unico(0, VALOR_UTM, TRAMOS), 0.0)
        self.assertEqual(calcular_impuesto_unico(1000, 0, TRAMOS), 0.0)


if __name__ == "__main__":
    unittest.main()
