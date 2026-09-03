"""
Módulo de gestión de instituciones previsionales
"""
from ui.utils import titulo, pedir_texto, pausar


def menu_instituciones_previsionales():
    """
    Menú de instituciones previsionales
    """
    opciones = {
        0: ("Volver", lambda: None),
        1: ("AFP", ver_afp),
        2: ("Isapres", ver_isapres),
        3: ("CCAF", ver_ccaf),
        4: ("Mutuales", ver_mutuales),
        5: ("Ahorro Previsional (APV)", ver_apv),
    }
    from ui.menus import _menu
    _menu(opciones, "Instituciones Previsionales")


def ver_afp():
    """
    Visualiza lista de AFP
    """
    titulo("Listado de AFP")
    from database.models import fetch_all
    from ui.utils import imprimir_tabla
    
    afps = fetch_all('afp')
    if afps:
        columnas = ['codigo', 'nombre', 'factor_cotizacion']
        imprimir_tabla(afps, columnas)
    else:
        print("  * Sin AFP registradas")
    
    pausar()


def ver_isapres():
    """
    Visualiza lista de Isapres
    """
    titulo("Listado de Isapres")
    from database.models import fetch_all
    from ui.utils import imprimir_tabla
    
    isapres = fetch_all('isapre')
    if isapres:
        columnas = ['codigo', 'nombre']
        imprimir_tabla(isapres, columnas)
    else:
        print("  * Sin Isapres registradas")
    
    pausar()


def ver_ccaf():
    """
    Visualiza lista de CCAF
    """
    titulo("Listado de CCAF")
    from database.models import fetch_all
    from ui.utils import imprimir_tabla
    
    ccafs = fetch_all('ccaf')
    if ccafs:
        columnas = ['codigo', 'nombre']
        imprimir_tabla(ccafs, columnas)
    else:
        print("  * Sin CCAF registradas")
    
    pausar()


def ver_mutuales():
    """
    Visualiza lista de Mutuales
    """
    titulo("Listado de Mutuales")
    from database.models import fetch_all
    from ui.utils import imprimir_tabla
    
    mutuales = fetch_all('mutual')
    if mutuales:
        columnas = ['codigo', 'nombre']
        imprimir_tabla(mutuales, columnas)
    else:
        print("  * Sin Mutuales registradas")
    
    pausar()


def ver_apv():
    """
    Visualiza lista de APV
    """
    titulo("Listado de Ahorro Previsional (APV)")
    from database.models import fetch_all
    from ui.utils import imprimir_tabla
    
    apvs = fetch_all('ahorro_previsional')
    if apvs:
        columnas = ['codigo', 'nombre']
        imprimir_tabla(apvs, columnas)
    else:
        print("  * Sin APV registradas")
    
    pausar()
