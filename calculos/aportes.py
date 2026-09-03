# -*- coding: utf-8 -*-
"""Cálculo de aportes patronales (de cargo del empleador, sin descontar al trabajador)."""

from calculos.previsiones import calcular_imponible_afp


def calcular_aporte_sis(total_imponible, tope_uf, valor_uf, sis_pct, aplica_sis):
    """Calcula el aporte del Seguro de Invalidez y Sobrevivencia (SIS) patronal."""
    if aplica_sis != "S":
        return 0.0
    imponible = calcular_imponible_afp(total_imponible, tope_uf, valor_uf)
    return round(imponible * (sis_pct / 100.0), 0)


def calcular_aporte_afc_empleador(total_imponible, tope_uf, valor_uf, seguro_cesantia,
                                   pct_indefinido, pct_plazo_fijo):
    """Calcula el aporte patronal de Seguro de Cesantía según tipo de contrato."""
    imponible = calcular_imponible_afp(total_imponible, tope_uf, valor_uf)
    porcentaje = pct_plazo_fijo if seguro_cesantia == "Plazo Fijo" else pct_indefinido
    return round(imponible * (porcentaje / 100.0), 0)


def calcular_aporte_ccaf(total_imponible, ccaf_pct):
    """Calcula el aporte patronal a la Caja de Compensación de Asignación Familiar."""
    return round(total_imponible * (ccaf_pct / 100.0), 0)


def calcular_aporte_patronal_afp(total_imponible, tope_uf, valor_uf, aporte_patronal_pct):
    """Calcula el aporte patronal adicional (donde aplique, sistema antiguo)."""
    imponible = calcular_imponible_afp(total_imponible, tope_uf, valor_uf)
    return round(imponible * (aporte_patronal_pct / 100.0), 0)


def calcular_aportes_patronales(total_imponible, tope_uf, valor_uf, parametros,
                                 aplica_sis, seguro_cesantia):
    """Calcula todos los aportes patronales y devuelve un resumen con el total.

    ``parametros`` es un dict/Row con los campos de la tabla ``parametros``.
    """
    aporte_sis = calcular_aporte_sis(
        total_imponible, tope_uf, valor_uf, parametros["sis_empleador_pct"], aplica_sis
    )
    aporte_afc = calcular_aporte_afc_empleador(
        total_imponible,
        tope_uf,
        valor_uf,
        seguro_cesantia,
        parametros["afc_empleador_indefinido_pct"],
        parametros["afc_empleador_plazo_fijo_pct"],
    )
    aporte_ccaf = calcular_aporte_ccaf(total_imponible, parametros["ccaf_pct"])
    aporte_patronal_afp = calcular_aporte_patronal_afp(
        total_imponible, tope_uf, valor_uf, parametros["aporte_patronal_pct"]
    )

    total = aporte_sis + aporte_afc + aporte_ccaf + aporte_patronal_afp

    return {
        "aporte_patronal_afp": aporte_patronal_afp,
        "aporte_sis": aporte_sis,
        "aporte_afc_empleador": aporte_afc,
        "aporte_ccaf": aporte_ccaf,
        "total_aportes_patronales": total,
    }
