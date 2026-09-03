# -*- coding: utf-8 -*-
"""Gestión de Instituciones Previsionales: AFP, Isapres, CCAF, Mutuales y Ahorro."""
from database.conexion import conexion_bd

_TABLAS = {
    "afp": ("codigo_afp", ("codigo_afp", "nombre", "factor_cotizacion", "sistema_previsional")),
    "isapre": ("codigo_isapre", ("codigo_isapre", "nombre")),
    "ccaf": ("codigo_ccaf", ("codigo_ccaf", "nombre")),
    "mutual": ("codigo_mutual", ("codigo_mutual", "nombre")),
    "ahorro_previsional": ("codigo_ahorro", ("codigo_ahorro", "nombre")),
}


def _crear(tabla, datos, ruta_bd=None):
    clave, campos = _TABLAS[tabla]
    valores = tuple(datos.get(campo) for campo in campos)
    with conexion_bd(ruta_bd) as conexion:
        conexion.execute(
            "INSERT INTO {} ({}) VALUES ({})".format(
                tabla, ", ".join(campos), ", ".join(["?"] * len(campos))
            ),
            valores,
        )


def _actualizar(tabla, codigo, datos, ruta_bd=None):
    clave, _ = _TABLAS[tabla]
    campos = list(datos.keys())
    valores = list(datos.values())
    valores.append(codigo)
    with conexion_bd(ruta_bd) as conexion:
        conexion.execute(
            "UPDATE {} SET {} WHERE {} = ?".format(
                tabla, ", ".join("{} = ?".format(campo) for campo in campos), clave
            ),
            valores,
        )


def _eliminar(tabla, codigo, ruta_bd=None):
    clave, _ = _TABLAS[tabla]
    with conexion_bd(ruta_bd) as conexion:
        conexion.execute("DELETE FROM {} WHERE {} = ?".format(tabla, clave), (codigo,))


def _listar(tabla, ruta_bd=None):
    clave, _ = _TABLAS[tabla]
    with conexion_bd(ruta_bd) as conexion:
        cursor = conexion.execute("SELECT * FROM {} ORDER BY {}".format(tabla, clave))
        return [dict(fila) for fila in cursor.fetchall()]


def _obtener(tabla, codigo, ruta_bd=None):
    clave, _ = _TABLAS[tabla]
    with conexion_bd(ruta_bd) as conexion:
        cursor = conexion.execute(
            "SELECT * FROM {} WHERE {} = ?".format(tabla, clave), (codigo,)
        )
        fila = cursor.fetchone()
        return dict(fila) if fila else None


# AFP
def crear_afp(datos, ruta_bd=None):
    return _crear("afp", datos, ruta_bd)


def actualizar_afp(codigo_afp, datos, ruta_bd=None):
    return _actualizar("afp", codigo_afp, datos, ruta_bd)


def eliminar_afp(codigo_afp, ruta_bd=None):
    return _eliminar("afp", codigo_afp, ruta_bd)


def listar_afp(ruta_bd=None):
    return _listar("afp", ruta_bd)


def obtener_afp(codigo_afp, ruta_bd=None):
    return _obtener("afp", codigo_afp, ruta_bd)


# Isapre
def crear_isapre(datos, ruta_bd=None):
    return _crear("isapre", datos, ruta_bd)


def actualizar_isapre(codigo_isapre, datos, ruta_bd=None):
    return _actualizar("isapre", codigo_isapre, datos, ruta_bd)


def eliminar_isapre(codigo_isapre, ruta_bd=None):
    return _eliminar("isapre", codigo_isapre, ruta_bd)


def listar_isapres(ruta_bd=None):
    return _listar("isapre", ruta_bd)


# CCAF
def crear_ccaf(datos, ruta_bd=None):
    return _crear("ccaf", datos, ruta_bd)


def actualizar_ccaf(codigo_ccaf, datos, ruta_bd=None):
    return _actualizar("ccaf", codigo_ccaf, datos, ruta_bd)


def eliminar_ccaf(codigo_ccaf, ruta_bd=None):
    return _eliminar("ccaf", codigo_ccaf, ruta_bd)


def listar_ccaf(ruta_bd=None):
    return _listar("ccaf", ruta_bd)


# Mutual
def crear_mutual(datos, ruta_bd=None):
    return _crear("mutual", datos, ruta_bd)


def actualizar_mutual(codigo_mutual, datos, ruta_bd=None):
    return _actualizar("mutual", codigo_mutual, datos, ruta_bd)


def eliminar_mutual(codigo_mutual, ruta_bd=None):
    return _eliminar("mutual", codigo_mutual, ruta_bd)


def listar_mutuales(ruta_bd=None):
    return _listar("mutual", ruta_bd)


# Ahorro previsional
def crear_ahorro_previsional(datos, ruta_bd=None):
    return _crear("ahorro_previsional", datos, ruta_bd)


def actualizar_ahorro_previsional(codigo_ahorro, datos, ruta_bd=None):
    return _actualizar("ahorro_previsional", codigo_ahorro, datos, ruta_bd)


def eliminar_ahorro_previsional(codigo_ahorro, ruta_bd=None):
    return _eliminar("ahorro_previsional", codigo_ahorro, ruta_bd)


def listar_ahorros_previsionales(ruta_bd=None):
    return _listar("ahorro_previsional", ruta_bd)
