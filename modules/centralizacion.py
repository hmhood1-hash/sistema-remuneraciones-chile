# -*- coding: utf-8 -*-
"""Procesos mensuales: Centralización y Actualización de Base de Datos."""
import shutil
from datetime import datetime

from database.conexion import obtener_ruta_base_datos, obtener_directorio_datos
from database.init_db import inicializar_base_datos
from modules.trabajador import listar_trabajadores
from modules.liquidacion import calcular_liquidacion, guardar_liquidacion


def centralizacion_mensual(codigo_empresa, anio, mes, ruta_bd=None):
    """Genera (calcula y guarda) las liquidaciones de todos los trabajadores activos
    de una empresa para el período indicado.

    Devuelve un resumen con la cantidad de liquidaciones generadas y errores.
    """
    trabajadores = listar_trabajadores(codigo_empresa, solo_activos=True, ruta_bd=ruta_bd)
    generadas = []
    errores = []

    for trabajador in trabajadores:
        try:
            liquidacion = calcular_liquidacion(
                trabajador["codigo_empleado"], anio, mes, ruta_bd=ruta_bd
            )
            id_liquidacion = guardar_liquidacion(liquidacion, ruta_bd=ruta_bd)
            generadas.append(
                {"codigo_empleado": trabajador["codigo_empleado"], "id_liquidacion": id_liquidacion}
            )
        except Exception as error:  # noqa: BLE001 - se reporta el error por trabajador
            errores.append({"codigo_empleado": trabajador["codigo_empleado"], "error": str(error)})

    return {
        "total_trabajadores": len(trabajadores),
        "total_generadas": len(generadas),
        "generadas": generadas,
        "errores": errores,
    }


def respaldar_base_datos(ruta_bd=None, directorio_destino=None):
    """Genera una copia de respaldo del archivo de base de datos SQLite."""
    origen = ruta_bd or obtener_ruta_base_datos()
    destino_dir = directorio_destino or obtener_directorio_datos()
    marca_tiempo = datetime.now().strftime("%Y%m%d_%H%M%S")
    destino = "{}/respaldo_remuneraciones_{}.db".format(destino_dir, marca_tiempo)
    shutil.copy2(origen, destino)
    return destino


def actualizar_base_datos(ruta_bd=None):
    """Aplica el esquema más reciente a la base de datos existente (idempotente)."""
    return inicializar_base_datos(ruta_bd)
