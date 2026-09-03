"""
Cálculo de aportes patronales (de cargo del empleador): SIS, AFC empleador,
CCAF y Mutual de seguridad.
"""


def calcular_aporte_sis(monto_imponible, tope_imponible_pesos, sis_pct, aplica_sis=True):
    if not aplica_sis:
        return 0
    base = min(monto_imponible, tope_imponible_pesos)
    return round(base * sis_pct / 100.0)


def calcular_aporte_afc_empleador(monto_imponible, tope_imponible_pesos, tipo_contrato="Indefinido",
                                   pct_indefinido=2.4, pct_plazo_fijo=3.0):
    base = min(monto_imponible, tope_imponible_pesos)
    pct = pct_indefinido if tipo_contrato == "Indefinido" else pct_plazo_fijo
    return round(base * pct / 100.0)


def calcular_aporte_ccaf(monto_imponible, tope_imponible_pesos, ccaf_pct):
    base = min(monto_imponible, tope_imponible_pesos)
    return round(base * ccaf_pct / 100.0)


def calcular_aporte_mutual(monto_imponible, tope_imponible_pesos, mutual_pct):
    base = min(monto_imponible, tope_imponible_pesos)
    return round(base * mutual_pct / 100.0)


def calcular_aportes_patronales(monto_imponible, tope_imponible_pesos, parametros, tipo_contrato="Indefinido",
                                 aplica_sis=True):
    """
    Calcula el total de aportes patronales según los parámetros configurados
    (dict de la tabla `parametros`).
    """
    sis = calcular_aporte_sis(
        monto_imponible, tope_imponible_pesos, parametros.get("sis_empleador_pct", 0), aplica_sis
    )
    afc = calcular_aporte_afc_empleador(
        monto_imponible, tope_imponible_pesos, tipo_contrato,
        parametros.get("afc_empleador_indefinido_pct", 2.4),
        parametros.get("afc_empleador_pfijo_pct", 3.0),
    )
    ccaf = calcular_aporte_ccaf(monto_imponible, tope_imponible_pesos, parametros.get("ccaf_pct", 0))
    mutual = calcular_aporte_mutual(monto_imponible, tope_imponible_pesos, parametros.get("aporte_patronal_pct", 0))

    total = sis + afc + ccaf + mutual
    return {
        "aporte_sis": sis,
        "aporte_afc": afc,
        "aporte_ccaf": ccaf,
        "aporte_mutual": mutual,
        "total_aportes_patronales": total,
    }
