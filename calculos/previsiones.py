"""
Cálculo de descuentos previsionales del trabajador: AFP, Salud (Isapre/Fonasa),
Seguro de Cesantía (AFC) y Ahorro Previsional Voluntario (APV).
"""


def calcular_tope_imponible_pesos(tope_uf, valor_uf):
    return round(tope_uf * valor_uf)


def calcular_afp(monto_imponible, factor_cotizacion_pct, tope_imponible_pesos, aplica_sis=False, sis_pct=0.0):
    """
    Cotización obligatoria AFP = 10% + comisión AFP (factor_cotizacion_pct), aplicado
    sobre el monto imponible topado. El SIS es de cargo del empleador (no descuento
    del trabajador) pero se informa referencialmente si aplica_sis=True.
    """
    base = min(monto_imponible, tope_imponible_pesos)
    cotizacion_obligatoria_pct = 10.0 + factor_cotizacion_pct
    monto_afp = round(base * cotizacion_obligatoria_pct / 100.0)
    monto_sis_patronal = round(base * sis_pct / 100.0) if aplica_sis else 0
    return {
        "base_imponible": base,
        "porcentaje_aplicado": cotizacion_obligatoria_pct,
        "monto_afp": monto_afp,
        "monto_sis_patronal": monto_sis_patronal,
    }


def calcular_salud(monto_imponible, tope_imponible_pesos, modalidad="7%", cotizacion_pactada=7.0, plan_uf=0.0,
                    valor_uf=0.0):
    """
    Calcula el descuento de salud según modalidad:
    - "7%": cotización legal mínima 7% sobre imponible topado.
    - "7%+UF" / "UF": plan pactado en UF, convertido a pesos (no puede ser menor al 7% legal).
    - "Pesos": plan pactado fijo en pesos.
    """
    base = min(monto_imponible, tope_imponible_pesos)
    minimo_legal = round(base * 7.0 / 100.0)

    if modalidad == "Pesos":
        monto = max(minimo_legal, round(cotizacion_pactada))
    elif modalidad in ("UF", "7%+UF", "7%+UF+Pesos"):
        monto_uf_pesos = round(plan_uf * valor_uf)
        monto = max(minimo_legal, monto_uf_pesos)
    else:  # "7%" u otro
        pct = max(7.0, cotizacion_pactada)
        monto = round(base * pct / 100.0)

    return {
        "base_imponible": base,
        "minimo_legal": minimo_legal,
        "monto_salud": monto,
    }


def calcular_afc(monto_imponible, tope_imponible_pesos, tipo_contrato="Indefinido"):
    """
    Seguro de Cesantía (AFC): descuento del trabajador solo aplica a contratos
    indefinidos (0.6%). En contratos a plazo fijo no hay descuento al trabajador.
    """
    base = min(monto_imponible, tope_imponible_pesos)
    if tipo_contrato == "Indefinido":
        pct_trabajador = 0.6
        pct_empleador = 2.4
    else:
        pct_trabajador = 0.0
        pct_empleador = 3.0

    monto_trabajador = round(base * pct_trabajador / 100.0)
    monto_empleador = round(base * pct_empleador / 100.0)

    return {
        "base_imponible": base,
        "monto_trabajador": monto_trabajador,
        "monto_empleador": monto_empleador,
    }


def calcular_apv(monto_apv_pesos, tope_mensual_uf, valor_uf):
    tope_pesos = round(tope_mensual_uf * valor_uf)
    return min(monto_apv_pesos, tope_pesos)
