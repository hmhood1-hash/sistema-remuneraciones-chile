"""
Validaciones de datos
"""
import re
from datetime import datetime


def validar_rut(rut):
    """
    Valida un RUT chileno con dígito verificador.
    Formato: XX.XXX.XXX-K o XXXXXXXX-K
    
    Args:
        rut: String con el RUT a validar
    
    Returns:
        True si es válido, False en caso contrario
    """
    rut = rut.strip().upper()
    rut = re.sub(r'[.]', '', rut)  # Quitar puntos
    
    if not re.match(r'^\d{7,8}-[\dK]$', rut):
        return False
    
    numero, digito = rut.split('-')
    numero = int(numero)
    
    # Calcular dígito verificador
    multiplos = [2, 3, 4, 5, 6, 7]
    suma = 0
    i = 0
    
    for d in reversed(str(numero)):
        suma += int(d) * multiplos[i % 6]
        i += 1
    
    digito_calculado = 11 - (suma % 11)
    
    if digito_calculado == 11:
        digito_calculado = 0
    elif digito_calculado == 10:
        digito_calculado = 'K'
    else:
        digito_calculado = str(digito_calculado)
    
    return str(digito_calculado) == digito


def validar_fecha(fecha_str):
    """
    Valida una fecha en formato DD-MM-YYYY.
    
    Args:
        fecha_str: String con la fecha
    
    Returns:
        True si es válida, False en caso contrario
    """
    try:
        datetime.strptime(fecha_str, "%d-%m-%Y")
        return True
    except ValueError:
        return False


def validar_monto(monto):
    """
    Valida que un monto sea un número positivo.
    
    Args:
        monto: String o número
    
    Returns:
        True si es válido, False en caso contrario
    """
    try:
        valor = float(monto)
        return valor >= 0
    except (ValueError, TypeError):
        return False
