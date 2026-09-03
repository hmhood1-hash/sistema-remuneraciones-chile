"""
Utilidades de interfaz de usuario y validaciones
"""
import re
from datetime import datetime
from calculos.validaciones import validar_rut as validar_rut_func
from calculos.validaciones import validar_fecha as validar_fecha_func
from calculos.validaciones import validar_monto as validar_monto_func


def titulo(texto):
    """Imprime un título con formato."""
    print("\n" + "="*60)
    print(f"  {texto.center(56)}")
    print("="*60)


def separador():
    """Imprime un separador."""
    print("-" * 60)


def pausar():
    """Pausa la ejecución hasta que el usuario presione Enter."""
    input("\nPresione ENTER para continuar...")


def limpiar_pantalla():
    """Limpia la pantalla (Windows compatible)."""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


def pedir_texto(mensaje, obligatorio=True, default=""):
    """
    Pide un texto al usuario.
    
    Args:
        mensaje: Mensaje a mostrar
        obligatorio: Si es obligatorio (True/False)
        default: Valor por defecto
    
    Returns:
        String con el texto ingresado
    """
    while True:
        valor = input(f"{mensaje}: ").strip()
        
        if not valor and default:
            return default
        
        if not valor and obligatorio:
            print("  * Este campo es obligatorio")
            continue
        
        return valor


def pedir_rut(mensaje="RUT"):
    """
    Pide un RUT chileno validado.
    
    Args:
        mensaje: Mensaje personalizado
    
    Returns:
        String con el RUT válido
    """
    while True:
        rut = input(f"{mensaje} (formato 12345678-9): ").strip().upper()
        
        if validar_rut_func(rut):
            # Normalizar formato
            rut = re.sub(r'[.]', '', rut)
            return rut
        
        print("  * RUT inválido, intente nuevamente.")


def pedir_fecha(mensaje="Fecha"):
    """
    Pide una fecha en formato DD-MM-YYYY.
    
    Args:
        mensaje: Mensaje personalizado
    
    Returns:
        String con la fecha válida
    """
    while True:
        fecha = input(f"{mensaje} (formato DD-MM-YYYY): ").strip()
        
        if validar_fecha_func(fecha):
            return fecha
        
        print("  * Fecha inválida, intente nuevamente.")


def pedir_monto(mensaje="Monto", permitir_cero=False):
    """
    Pide un monto numérico.
    
    Args:
        mensaje: Mensaje personalizado
        permitir_cero: Si permite monto 0
    
    Returns:
        Float con el monto
    """
    while True:
        try:
            monto = input(f"{mensaje}: ").strip()
            
            if not monto:
                if permitir_cero:
                    return 0.0
                print("  * Debe ingresar un monto")
                continue
            
            valor = float(monto.replace(",", "."))
            
            if valor < 0:
                print("  * El monto no puede ser negativo")
                continue
            
            if valor == 0 and not permitir_cero:
                print("  * El monto debe ser mayor a 0")
                continue
            
            return valor
        except ValueError:
            print("  * Ingrese un número válido")


def pedir_entero(mensaje="Número", minimo=None, maximo=None):
    """
    Pide un número entero.
    
    Args:
        mensaje: Mensaje personalizado
        minimo: Valor mínimo permitido
        maximo: Valor máximo permitido
    
    Returns:
        Integer validado
    """
    while True:
        try:
            valor = int(input(f"{mensaje}: ").strip())
            
            if minimo is not None and valor < minimo:
                print(f"  * El valor debe ser mayor o igual a {minimo}")
                continue
            
            if maximo is not None and valor > maximo:
                print(f"  * El valor debe ser menor o igual a {maximo}")
                continue
            
            return valor
        except ValueError:
            print("  * Ingrese un número válido")


def pedir_opcion(mensaje="Seleccione", opciones=None):
    """
    Pide que se seleccione una opción de una lista.
    
    Args:
        mensaje: Mensaje personalizado
        opciones: Lista de opciones válidas
    
    Returns:
        Opción seleccionada
    """
    while True:
        valor = input(f"{mensaje}: ").strip().upper()
        
        if opciones and valor not in opciones:
            print(f"  * Seleccione una opción válida: {', '.join(opciones)}")
            continue
        
        return valor


def imprimir_tabla(datos, columnas=None, titulo_tabla=""):
    """
    Imprime datos en formato de tabla.
    
    Args:
        datos: Lista de diccionarios o tuplas
        columnas: Lista de nombres de columnas (si es None, usa todas)
        titulo_tabla: Título de la tabla
    """
    if not datos:
        print("  * Sin registros")
        return
    
    # Si son diccionarios
    if isinstance(datos[0], dict):
        if columnas is None:
            columnas = list(datos[0].keys())
        
        # Calcular ancho de columnas
        anchos = {col: max(len(str(col)), max(len(str(fila.get(col, ""))) for fila in datos)) for col in columnas}
    else:
        # Si son tuplas
        if columnas is None:
            columnas = [f"Col{i+1}" for i in range(len(datos[0]))]
        
        anchos = {col: max(len(str(col)), max(len(str(fila[i] if i < len(fila) else "")) for fila in datos)) for i, col in enumerate(columnas)}
    
    # Encabezado
    if titulo_tabla:
        print(f"\n{titulo_tabla}")
    
    encabezado = " | ".join(str(col).ljust(anchos.get(col, 10)) for col in columnas)
    print(encabezado)
    print("-" * len(encabezado))
    
    # Filas
    for fila in datos:
        if isinstance(fila, dict):
            fila_str = " | ".join(str(fila.get(col, "")).ljust(anchos.get(col, 10)) for col in columnas)
        else:
            fila_str = " | ".join(str(fila[i] if i < len(fila) else "").ljust(anchos.get(columnas[i], 10)) for i, col in enumerate(columnas))
        print(fila_str)


def formatear_rut(rut):
    """
    Formatea un RUT a XX.XXX.XXX-K.
    
    Args:
        rut: RUT sin formato
    
    Returns:
        RUT formateado
    """
    rut = rut.replace(".", "").replace("-", "").upper()
    if len(rut) < 8:
        return rut
    
    numero = rut[:-1]
    digito = rut[-1]
    
    # Agregar puntos
    numero_formateado = f"{numero[:-6]}.{numero[-6:-3]}.{numero[-3:]}"
    return f"{numero_formateado}-{digito}"


def validar_rut(rut):
    """
    Valida un RUT.
    
    Args:
        rut: RUT a validar
    
    Returns:
        True si es válido
    """
    return validar_rut_func(rut)


def formatear_moneda(monto):
    """
    Formatea un monto como moneda chilena.
    
    Args:
        monto: Monto a formatear
    
    Returns:
        String formateado
    """
    return f"${monto:,.0f}".replace(",", ".")
