"""
Módulo de gestión de haberes y descuentos
"""
from database.models import fetch_all, fetch_one, insert, update, delete
from ui.utils import titulo, pedir_texto, pedir_monto, pedir_entero, imprimir_tabla, pausar


def menu_haberes():
    """
    Menú de gestión de haberes y descuentos
    """
    opciones = {
        0: ("Volver", lambda: None),
        1: ("Crear Haber", crear_haber),
        2: ("Listar Haberes", listar_haberes),
        3: ("Crear Descuento", crear_descuento),
        4: ("Listar Descuentos", listar_descuentos),
    }
    from ui.menus import _menu
    _menu(opciones, "Haberes y Descuentos")


def crear_haber():
    """
    Crea un nuevo haber
    """
    titulo("Crear Haber")
    
    from database.models import fetch_all
    empresas = fetch_all('empresa')
    
    if not empresas:
        print("  ✗ No hay empresas registradas")
        pausar()
        return
    
    print("  Empresas disponibles:")
    for emp in empresas:
        print(f"    {emp['codigo']}: {emp['razon_social']}")
    
    data = {
        'empresa_codigo': pedir_entero("Código de Empresa"),
        'nombre': pedir_texto("Nombre del Haber"),
        'clasificacion': pedir_texto("Clasificación (Imponible/Tributable/Adicional HE/etc)"),
        'tipo': pedir_texto("Tipo (Fijo/Variable/Valor diario/Semana corrida/Porcentaje)"),
        'monto_pesos': pedir_monto("Monto en Pesos", permitir_cero=True),
        'porcentaje': pedir_monto("Porcentaje", permitir_cero=True),
        'base_calculo': pedir_texto("Base Cálculo (Sueldo base/Imponible/etc)", obligatorio=False),
    }
    
    try:
        codigo = insert('haber', data)
        print(f"  ✓ Haber creado con código {codigo}")
        pausar()
    except Exception as e:
        print(f"  ✗ Error: {str(e)}")
        pausar()


def listar_haberes():
    """
    Lista todos los haberes
    """
    titulo("Listado de Haberes")
    
    haberes = fetch_all('haber')
    
    if haberes:
        columnas = ['codigo', 'nombre', 'clasificacion', 'tipo']
        imprimir_tabla(haberes, columnas)
    else:
        print("  * Sin haberes registrados")
    
    pausar()


def crear_descuento():
    """
    Crea un nuevo descuento
    """
    titulo("Crear Descuento")
    
    from database.models import fetch_all
    empresas = fetch_all('empresa')
    
    if not empresas:
        print("  ✗ No hay empresas registradas")
        pausar()
        return
    
    print("  Empresas disponibles:")
    for emp in empresas:
        print(f"    {emp['codigo']}: {emp['razon_social']}")
    
    data = {
        'empresa_codigo': pedir_entero("Código de Empresa"),
        'nombre': pedir_texto("Nombre del Descuento"),
        'tipo': pedir_texto("Tipo (Fijo/Variable/Porcentaje)"),
        'monto_pesos': pedir_monto("Monto en Pesos", permitir_cero=True),
        'porcentaje': pedir_monto("Porcentaje", permitir_cero=True),
        'base_calculo': pedir_texto("Base Cálculo (Sueldo base/Imponible/etc)", obligatorio=False),
    }
    
    try:
        codigo = insert('descuento', data)
        print(f"  ✓ Descuento creado con código {codigo}")
        pausar()
    except Exception as e:
        print(f"  ✗ Error: {str(e)}")
        pausar()


def listar_descuentos():
    """
    Lista todos los descuentos
    """
    titulo("Listado de Descuentos")
    
    descuentos = fetch_all('descuento')
    
    if descuentos:
        columnas = ['codigo', 'nombre', 'tipo']
        imprimir_tabla(descuentos, columnas)
    else:
        print("  * Sin descuentos registrados")
    
    pausar()
