"""
Cálculo de aportes patronales
"""
from database.models import fetch_one


def calcular_aporte_patronal(sueldo_base, anio, mes):
    """
    Calcula aporte patronal básico (13% - 15%).
    
    Args:
        sueldo_base: Sueldo base del trabajador
        anio, mes: Para obtener parámetros
    
    Returns:
        Monto de aporte patronal
    """
    param = fetch_one("parametro", {"anio": anio, "mes": mes})
    
    if param and param["aporte_patronal_porcentaje"]:
        porcentaje = param["aporte_patronal_porcentaje"]
    else:
        porcentaje = 13.0  # Por defecto 13%
    
    monto = sueldo_base * (porcentaje / 100)
    return monto


def calcular_aporte_afc_empleador(sueldo_base, tipo_contrato, anio, mes):
    """
    Calcula aporte del empleador para AFC.
    
    Args:
        sueldo_base: Sueldo base
        tipo_contrato: Tipo (Indefinido, Plazo Fijo)
        anio, mes: Para obtener parámetros
    
    Returns:
        Monto de aporte AFC empleador
    """
    param = fetch_one("parametro", {"anio": anio, "mes": mes})
    
    if tipo_contrato == "Indefinido" and param:
        porcentaje = param.get("afc_empleador_indefinido_porcentaje", 2.4)
    elif tipo_contrato == "Plazo Fijo" and param:
        porcentaje = param.get("afc_empleador_plazo_fijo_porcentaje", 3.0)
    else:
        porcentaje = 2.4
    
    monto = sueldo_base * (porcentaje / 100)
    return monto


def calcular_aporte_sis(sueldo_base, aplica_sis, anio, mes):
    """
    Calcula aporte para Seguro de Invalidez y Sobrevivencia (SIS).
    
    Args:
        sueldo_base: Sueldo base
        aplica_sis: S/N
        anio, mes: Para obtener parámetros
    
    Returns:
        Monto de SIS empleador
    """
    if aplica_sis != "S":
        return 0
    
    param = fetch_one("parametro", {"anio": anio, "mes": mes})
    
    if param and param["sis_empleador_porcentaje"]:
        porcentaje = param["sis_empleador_porcentaje"]
    else:
        porcentaje = 1.47  # Por defecto
    
    monto = sueldo_base * (porcentaje / 100)
    return monto


def calcular_aporte_ccaf(sueldo_base, anio, mes):
    """
    Calcula aporte para CCAF.
    
    Args:
        sueldo_base: Sueldo base
        anio, mes: Para obtener parámetros
    
    Returns:
        Monto de CCAF
    """
    param = fetch_one("parametro", {"anio": anio, "mes": mes})
    
    if param and param["ccaf_porcentaje"]:
        porcentaje = param["ccaf_porcentaje"]
    else:
        porcentaje = 2.0  # Por defecto
    
    monto = sueldo_base * (porcentaje / 100)
    return monto
