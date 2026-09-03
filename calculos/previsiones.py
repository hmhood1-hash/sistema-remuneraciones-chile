# -*- coding: utf-8 -*-
"""Cálculo de descuentos previsionales: AFP, Salud y Seguro de Cesantía."""

PORCENTAJE_AFP = 10.0  # Cotización obligatoria de AFP (10% del imponible)
PORCENTAJE_SALUD_MINIMO = 7.0  # Cotización de salud legal mínima


def tope_imponible_pesos(tope_uf, valor_uf):
    """Convierte el tope imponible (en UF) a pesos según el valor de la UF."""
    return tope_uf * valor_uf


def calcular_imponible_afp(total_imponible, tope_uf, valor_uf):
    """Aplica el tope imponible de AFP (en UF) al total imponible del trabajador."""
    tope_pesos = tope_imponible_pesos(tope_uf, valor_uf)
    return min(total_imponible, tope_pesos) if tope_pesos > 0 else total_imponible


def calcular_afp(total_imponible, factor_cotizacion_afp, tope_uf, valor_uf,
                  tipo_trabajador="Activo No Pensionado"):
    """Calcula el descuento total de AFP (cotización 10% + comisión AFP).

    ``factor_cotizacion_afp`` corresponde al porcentaje total informado por la
    AFP (cotización obligatoria + comisión). Si el trabajador está pensionado
    y no cotiza, el descuento es 0.
    """
    if tipo_trabajador == "Pensionado no cotiza":
        return 0.0

    imponible = calcular_imponible_afp(total_imponible, tope_uf, valor_uf)
    return round(imponible * (factor_cotizacion_afp / 100.0), 0)


def calcular_salud(total_imponible, tope_uf, valor_uf, porcentaje_pactado=None,
                    tipo_trabajador="Activo No Pensionado"):
    """Calcula el descuento de salud (Fonasa/Isapre), aplicando el tope legal.

    ``porcentaje_pactado`` permite indicar un plan Isapre pactado superior al
    7% legal. Si no se indica, se usa el mínimo legal (7%).
    """
    if tipo_trabajador == "Pensionado no cotiza":
        return 0.0

    porcentaje = porcentaje_pactado if porcentaje_pactado else PORCENTAJE_SALUD_MINIMO
    imponible = calcular_imponible_afp(total_imponible, tope_uf, valor_uf)
    return round(imponible * (porcentaje / 100.0), 0)


def calcular_seguro_cesantia(total_imponible, tope_uf, valor_uf, seguro_cesantia,
                              porcentaje_trabajador):
    """Calcula el descuento de Seguro de Cesantía (AFC) para el trabajador.

    Los contratos a plazo fijo no cotizan seguro de cesantía por parte del
    trabajador (según la ley, sólo el empleador aporta en ese caso).
    """
    if seguro_cesantia == "Plazo Fijo":
        return 0.0

    imponible = calcular_imponible_afp(total_imponible, tope_uf, valor_uf)
    return round(imponible * (porcentaje_trabajador / 100.0), 0)
