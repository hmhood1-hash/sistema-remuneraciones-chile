"""
Módulo de gestión de parámetros y factores
"""
from database.models import fetch_all, fetch_one, insert, update
from ui.utils import titulo, pedir_entero, pedir_monto, imprimir_tabla, pausar
from datetime import date


def menu_parametros():
    """
    Menú de parámetros y factores
    """
    opciones = {
        0: ("Volver", lambda: None),
        1: ("Ver/Actualizar Factores de Actualización", ver_factores),
        2: ("Ver/Actualizar Parámetros", ver_parametros),
        3: ("Ver/Actualizar Tabla Impuesto Único", ver_impuesto_unico),
        4: ("Ver/Actualizar Tramos de Cargas Familiares", ver_tramos_cargas),
    }
    from ui.menus import _menu
    _menu(opciones, "Parámetros y Factores")


def ver_factores():
    """
    Visualiza/actualiza factores de actualización mensuales
    """
    titulo("Factores de Actualización Mensuales")
    
    anio = pedir_entero("Año")
    mes = pedir_entero("Mes (1-12)")
    
    factor = fetch_one('parametro', {'anio': anio, 'mes': mes})
    
    if factor:
        print(f"\n  UTM: {factor['utm']}")
        print(f"  UF: {factor['uf']}")
        print(f"  Factor: {factor['factor_actualizacion']}")
    else:
        print("\n  * Sin factores para este período")
        print("\n  Crear nuevo registro:")
        
        data = {
            'anio': anio,
            'mes': mes,
            'utm': pedir_monto("UTM"),
            'uf': pedir_monto("UF"),
            'factor_actualizacion': pedir_monto("Factor"),
        }
        
        try:
            insert('parametro', data)
            print("  ✓ Factores registrados")
        except Exception as e:
            print(f"  ✗ Error: {str(e)}")
    
    pausar()


def guardar_factor_actualizacion(anio, mes, datos):
    """
    Guarda factores de actualización
    """
    datos['anio'] = anio
    datos['mes'] = mes
    
    # Verificar si ya existe
    existente = fetch_one('parametro', {'anio': anio, 'mes': mes})
    
    if existente:
        update('parametro', datos, {'anio': anio, 'mes': mes})
    else:
        insert('parametro', datos)


def ver_parametros():
    """
    Visualiza parámetros
    """
    titulo("Parámetros del Sistema")
    
    parametros = fetch_all('parametro')
    
    if parametros:
        columnas = ['anio', 'mes', 'utm', 'uf', 'sueldo_minimo']
        imprimir_tabla(parametros, columnas)
    else:
        print("  * Sin parámetros registrados")
    
    pausar()


def ver_impuesto_unico():
    """
    Visualiza tabla de impuesto único
    """
    titulo("Tabla de Impuesto Único")
    
    anio = pedir_entero("Año")
    
    tramos = fetch_all('impuesto_unico', {'anio': anio})
    
    if tramos:
        columnas = ['sueldo_desde', 'sueldo_hasta', 'factor', 'rebaja']
        imprimir_tabla(tramos, columnas)
    else:
        print("  * Sin tabla de impuesto único para este año")
    
    pausar()


def ver_tramos_cargas():
    """
    Visualiza tramos de cargas familiares
    """
    titulo("Tramos de Cargas Familiares")
    
    from database.models import fetch_all
    
    tramos = fetch_all('tramo_carga_familiar')
    
    if tramos:
        columnas = ['numero_tramo', 'sueldo_desde', 'sueldo_hasta', 'valor_carga']
        imprimir_tabla(tramos, columnas)
    else:
        print("  * Sin tramos de cargas familiares registrados")
    
    pausar()
