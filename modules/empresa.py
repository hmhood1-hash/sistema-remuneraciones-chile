# -*- coding: utf-8 -*-
"""CRUD de Empresas, Sucursales y Centros de Costo."""
from database.conexion import conexion_bd


# ---------------------------------------------------------------------------
# Empresa
# ---------------------------------------------------------------------------
def crear_empresa(datos, ruta_bd=None):
    campos = (
        "rut", "razon_social", "calle", "numero", "depto", "poblacion_villa",
        "comuna", "ciudad", "region", "correo", "fono", "giro_comercial",
        "codigo_actividad_economica", "rep_legal_rut", "rep_legal_nombres",
        "rep_legal_apellido_paterno", "rep_legal_apellido_materno",
    )
    valores = tuple(datos.get(campo) for campo in campos)
    with conexion_bd(ruta_bd) as conexion:
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO empresa ({}) VALUES ({})".format(
                ", ".join(campos), ", ".join(["?"] * len(campos))
            ),
            valores,
        )
        return cursor.lastrowid


def actualizar_empresa(codigo_empresa, datos, ruta_bd=None):
    campos = list(datos.keys())
    valores = list(datos.values())
    valores.append(codigo_empresa)
    with conexion_bd(ruta_bd) as conexion:
        conexion.execute(
            "UPDATE empresa SET {} WHERE codigo_empresa = ?".format(
                ", ".join("{} = ?".format(campo) for campo in campos)
            ),
            valores,
        )


def eliminar_empresa(codigo_empresa, ruta_bd=None):
    with conexion_bd(ruta_bd) as conexion:
        conexion.execute("DELETE FROM empresa WHERE codigo_empresa = ?", (codigo_empresa,))


def listar_empresas(ruta_bd=None):
    with conexion_bd(ruta_bd) as conexion:
        cursor = conexion.execute("SELECT * FROM empresa ORDER BY razon_social")
        return [dict(fila) for fila in cursor.fetchall()]


def obtener_empresa(codigo_empresa, ruta_bd=None):
    with conexion_bd(ruta_bd) as conexion:
        cursor = conexion.execute(
            "SELECT * FROM empresa WHERE codigo_empresa = ?", (codigo_empresa,)
        )
        fila = cursor.fetchone()
        return dict(fila) if fila else None


# ---------------------------------------------------------------------------
# Sucursales
# ---------------------------------------------------------------------------
def crear_sucursal(datos, ruta_bd=None):
    campos = ("codigo_empresa", "nombre", "direccion", "region", "ciudad", "comuna", "fono")
    valores = tuple(datos.get(campo) for campo in campos)
    with conexion_bd(ruta_bd) as conexion:
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO sucursal ({}) VALUES ({})".format(
                ", ".join(campos), ", ".join(["?"] * len(campos))
            ),
            valores,
        )
        return cursor.lastrowid


def actualizar_sucursal(codigo_sucursal, datos, ruta_bd=None):
    campos = list(datos.keys())
    valores = list(datos.values())
    valores.append(codigo_sucursal)
    with conexion_bd(ruta_bd) as conexion:
        conexion.execute(
            "UPDATE sucursal SET {} WHERE codigo_sucursal = ?".format(
                ", ".join("{} = ?".format(campo) for campo in campos)
            ),
            valores,
        )


def eliminar_sucursal(codigo_sucursal, ruta_bd=None):
    with conexion_bd(ruta_bd) as conexion:
        conexion.execute("DELETE FROM sucursal WHERE codigo_sucursal = ?", (codigo_sucursal,))


def listar_sucursales(codigo_empresa=None, ruta_bd=None):
    with conexion_bd(ruta_bd) as conexion:
        if codigo_empresa:
            cursor = conexion.execute(
                "SELECT * FROM sucursal WHERE codigo_empresa = ? ORDER BY nombre",
                (codigo_empresa,),
            )
        else:
            cursor = conexion.execute("SELECT * FROM sucursal ORDER BY nombre")
        return [dict(fila) for fila in cursor.fetchall()]


# ---------------------------------------------------------------------------
# Centros de Costo
# ---------------------------------------------------------------------------
def crear_centro_costo(datos, ruta_bd=None):
    with conexion_bd(ruta_bd) as conexion:
        conexion.execute(
            "INSERT INTO centro_costo (codigo_centro_costo, descripcion, codigo_empresa) "
            "VALUES (?, ?, ?)",
            (
                datos.get("codigo_centro_costo"),
                datos.get("descripcion"),
                datos.get("codigo_empresa"),
            ),
        )


def actualizar_centro_costo(codigo_centro_costo, datos, ruta_bd=None):
    campos = list(datos.keys())
    valores = list(datos.values())
    valores.append(codigo_centro_costo)
    with conexion_bd(ruta_bd) as conexion:
        conexion.execute(
            "UPDATE centro_costo SET {} WHERE codigo_centro_costo = ?".format(
                ", ".join("{} = ?".format(campo) for campo in campos)
            ),
            valores,
        )


def eliminar_centro_costo(codigo_centro_costo, ruta_bd=None):
    with conexion_bd(ruta_bd) as conexion:
        conexion.execute(
            "DELETE FROM centro_costo WHERE codigo_centro_costo = ?", (codigo_centro_costo,)
        )


def listar_centros_costo(codigo_empresa=None, ruta_bd=None):
    with conexion_bd(ruta_bd) as conexion:
        if codigo_empresa:
            cursor = conexion.execute(
                "SELECT * FROM centro_costo WHERE codigo_empresa = ? ORDER BY codigo_centro_costo",
                (codigo_empresa,),
            )
        else:
            cursor = conexion.execute("SELECT * FROM centro_costo ORDER BY codigo_centro_costo")
        return [dict(fila) for fila in cursor.fetchall()]
