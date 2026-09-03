"""
Funciones de utilidad para la interfaz de consola: entrada de datos, validaciones
(RUT, fechas, montos) e impresión de tablas y menús.
"""
from datetime import datetime


def limpiar_pantalla():
    print("\n" * 2)


def titulo(texto):
    print("=" * 60)
    print(texto.center(60))
    print("=" * 60)


def validar_rut(rut):
    """Valida un RUT chileno (formato NNNNNNNN-DV) usando el algoritmo del dígito verificador."""
    if not rut:
        return False
    rut = rut.strip().upper().replace(".", "")
    if "-" not in rut:
        return False
    cuerpo, dv = rut.rsplit("-", 1)
    cuerpo = cuerpo.strip()
    dv = dv.strip()
    if not cuerpo.isdigit():
        return False
    suma = 0
    multiplo = 2
    for c in reversed(cuerpo):
        suma += int(c) * multiplo
        multiplo = multiplo + 1 if multiplo < 7 else 2
    resto = 11 - (suma % 11)
    if resto == 11:
        dv_calculado = "0"
    elif resto == 10:
        dv_calculado = "K"
    else:
        dv_calculado = str(resto)
    return dv == dv_calculado


def formatear_rut(rut):
    return rut.strip().upper().replace(".", "")


def validar_fecha(fecha_str, formato="%d-%m-%Y"):
    try:
        datetime.strptime(fecha_str, formato)
        return True
    except (ValueError, TypeError):
        return False


def validar_monto(valor):
    try:
        return float(valor) >= 0
    except (TypeError, ValueError):
        return False


def pedir_texto(mensaje, obligatorio=True, default=None):
    while True:
        valor = input(f"{mensaje}: ").strip()
        if not valor and default is not None:
            return default
        if not valor and not obligatorio:
            return ""
        if valor:
            return valor
        print("  * Este dato es obligatorio.")


def pedir_rut(mensaje="RUT", obligatorio=True):
    while True:
        rut = input(f"{mensaje} (formato 12345678-9): ").strip()
        if not rut and not obligatorio:
            return ""
        rut = formatear_rut(rut)
        if validar_rut(rut):
            return rut
        print("  * RUT inválido, intente nuevamente.")


def pedir_fecha(mensaje, formato="%d-%m-%Y", obligatorio=True):
    while True:
        fecha = input(f"{mensaje} ({formato}): ").strip()
        if not fecha and not obligatorio:
            return None
        if validar_fecha(fecha, formato):
            return fecha
        print(f"  * Fecha inválida, use el formato {formato}.")


def pedir_monto(mensaje, default=None):
    while True:
        valor = input(f"{mensaje}: ").strip()
        if not valor and default is not None:
            return default
        if validar_monto(valor):
            return float(valor)
        print("  * Monto inválido, ingrese un número mayor o igual a 0.")


_SIN_DEFAULT = object()


def pedir_entero(mensaje, default=_SIN_DEFAULT):
    while True:
        valor = input(f"{mensaje}: ").strip()
        if not valor and default is not _SIN_DEFAULT:
            return default
        try:
            return int(valor)
        except ValueError:
            print("  * Debe ingresar un número entero.")


def pedir_opcion(mensaje, opciones):
    """opciones: lista de valores válidos (strings)"""
    opciones_norm = [str(o) for o in opciones]
    while True:
        valor = input(f"{mensaje} [{'/'.join(opciones_norm)}]: ").strip()
        if valor in opciones_norm:
            return valor
        print("  * Opción inválida.")


def formatear_pesos(monto):
    return f"${monto:,.0f}".replace(",", ".")


def imprimir_tabla(filas, columnas=None):
    """Imprime una lista de dicts como tabla simple en consola."""
    if not filas:
        print("(sin registros)")
        return
    if columnas is None:
        columnas = list(filas[0].keys())
    anchos = {c: max(len(c), max(len(str(f.get(c, ""))) for f in filas)) for c in columnas}
    encabezado = " | ".join(c.ljust(anchos[c]) for c in columnas)
    print(encabezado)
    print("-" * len(encabezado))
    for f in filas:
        print(" | ".join(str(f.get(c, "")).ljust(anchos[c]) for c in columnas))


def pausar():
    input("\nPresione ENTER para continuar...")
