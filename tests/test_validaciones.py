# -*- coding: utf-8 -*-
"""Pruebas unitarias de validaciones (RUT, fechas, montos)."""
import unittest

from calculos.validaciones import (
    validar_rut,
    formatear_rut,
    validar_fecha,
    validar_monto_positivo,
    validar_texto_no_vacio,
)


class TestValidaciones(unittest.TestCase):
    def test_rut_valido(self):
        self.assertTrue(validar_rut("12345678-5"))
        self.assertTrue(validar_rut("11.111.111-1"))

    def test_rut_invalido(self):
        self.assertFalse(validar_rut("12345678-9"))
        self.assertFalse(validar_rut(""))
        self.assertFalse(validar_rut("ABC"))

    def test_formatear_rut(self):
        self.assertEqual(formatear_rut("123456785"), "12.345.678-5")

    def test_validar_fecha(self):
        self.assertTrue(validar_fecha("2024-01-31"))
        self.assertFalse(validar_fecha("2024-02-30"))
        self.assertFalse(validar_fecha(""))

    def test_validar_monto_positivo(self):
        self.assertTrue(validar_monto_positivo(0))
        self.assertTrue(validar_monto_positivo(100.5))
        self.assertFalse(validar_monto_positivo(-1))
        self.assertFalse(validar_monto_positivo("abc"))

    def test_validar_texto_no_vacio(self):
        self.assertTrue(validar_texto_no_vacio("Hola"))
        self.assertFalse(validar_texto_no_vacio("   "))
        self.assertFalse(validar_texto_no_vacio(None))


if __name__ == "__main__":
    unittest.main()
