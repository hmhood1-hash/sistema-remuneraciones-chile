# -*- coding: utf-8 -*-
"""Cálculo y gestión de Finiquitos."""
from datetime import datetime

from database.conexion import conexion_bd

CAMPOS = ("codigo_empleado", "fecha_inicio", "fecha_termino", "cargo", "codigo_causal")

CAUSALES_CON_INDEMNIZACION = {"ART161"}  # Necesidades de la empresa: da derecho a indemnización.
TOPE_ANIOS_INDEMNIZACION = 11


def _anios_servicio(fecha_inicio, fecha_termino):
    inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
    termino = datetime.strptime(fecha_termino, "%Y-%m-%d")
    dias = (termino - inicio).days
    return dias / 365.25


def calcular_finiquito(sueldo_base, fecha_inicio, fecha_termino, codigo_causal,
                        dias_vacaciones_pendientes=0, aviso_previo_pagado=False):
    """Calcula el monto total de un finiquito (indemnizaciones + vacaciones proporcionales).

    Incluye:
      - Indemnización por años de servicio (1 mes de sueldo por año, tope 11 años),
        sólo si la causal corresponde a "Necesidades de la Empresa".
      - Indemnización sustitutiva del aviso previo (1 mes), si no se avisó con 30 días
        de anticipación y la causal lo requiere.
      - Vacaciones proporcionales no tomadas.
    """
    anios = _anios_servicio(fecha_inicio, fecha_termino)
    anios_para_indemnizacion = min(int(anios), TOPE_ANIOS_INDEMNIZACION)

    indemnizacion_anos_servicio = 0.0
    indemnizacion_aviso_previo = 0.0

    if codigo_causal in CAUSALES_CON_INDEMNIZACION and anios >= 1:
        indemnizacion_anos_servicio = sueldo_base * anios_para_indemnizacion
        if not aviso_previo_pagado:
            indemnizacion_aviso_previo = sueldo_base

    valor_dia = sueldo_base / 30.0
    vacaciones_proporcionales = round(valor_dia * dias_vacaciones_pendientes, 0)

    total = indemnizacion_anos_servicio + indemnizacion_aviso_previo + vacaciones_proporcionales

    return {
        "anios_servicio": round(anios, 2),
        "indemnizacion_anos_servicio": round(indemnizacion_anos_servicio, 0),
        "indemnizacion_aviso_previo": round(indemnizacion_aviso_previo, 0),
        "vacaciones_proporcionales": vacaciones_proporcionales,
        "monto_total": round(total, 0),
    }


def crear_finiquito(datos, monto_total, ruta_bd=None):
    valores = tuple(datos.get(campo) for campo in CAMPOS)
    fecha_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with conexion_bd(ruta_bd) as conexion:
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO finiquito ({}, monto_total, fecha_creacion) VALUES ({}, ?, ?)".format(
                ", ".join(CAMPOS), ", ".join(["?"] * len(CAMPOS))
            ),
            valores + (monto_total, fecha_creacion),
        )
        return cursor.lastrowid


def listar_finiquitos(codigo_empleado=None, ruta_bd=None):
    with conexion_bd(ruta_bd) as conexion:
        if codigo_empleado:
            cursor = conexion.execute(
                "SELECT * FROM finiquito WHERE codigo_empleado = ? ORDER BY fecha_creacion DESC",
                (codigo_empleado,),
            )
        else:
            cursor = conexion.execute("SELECT * FROM finiquito ORDER BY fecha_creacion DESC")
        return [dict(fila) for fila in cursor.fetchall()]


def obtener_finiquito(id_finiquito, ruta_bd=None):
    with conexion_bd(ruta_bd) as conexion:
        cursor = conexion.execute(
            "SELECT * FROM finiquito WHERE id_finiquito = ?", (id_finiquito,)
        )
        fila = cursor.fetchone()
        return dict(fila) if fila else None
