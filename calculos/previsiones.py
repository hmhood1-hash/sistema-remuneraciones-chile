"""
Cálculo de previsiones (AFP, Salud, AFC)
"""
from database.models import fetch_one


def calcular_afp(sueldo_imponible, afp_codigo, anio, mes):
    """
    Calcula descuento de AFP (10% estándar sobre imponible, aplica tope).
    
    Args:
        sueldo_imponible: Sueldo base para cálculo
        afp_codigo: Código de AFP
        anio, mes: Para obtener parámetros del período
    
    Returns:
        Monto de AFP a descontar
    """
    porcentaje_afp = 10.0  # 10% estándar en Chile
    monto = sueldo_imponible * (porcentaje_afp / 100)
    
    # Obtener parámetro de tope imponible AFP
    param = fetch_one("parametro", {"anio": anio, "mes": mes})
    if param and param["tope_imponible_afp_uf"] and param["uf"]:
        tope_pesos = param["tope_imponible_afp_uf"] * param["uf"]
        if sueldo_imponible > tope_pesos:
            monto = tope_pesos * (porcentaje_afp / 100)
    
    return monto


def calcular_salud(sueldo_imponible, isapre_codigo, modalidad, anio, mes):
    """
    Calcula descuento de salud (7% Fonasa o valor Isapre).
    
    Args:
        sueldo_imponible: Sueldo base
        isapre_codigo: Código de Isapre/Fonasa
        modalidad: Modalidad de salud (7%, UF, etc.)
        anio, mes: Para obtener parámetros
    
    Returns:
        Monto de salud a descontar
    """
    if modalidad == "7%" or isapre_codigo == "FONASA":
        porcentaje = 7.0
    else:
        porcentaje = 7.0  # Por defecto 7%
    
    monto = sueldo_imponible * (porcentaje / 100)
    
    # Aplicar tope si existe
    param = fetch_one("parametro", {"anio": anio, "mes": mes})
    if param and param["uf"]:
        # Tope típico: 2.25 UF
        tope_uf = 2.25
        tope_pesos = tope_uf * param["uf"]
        if monto > tope_pesos:
            monto = tope_pesos
    
    return monto


def calcular_afc(sueldo_base, tipo_trabajador, anio, mes):
    """
    Calcula Ahorro para Fondo de Cesantía (AFC).
    
    Args:
        sueldo_base: Sueldo base
        tipo_trabajador: Tipo (Indefinido, Plazo Fijo)
        anio, mes: Para obtener parámetros
    
    Returns:
        Monto de AFC a descontar
    """
    param = fetch_one("parametro", {"anio": anio, "mes": mes})
    
    if tipo_trabajador == "Indefinido" and param:
        # AFC trabajador indefinido: 0.6% (típico)
        porcentaje = param.get("afc_trabajador_indefinido_porcentaje", 0.6)
    elif param:
        porcentaje = 0.6  # Por defecto
    else:
        porcentaje = 0.6
    
    monto = sueldo_base * (porcentaje / 100)
    return monto


def calcular_seguro_cesantia(sueldo_imponible, tipo_seguro, anio, mes):
    """
    Calcula Seguro de Cesantía.
    
    Args:
        sueldo_imponible: Sueldo imponible
        tipo_seguro: Tipo (Plazo Fijo, Indefinido)
        anio, mes: Para obtener parámetros
    
    Returns:
        Monto de seguro de cesantía
    """
    # Porcentaje típico: 0.6% - 0.8% según tipo
    if tipo_seguro == "Plazo Fijo":
        porcentaje = 0.6
    else:
        porcentaje = 0.8  # Indefinido
    
    monto = sueldo_imponible * (porcentaje / 100)
    return monto
