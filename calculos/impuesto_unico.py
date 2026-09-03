"""
Cálculo de Impuesto Único (tabla progresiva en UTM)
"""
from database.models import fetch_all, fetch_one


def calcular_impuesto_unico(sueldo_imponible, anio, cargas_familiares=0):
    """
    Calcula el impuesto único aplicando tabla progresiva.
    Fórmula: (sueldo_imponible × factor) - rebaja + (cargas × monto_carga)
    
    Args:
        sueldo_imponible: Sueldo base para cálculo de impuesto
        anio: Año de aplicación
        cargas_familiares: Número de cargas familiares
    
    Returns:
        Monto de impuesto único (nunca negativo)
    """
    if sueldo_imponible <= 0:
        return 0
    
    # Obtener tramo de impuesto correspondiente
    tramo = fetch_one(
        "impuesto_unico",
        {"anio": anio}
    )
    
    if not tramo:
        # Si no hay tabla para el año, retornar 0
        return 0
    
    # Buscar el tramo correcto
    tramos = fetch_all("impuesto_unico", {"anio": anio})
    tramo_aplicable = None
    
    for t in tramos:
        if sueldo_imponible >= t["sueldo_desde"] and sueldo_imponible <= t["sueldo_hasta"]:
            tramo_aplicable = t
            break
    
    if not tramo_aplicable:
        # Usar el último tramo si el sueldo es superior
        tramo_aplicable = tramos[-1] if tramos else None
    
    if not tramo_aplicable:
        return 0
    
    # Fórmula: (sueldo × factor) - rebaja
    impuesto = (sueldo_imponible * tramo_aplicable["factor"]) - tramo_aplicable["rebaja"]
    
    # Agregar valor de cargas familiares (si aplica)
    if cargas_familiares > 0:
        # Obtener valor de carga familiar según tramo de sueldo
        cargas_tramo = fetch_one(
            "tramo_carga_familiar",
            {"sueldo_desde": sueldo_imponible}
        )
        if cargas_tramo:
            impuesto += cargas_familiares * cargas_tramo["valor_carga"]
    
    # El impuesto nunca puede ser negativo
    return max(0, impuesto)
