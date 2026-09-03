# -*- coding: utf-8 -*-
"""Gestión de Contratos de Trabajo."""
from datetime import datetime

from database.conexion import conexion_bd

CAMPOS = (
    "codigo_empleado", "nacionalidad", "labor_ejecutar", "establecimiento",
    "horarios", "duracion_contrato", "codigo_tipo_contrato", "pago",
    "sueldo_base", "movilizacion", "colacion", "gratificacion",
    "remuneracion_adicional",
)


def crear_contrato(datos, ruta_bd=None):
    valores = tuple(datos.get(campo) for campo in CAMPOS)
    fecha_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with conexion_bd(ruta_bd) as conexion:
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO contrato ({}, fecha_creacion) VALUES ({}, ?)".format(
                ", ".join(CAMPOS), ", ".join(["?"] * len(CAMPOS))
            ),
            valores + (fecha_creacion,),
        )
        return cursor.lastrowid


def actualizar_contrato(id_contrato, datos, ruta_bd=None):
    campos = list(datos.keys())
    valores = list(datos.values())
    valores.append(id_contrato)
    with conexion_bd(ruta_bd) as conexion:
        conexion.execute(
            "UPDATE contrato SET {} WHERE id_contrato = ?".format(
                ", ".join("{} = ?".format(campo) for campo in campos)
            ),
            valores,
        )


def eliminar_contrato(id_contrato, ruta_bd=None):
    with conexion_bd(ruta_bd) as conexion:
        conexion.execute("DELETE FROM contrato WHERE id_contrato = ?", (id_contrato,))


def listar_contratos(codigo_empleado=None, ruta_bd=None):
    with conexion_bd(ruta_bd) as conexion:
        if codigo_empleado:
            cursor = conexion.execute(
                "SELECT * FROM contrato WHERE codigo_empleado = ? ORDER BY fecha_creacion DESC",
                (codigo_empleado,),
            )
        else:
            cursor = conexion.execute("SELECT * FROM contrato ORDER BY fecha_creacion DESC")
        return [dict(fila) for fila in cursor.fetchall()]


def obtener_contrato(id_contrato, ruta_bd=None):
    with conexion_bd(ruta_bd) as conexion:
        cursor = conexion.execute("SELECT * FROM contrato WHERE id_contrato = ?", (id_contrato,))
        fila = cursor.fetchone()
        return dict(fila) if fila else None
