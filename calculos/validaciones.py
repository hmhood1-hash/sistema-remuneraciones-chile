# -*- coding: utf-8 -*-
"""Validaciones de datos comunes: RUT chileno, fechas y montos."""
import re
from datetime import datetime


def limpiar_rut(rut):
    """Quita puntos, guiones y espacios, y deja el dígito verificador en mayúscula."""
    if rut is None:
        return ""
    return re.sub(r"[.\-\s]", "", str(rut)).upper()


def calcular_dv(rut_numero):
    """Calcula el dígito verificador de un RUT chileno (algoritmo módulo 11)."""
    rut_numero = int(rut_numero)
    suma = 0
    multiplicador = 2
    for digito in reversed(str(rut_numero)):
        suma += int(digito) * multiplicador
        multiplicador = multiplicador + 1 if multiplicador < 7 else 2
    resto = 11 - (suma % 11)
    if resto == 11:
        return "0"
    if resto == 10:
        return "K"
    return str(resto)


def validar_rut(rut):
    """Valida un RUT chileno (formato ``12345678-9`` o ``12.345.678-9``).

    Devuelve ``True`` si el dígito verificador es correcto.
    """
    rut_limpio = limpiar_rut(rut)
    if len(rut_limpio) < 2:
        return False
    cuerpo, dv = rut_limpio[:-1], rut_limpio[-1]
    if not cuerpo.isdigit():
        return False
    return calcular_dv(cuerpo) == dv


def formatear_rut(rut):
    """Formatea un RUT como ``12.345.678-9``."""
    rut_limpio = limpiar_rut(rut)
    if len(rut_limpio) < 2:
        return rut_limpio
    cuerpo, dv = rut_limpio[:-1], rut_limpio[-1]
    cuerpo_formateado = "{:,}".format(int(cuerpo)).replace(",", ".")
    return "{}-{}".format(cuerpo_formateado, dv)


def validar_fecha(fecha_texto, formato="%Y-%m-%d"):
    """Valida que ``fecha_texto`` corresponda a una fecha real según ``formato``."""
    if not fecha_texto:
        return False
    try:
        datetime.strptime(fecha_texto, formato)
        return True
    except ValueError:
        return False


def validar_monto_positivo(monto):
    """Valida que ``monto`` sea un número mayor o igual a cero."""
    try:
        return float(monto) >= 0
    except (TypeError, ValueError):
        return False


def validar_texto_no_vacio(texto):
    return bool(texto and str(texto).strip())
