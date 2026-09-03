# -*- coding: utf-8 -*-
"""CRUD de Haberes y Descuentos."""
from database.conexion import conexion_bd

CAMPOS = ("codigo", "nombre", "clasificacion", "clase", "monto", "porcentaje", "base_porcentaje")


def crear_haber_descuento(datos, ruta_bd=None):
    valores = tuple(datos.get(campo) for campo in CAMPOS)
    with conexion_bd(ruta_bd) as conexion:
        conexion.execute(
            "INSERT INTO haber_descuento ({}) VALUES ({})".format(
                ", ".join(CAMPOS), ", ".join(["?"] * len(CAMPOS))
            ),
            valores,
        )


def actualizar_haber_descuento(codigo, datos, ruta_bd=None):
    campos = list(datos.keys())
    valores = list(datos.values())
    valores.append(codigo)
    with conexion_bd(ruta_bd) as conexion:
        conexion.execute(
            "UPDATE haber_descuento SET {} WHERE codigo = ?".format(
                ", ".join("{} = ?".format(campo) for campo in campos)
            ),
            valores,
        )


def eliminar_haber_descuento(codigo, ruta_bd=None):
    with conexion_bd(ruta_bd) as conexion:
        conexion.execute("DELETE FROM haber_descuento WHERE codigo = ?", (codigo,))


def listar_haberes_descuentos(ruta_bd=None):
    with conexion_bd(ruta_bd) as conexion:
        cursor = conexion.execute("SELECT * FROM haber_descuento ORDER BY codigo")
        return [dict(fila) for fila in cursor.fetchall()]


def obtener_haber_descuento(codigo, ruta_bd=None):
    with conexion_bd(ruta_bd) as conexion:
        cursor = conexion.execute(
            "SELECT * FROM haber_descuento WHERE codigo = ?", (codigo,)
        )
        fila = cursor.fetchone()
        return dict(fila) if fila else None


def calcular_monto_haber(haber, sueldo_base, sueldo_imponible, cantidad=1):
    """Calcula el monto en pesos de un haber/descuento según su clase.

    - Fijo / Valor diario / Semana corrida: usa el monto configurado x cantidad.
    - Porcentaje: aplica el porcentaje sobre la base indicada (sueldo base o imponible).
    - Variable: usa el monto informado directamente (cantidad ya es el monto).
    """
    clase = haber["clase"]
    if clase == "Porcentaje":
        base = sueldo_imponible if haber["base_porcentaje"] == "Sueldo imponible" else sueldo_base
        return round(base * (haber["porcentaje"] / 100.0), 0)
    if clase == "Variable":
        return round(cantidad, 0)
    return round(haber["monto"] * cantidad, 0)
