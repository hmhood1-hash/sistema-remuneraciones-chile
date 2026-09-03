# -*- coding: utf-8 -*-
"""Cálculo del Impuesto Único de Segunda Categoría (tabla progresiva mensual)."""


def obtener_tramo(base_tributable_utm, tramos):
    """Busca el tramo aplicable para una base tributable expresada en UTM.

    ``tramos`` es una lista de dicts con llaves: tramo, desde_utm, hasta_utm,
    factor, rebaja_utm (``hasta_utm`` puede ser ``None`` para el último tramo).
    """
    tramos_ordenados = sorted(tramos, key=lambda t: t["desde_utm"])
    for tramo in tramos_ordenados:
        hasta = tramo["hasta_utm"]
        if hasta is None or base_tributable_utm <= hasta:
            if base_tributable_utm >= tramo["desde_utm"]:
                return tramo
    return tramos_ordenados[-1] if tramos_ordenados else None


def calcular_impuesto_unico(base_tributable, valor_utm, tramos, monto_cargas_familiares=0):
    """Calcula el Impuesto Único mensual aplicando la fórmula progresiva chilena.

    Fórmula: (base_imponible x factor) - rebaja - cargas_familiares
    El resultado nunca puede ser negativo.

    Parámetros:
        base_tributable: base imponible tributable en pesos.
        valor_utm: valor de la UTM del mes correspondiente.
        tramos: lista de tramos de impuesto único (ver :func:`obtener_tramo`).
        monto_cargas_familiares: monto total a rebajar por cargas familiares.
    """
    if valor_utm <= 0 or base_tributable <= 0 or not tramos:
        return 0.0

    base_utm = base_tributable / valor_utm
    tramo = obtener_tramo(base_utm, tramos)
    if tramo is None:
        return 0.0

    factor = tramo["factor"]
    rebaja_utm = tramo["rebaja_utm"]

    impuesto_utm = (base_utm * factor) - rebaja_utm
    impuesto_pesos = impuesto_utm * valor_utm
    impuesto_pesos -= monto_cargas_familiares

    return round(max(impuesto_pesos, 0.0), 0)
