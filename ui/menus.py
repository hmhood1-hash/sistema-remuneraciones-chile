"""
Menús desplegables del sistema
"""
from ui.utils import titulo, separador, pausar


def _menu(opciones, nombre_menu=""):
    """
    Menú genérico que despliega opciones.
    
    Args:
        opciones: Diccionario {número: (descripción, función)}
        nombre_menu: Nombre del menú
    """
    while True:
        if nombre_menu:
            titulo(nombre_menu)
        
        for num in sorted(opciones.keys()):
            descripcion, _ = opciones[num]
            print(f"  {num}. {descripcion}")
        
        try:
            seleccion = input("\nSeleccione una opción: ").strip()
            
            if not seleccion.isdigit():
                print("  * Ingrese un número válido")
                continue
            
            seleccion = int(seleccion)
            
            if seleccion not in opciones:
                print("  * Opción no válida")
                continue
            
            descripcion, funcion = opciones[seleccion]
            
            if seleccion == 0:  # Salir
                return
            
            funcion()
        except KeyboardInterrupt:
            print("\n  * Operación cancelada")
            return
        except Exception as e:
            print(f"  * Error: {str(e)}")


def menu_principal():
    """
    Menú principal del sistema.
    """
    from modules.empresa import menu_gestion_empresa
    from modules.trabajador import menu_gestion_trabajador
    from modules.previsional import menu_instituciones_previsionales
    from modules.parametros import menu_parametros
    from modules.haberes import menu_haberes
    from modules.contrato import menu_contratos
    from modules.vacaciones import menu_vacaciones
    from modules.liquidacion import menu_liquidacion
    from modules.reportes import menu_reportes
    from modules.procesos import menu_procesos
    
    opciones = {
        0: ("Salir", lambda: None),
        1: ("Gestión de Empresa / Sucursales / Centros de Costo", menu_gestion_empresa),
        2: ("Gestión de Trabajadores", menu_gestion_trabajador),
        3: ("Instituciones Previsionales", menu_instituciones_previsionales),
        4: ("Parámetros y Factores", menu_parametros),
        5: ("Haberes y Descuentos", menu_haberes),
        6: ("Contratos y Finiquitos", menu_contratos),
        7: ("Control de Vacaciones", menu_vacaciones),
        8: ("Liquidaciones de Sueldo", menu_liquidacion),
        9: ("Informes y Reportes", menu_reportes),
        10: ("Procesos", menu_procesos),
    }
    
    _menu(opciones, "SISTEMA DE REMUNERACIONES - CHILE")
