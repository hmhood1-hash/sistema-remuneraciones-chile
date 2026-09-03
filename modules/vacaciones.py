# -*- coding: utf-8 -*-
"""Control de Vacaciones: registro y cálculo de días acumulados."""
from datetime import datetime

from database.conexion import conexion_bd

DIAS_HABILES_POR_ANIO = 15.0


def calcular_dias_disponibles(fecha_contrato, fecha_referencia=None, dias_usados=0):
    """Calcula los días hábiles de vacaciones acumulados y disponibles.

    Chile otorga 15 días hábiles por cada año de trabajo (proporcional para
    fracciones de año), a los que se restan los días ya usados/registrados.
    """
    inicio = datetime.strptime(fecha_contrato, "%Y-%m-%d")
    referencia = (
        datetime.strptime(fecha_referencia, "%Y-%m-%d") if fecha_referencia else datetime.now()
    )
    dias_trabajados = max((referencia - inicio).days, 0)
    anios_trabajados = dias_trabajados / 365.25
    dias_acumulados = round(anios_trabajados * DIAS_HABILES_POR_ANIO, 2)
    dias_disponibles = round(dias_acumulados - dias_usados, 2)
    return {
        "anios_trabajados": round(anios_trabajados, 2),
        "dias_acumulados": dias_acumulados,
        "dias_usados": dias_usados,
        "dias_disponibles": max(dias_disponibles, 0.0),
    }


def registrar_vacaciones(datos, ruta_bd=None):
    campos = (
        "codigo_empleado", "fecha_inicio", "fecha_termino", "dias_habiles",
        "dias_acumulados_antes", "observaciones",
    )
    valores = tuple(datos.get(campo) for campo in campos)
    with conexion_bd(ruta_bd) as conexion:
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO vacaciones ({}) VALUES ({})".format(
                ", ".join(campos), ", ".join(["?"] * len(campos))
            ),
            valores,
        )
        return cursor.lastrowid


def eliminar_vacaciones(id_vacacion, ruta_bd=None):
    with conexion_bd(ruta_bd) as conexion:
        conexion.execute("DELETE FROM vacaciones WHERE id_vacacion = ?", (id_vacacion,))


def listar_vacaciones(codigo_empleado=None, ruta_bd=None):
    with conexion_bd(ruta_bd) as conexion:
        if codigo_empleado:
            cursor = conexion.execute(
                "SELECT * FROM vacaciones WHERE codigo_empleado = ? ORDER BY fecha_inicio DESC",
                (codigo_empleado,),
            )
        else:
            cursor = conexion.execute("SELECT * FROM vacaciones ORDER BY fecha_inicio DESC")
        return [dict(fila) for fila in cursor.fetchall()]


def total_dias_usados(codigo_empleado, ruta_bd=None):
    with conexion_bd(ruta_bd) as conexion:
        cursor = conexion.execute(
            "SELECT COALESCE(SUM(dias_habiles), 0) AS total FROM vacaciones "
            "WHERE codigo_empleado = ?",
            (codigo_empleado,),
        )
        return cursor.fetchone()[0]
