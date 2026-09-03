"""
Módulo de control de vacaciones
"""
from database.models import fetch_all, fetch_one, insert, update
from ui.utils import titulo, pedir_rut, pedir_entero, pedir_fecha, imprimir_tabla, pausar


def menu_vacaciones():
    """
    Menú de control de vacaciones
    """
    opciones = {
        0: ("Volver", lambda: None),
        1: ("Registrar Vacaciones", registrar_vacaciones),
        2: ("Listar Vacaciones", listar_vacaciones),
        3: ("Ver Disponibilidad", ver_disponibilidad),
    }
    from ui.menus import _menu
    _menu(opciones, "Control de Vacaciones")


def registrar_vacaciones():
    """
    Registra vacaciones de un trabajador
    """
    titulo("Registrar Vacaciones")
    
    rut_trabajador = pedir_rut("RUT del Trabajador")
    
    if not fetch_one('trabajador', {'rut': rut_trabajador}):
        print("  ✗ Trabajador no encontrado")
        pausar()
        return
    
    anio = pedir_entero("Año Laboral")
    
    vacacion_existente = fetch_one('vacacion', {'trabajador_rut': rut_trabajador, 'anio_laboral': anio})
    
    dias_acumulados = pedir_entero("Días Acumulados")
    dias_tomados = pedir_entero("Días Tomados")
    dias_disponibles = dias_acumulados - dias_tomados
    
    data = {
        'trabajador_rut': rut_trabajador,
        'anio_laboral': anio,
        'dias_acumulados': dias_acumulados,
        'dias_tomados': dias_tomados,
        'dias_disponibles': dias_disponibles,
        'fecha_inicio_vacacion': pedir_fecha("Fecha Inicio Vacación", obligatorio=False),
        'fecha_termino_vacacion': pedir_fecha("Fecha Término Vacación", obligatorio=False),
    }
    
    try:
        if vacacion_existente:
            update('vacacion', data, {'trabajador_rut': rut_trabajador, 'anio_laboral': anio})
            print("  ✓ Vacaciones actualizada")
        else:
            insert('vacacion', data)
            print("  ✓ Vacaciones registrada")
        pausar()
    except Exception as e:
        print(f"  ✗ Error: {str(e)}")
        pausar()


def listar_vacaciones():
    """
    Lista vacaciones de todos los trabajadores
    """
    titulo("Listado de Vacaciones")
    
    vacaciones = fetch_all('vacacion')
    
    if vacaciones:
        columnas = ['trabajador_rut', 'anio_laboral', 'dias_acumulados', 'dias_tomados', 'dias_disponibles']
        imprimir_tabla(vacaciones, columnas)
    else:
        print("  * Sin registros de vacaciones")
    
    pausar()


def ver_disponibilidad():
    """
    Ver disponibilidad de vacaciones de un trabajador
    """
    titulo("Ver Disponibilidad de Vacaciones")
    
    rut_trabajador = pedir_rut("RUT del Trabajador")
    anio = pedir_entero("Año")
    
    vacacion = fetch_one('vacacion', {'trabajador_rut': rut_trabajador, 'anio_laboral': anio})
    
    if vacacion:
        print(f"\n  Trabajador: {rut_trabajador}")
        print(f"  Año: {vacacion['anio_laboral']}")
        print(f"  Días Acumulados: {vacacion['dias_acumulados']}")
        print(f"  Días Tomados: {vacacion['dias_tomados']}")
        print(f"  Días Disponibles: {vacacion['dias_disponibles']}")
    else:
        print("  * Sin registros de vacaciones para este trabajador y año")
    
    pausar()
