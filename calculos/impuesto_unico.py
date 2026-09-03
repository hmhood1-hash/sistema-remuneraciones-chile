"""
Cálculo del Impuesto Único de Segunda Categoría según tabla progresiva por tramos
expresada en UTM.
"""


def obtener_tramo(monto_utm, tramos):
    """Retorna el tramo (dict) que corresponde al monto en UTM dado."""
    for tramo in tramos:
        desde = tramo["desde_utm"]
        hasta = tramo["hasta_utm"]
        if hasta is None:
            if monto_utm >= desde:
                return tramo
        elif desde <= monto_utm < hasta:
            return tramo
    return tramos[-1] if tramos else None


def calcular_impuesto_unico(base_tributable, valor_utm, tramos):
    """
    Calcula el Impuesto Único de Segunda Categoría.

    base_tributable: monto tributable mensual en pesos.
    valor_utm: valor de la UTM del mes en pesos.
    tramos: lista de dicts con keys desde_utm, hasta_utm, factor, rebaja_utm.

    Retorna un dict con el detalle del cálculo.
    """
    if base_tributable <= 0 or valor_utm <= 0 or not tramos:
        return {
            "base_tributable_utm": 0.0,
            "tramo": None,
            "factor": 0.0,
            "rebaja_utm": 0.0,
            "impuesto_utm": 0.0,
            "impuesto_pesos": 0.0,
        }

    base_utm = base_tributable / valor_utm
    tramo = obtener_tramo(base_utm, tramos)
    factor = tramo["factor"] if tramo else 0.0
    rebaja_utm = tramo["rebaja_utm"] if tramo else 0.0

    impuesto_utm = max(0.0, base_utm * factor - rebaja_utm)
    impuesto_pesos = round(impuesto_utm * valor_utm)

    return {
        "base_tributable_utm": round(base_utm, 4),
        "tramo": tramo["tramo"] if tramo else None,
        "factor": factor,
        "rebaja_utm": rebaja_utm,
        "impuesto_utm": round(impuesto_utm, 4),
        "impuesto_pesos": impuesto_pesos,
    }
