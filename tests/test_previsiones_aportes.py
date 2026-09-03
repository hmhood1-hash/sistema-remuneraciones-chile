# -*- coding: utf-8 -*-
"""Pruebas unitarias de cálculo de previsiones y aportes patronales."""
import unittest

from calculos.previsiones import calcular_afp, calcular_salud, calcular_seguro_cesantia
from calculos.aportes import calcular_aportes_patronales


class TestPrevisiones(unittest.TestCase):
    def test_calcular_afp_bajo_tope(self):
        monto = calcular_afp(1_000_000, 11.44, 87.8, 37500)
        self.assertEqual(monto, round(1_000_000 * 0.1144, 0))

    def test_calcular_afp_sobre_tope(self):
        tope_pesos = 87.8 * 37500
        monto = calcular_afp(tope_pesos * 2, 11.44, 87.8, 37500)
        self.assertEqual(monto, round(tope_pesos * 0.1144, 0))

    def test_pensionado_no_cotiza(self):
        monto = calcular_afp(1_000_000, 11.44, 87.8, 37500, tipo_trabajador="Pensionado no cotiza")
        self.assertEqual(monto, 0.0)

    def test_calcular_salud_minimo_legal(self):
        monto = calcular_salud(1_000_000, 87.8, 37500)
        self.assertEqual(monto, round(1_000_000 * 0.07, 0))

    def test_calcular_seguro_cesantia_plazo_fijo(self):
        monto = calcular_seguro_cesantia(1_000_000, 87.8, 37500, "Plazo Fijo", 0.6)
        self.assertEqual(monto, 0.0)

    def test_calcular_seguro_cesantia_indefinido(self):
        monto = calcular_seguro_cesantia(1_000_000, 87.8, 37500, "Indefinido", 0.6)
        self.assertEqual(monto, round(1_000_000 * 0.006, 0))


class TestAportes(unittest.TestCase):
    def test_aportes_patronales_totales(self):
        parametros = {
            "sis_empleador_pct": 1.53,
            "afc_empleador_indefinido_pct": 2.4,
            "afc_empleador_plazo_fijo_pct": 3.0,
            "ccaf_pct": 0.6,
            "aporte_patronal_pct": 0.0,
        }
        resultado = calcular_aportes_patronales(1_000_000, 87.8, 37500, parametros, "S", "Indefinido")
        total_esperado = (
            resultado["aporte_sis"] + resultado["aporte_afc_empleador"]
            + resultado["aporte_ccaf"] + resultado["aporte_patronal_afp"]
        )
        self.assertEqual(resultado["total_aportes_patronales"], total_esperado)
        self.assertGreater(resultado["total_aportes_patronales"], 0)


if __name__ == "__main__":
    unittest.main()
