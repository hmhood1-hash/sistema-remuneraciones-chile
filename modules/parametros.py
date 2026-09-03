# -*- coding: utf-8 -*-
"""Gestión de Parámetros, Factores Mensuales, Tramos de Cargas e Impuesto Único."""
from database.conexion import conexion_bd


# ---------------------------------------------------------------------------
# Parámetros generales (fila única id=1)
# ---------------------------------------------------------------------------
def obtener_parametros(ruta_bd=None):
    with conexion_bd(ruta_bd) as conexion:
        cursor = conexion.execute("SELECT * FROM parametros WHERE id = 1")
        fila = cursor.fetchone()
        return dict(fila) if fila else None


def actualizar_parametros(datos, ruta_bd=None):
    campos = list(datos.keys())
    valores = list(datos.values())
    with conexion_bd(ruta_bd) as conexion:
        conexion.execute(
            "UPDATE parametros SET {} WHERE id = 1".format(
                ", ".join("{} = ?".format(campo) for campo in campos)
            ),
            valores,
        )


# ---------------------------------------------------------------------------
# Factores mensuales (UTM / UF por año-mes)
# ---------------------------------------------------------------------------
def guardar_factor_mensual(anio, mes, factor, utm, uf, ruta_bd=None):
    with conexion_bd(ruta_bd) as conexion:
        conexion.execute(
            "INSERT INTO factor_mensual (anio, mes, factor, utm, uf) VALUES (?, ?, ?, ?, ?) "
            "ON CONFLICT(anio, mes) DO UPDATE SET factor = excluded.factor, "
            "utm = excluded.utm, uf = excluded.uf",
            (anio, mes, factor, utm, uf),
        )


def obtener_factor_mensual(anio, mes, ruta_bd=None):
    with conexion_bd(ruta_bd) as conexion:
        cursor = conexion.execute(
            "SELECT * FROM factor_mensual WHERE anio = ? AND mes = ?", (anio, mes)
        )
        fila = cursor.fetchone()
        return dict(fila) if fila else None


def listar_factores_anio(anio, ruta_bd=None):
    with conexion_bd(ruta_bd) as conexion:
        cursor = conexion.execute(
            "SELECT * FROM factor_mensual WHERE anio = ? ORDER BY mes", (anio,)
        )
        return [dict(fila) for fila in cursor.fetchall()]


# ---------------------------------------------------------------------------
# Tramos de cargas familiares
# ---------------------------------------------------------------------------
def listar_tramos_carga_familiar(ruta_bd=None):
    with conexion_bd(ruta_bd) as conexion:
        cursor = conexion.execute("SELECT * FROM tramo_carga_familiar ORDER BY tramo")
        return [dict(fila) for fila in cursor.fetchall()]


def actualizar_tramo_carga_familiar(tramo, datos, ruta_bd=None):
    campos = list(datos.keys())
    valores = list(datos.values())
    valores.append(tramo)
    with conexion_bd(ruta_bd) as conexion:
        conexion.execute(
            "UPDATE tramo_carga_familiar SET {} WHERE tramo = ?".format(
                ", ".join("{} = ?".format(campo) for campo in campos)
            ),
            valores,
        )


def obtener_valor_carga_familiar(ingreso_imponible, ruta_bd=None):
    """Determina el valor por carga familiar según el tramo de ingreso imponible."""
    tramos = listar_tramos_carga_familiar(ruta_bd)
    for tramo in sorted(tramos, key=lambda t: t["desde"]):
        hasta = tramo["hasta"]
        if hasta is None or ingreso_imponible <= hasta:
            if ingreso_imponible >= tramo["desde"]:
                return tramo["valor"]
    return 0


# ---------------------------------------------------------------------------
# Tramos de Impuesto Único
# ---------------------------------------------------------------------------
def listar_tramos_impuesto_unico(ruta_bd=None):
    with conexion_bd(ruta_bd) as conexion:
        cursor = conexion.execute("SELECT * FROM tramo_impuesto_unico ORDER BY tramo")
        return [dict(fila) for fila in cursor.fetchall()]


def actualizar_tramo_impuesto_unico(tramo, datos, ruta_bd=None):
    campos = list(datos.keys())
    valores = list(datos.values())
    valores.append(tramo)
    with conexion_bd(ruta_bd) as conexion:
        conexion.execute(
            "UPDATE tramo_impuesto_unico SET {} WHERE tramo = ?".format(
                ", ".join("{} = ?".format(campo) for campo in campos)
            ),
            valores,
        )


# ---------------------------------------------------------------------------
# Tipos de contrato y causales de finiquito
# ---------------------------------------------------------------------------
def listar_tipos_contrato(ruta_bd=None):
    with conexion_bd(ruta_bd) as conexion:
        cursor = conexion.execute("SELECT * FROM tipo_contrato ORDER BY codigo")
        return [dict(fila) for fila in cursor.fetchall()]


def crear_tipo_contrato(codigo, descripcion, ruta_bd=None):
    with conexion_bd(ruta_bd) as conexion:
        conexion.execute(
            "INSERT INTO tipo_contrato (codigo, descripcion) VALUES (?, ?)",
            (codigo, descripcion),
        )


def listar_causales_finiquito(ruta_bd=None):
    with conexion_bd(ruta_bd) as conexion:
        cursor = conexion.execute("SELECT * FROM causal_finiquito ORDER BY codigo")
        return [dict(fila) for fila in cursor.fetchall()]


def crear_causal_finiquito(codigo, descripcion, ruta_bd=None):
    with conexion_bd(ruta_bd) as conexion:
        conexion.execute(
            "INSERT INTO causal_finiquito (codigo, descripcion) VALUES (?, ?)",
            (codigo, descripcion),
        )
