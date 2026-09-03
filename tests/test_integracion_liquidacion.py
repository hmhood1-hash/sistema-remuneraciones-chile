# -*- coding: utf-8 -*-
"""Pruebas de integración: base de datos, trabajador y cálculo de liquidación."""
import os
import tempfile
import unittest

from database.init_db import inicializar_base_datos
from modules import empresa as mod_empresa
from modules import trabajador as mod_trabajador
from modules import parametros as mod_parametros
from modules import liquidacion as mod_liquidacion


class TestLiquidacionIntegracion(unittest.TestCase):
    def setUp(self):
        descriptor, self.ruta_bd = tempfile.mkstemp(suffix=".db")
        os.close(descriptor)
        os.remove(self.ruta_bd)
        inicializar_base_datos(self.ruta_bd)

        self.codigo_empresa = mod_empresa.crear_empresa(
            {"rut": "76123456-7", "razon_social": "Empresa de Pruebas SpA"}, self.ruta_bd
        )
        mod_parametros.actualizar_parametros(
            {"utm": 65182, "uf_afp_isapre": 37500, "tope_imponible_afp_uf": 87.8}, self.ruta_bd
        )
        mod_parametros.guardar_factor_mensual(2024, 1, 1.0, 65182, 37500, self.ruta_bd)

        self.codigo_empleado = mod_trabajador.crear_trabajador(
            {
                "codigo_empresa": self.codigo_empresa,
                "rut": "12345678-5",
                "nombres": "Juan",
                "apellido_paterno": "Pérez",
                "sueldo_tipo": "Mensual",
                "sueldo_base": 800000,
                "codigo_afp": "CAPITAL",
                "seguro_cesantia": "Indefinido",
                "tipo_trabajador": "Activo No Pensionado",
                "aplica_sis": "S",
            },
            self.ruta_bd,
        )

    def tearDown(self):
        if os.path.exists(self.ruta_bd):
            os.remove(self.ruta_bd)

    def test_crear_empresa_y_trabajador(self):
        empresa = mod_empresa.obtener_empresa(self.codigo_empresa, self.ruta_bd)
        self.assertEqual(empresa["razon_social"], "Empresa de Pruebas SpA")
        trabajador = mod_trabajador.obtener_trabajador(self.codigo_empleado, self.ruta_bd)
        self.assertEqual(trabajador["rut"], "12345678-5")
        self.assertEqual(trabajador["sueldo_base"], 800000)

    def test_calcular_y_guardar_liquidacion(self):
        liquidacion = mod_liquidacion.calcular_liquidacion(
            self.codigo_empleado, 2024, 1, ruta_bd=self.ruta_bd
        )
        self.assertEqual(liquidacion["total_ingreso_bruto"], 800000.0)
        self.assertGreater(liquidacion["monto_afp"], 0)
        self.assertGreater(liquidacion["monto_salud"], 0)
        self.assertEqual(
            liquidacion["sueldo_liquido"],
            liquidacion["total_ingreso_bruto"] - liquidacion["total_descuentos"],
        )
        self.assertGreaterEqual(liquidacion["impuesto_unico"], 0)

        id_liquidacion = mod_liquidacion.guardar_liquidacion(liquidacion, self.ruta_bd)
        self.assertIsNotNone(id_liquidacion)

        guardada = mod_liquidacion.obtener_liquidacion(self.codigo_empleado, 2024, 1, self.ruta_bd)
        self.assertIsNotNone(guardada)
        self.assertEqual(guardada["sueldo_liquido"], liquidacion["sueldo_liquido"])

    def test_cargas_familiares_afectan_impuesto(self):
        mod_trabajador.crear_carga_familiar(
            {
                "codigo_empleado": self.codigo_empleado,
                "rut_carga": "22222222-2",
                "nombre": "Hijo de Prueba",
                "fecha_inicio": "2020-01-01",
                "tipo": "Simple",
                "parentesco": "Hijo",
            },
            self.ruta_bd,
        )
        cargas = mod_trabajador.listar_cargas_familiares(self.codigo_empleado, self.ruta_bd)
        self.assertEqual(len(cargas), 1)


if __name__ == "__main__":
    unittest.main()
