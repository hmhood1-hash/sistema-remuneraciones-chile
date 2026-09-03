"""
Módulo de gestión de trabajadores
"""
from database.models import fetch_all, fetch_one, insert, update, delete
from ui.utils import titulo, pedir_texto, pedir_rut, pedir_fecha, pedir_monto, imprimir_tabla, pausar


def menu_gestion_trabajador():
    """
    Menú de gestión de trabajadores
    """
    opciones = {
        0: ("Volver", lambda: None),
        1: ("Crear Trabajador", crear_trabajador),
        2: ("Listar Trabajadores", listar_trabajadores),
        3: ("Modificar Trabajador", modificar_trabajador),
        4: ("Gestión de Cargas Familiares", menu_cargas_familiares),
    }
    from ui.menus import _menu
    _menu(opciones, "Gestión de Trabajadores")


def crear_trabajador():
    """
    Crea un nuevo trabajador
    """
    titulo("Crear Nuevo Trabajador")
    
    empresas = fetch_all('empresa')
    if not empresas:
        print("  ✗ No hay empresas registradas")
        pausar()
        return
    
    print("  Empresas disponibles:")
    for emp in empresas:
        print(f"    {emp['codigo']}: {emp['razon_social']}")
    
    rut = pedir_rut("RUT Trabajador")
    
    # Verificar si ya existe
    if fetch_one('trabajador', {'rut': rut}):
        print("  ✗ El trabajador ya existe")
        pausar()
        return
    
    data = {
        'rut': rut,
        'empresa_codigo': pedir_texto("Código Empresa"),
        'nombre': pedir_texto("Nombre"),
        'ap_paterno': pedir_texto("Apellido Paterno", obligatorio=False),
        'ap_materno': pedir_texto("Apellido Materno", obligatorio=False),
        'fecha_nacimiento': pedir_fecha("Fecha Nacimiento"),
        'sexo': pedir_texto("Sexo (M/F/O)"),
        'estado_civil': pedir_texto("Estado Civil (Soltero/Casado/Viudo/Separado)", obligatorio=False),
        'calle': pedir_texto("Calle", obligatorio=False),
        'numero': pedir_texto("Número", obligatorio=False),
        'depto': pedir_texto("Depto", obligatorio=False),
        'comuna': pedir_texto("Comuna", obligatorio=False),
        'correo': pedir_texto("Correo", obligatorio=False),
        'fono': pedir_texto("Fono", obligatorio=False),
    }
    
    try:
        insert('trabajador', data)
        
        # Crear datos laborales
        datos_laborales = {
            'trabajador_rut': rut,
            'sueldo_tipo': pedir_texto("Tipo Sueldo (Mensual/Diario/Part Time)"),
            'sueldo_base': pedir_monto("Sueldo Base"),
            'gratificacion_tipo': pedir_texto("Tipo Gratificación (Mensual/Anual)", obligatorio=False),
            'horas_semanales': int(pedir_texto("Horas Semanales")),
            'dias_laborales_semana': int(pedir_texto("Días Laborales a la Semana")),
            'fecha_contrato': pedir_fecha("Fecha Contrato"),
            'cargo': pedir_texto("Cargo", obligatorio=False),
            'aplica_sis': pedir_texto("¿Aplica SIS? (S/N)"),
        }
        insert('datos_laborales', datos_laborales)
        
        # Crear datos previsionales
        datos_previsionales = {
            'trabajador_rut': rut,
            'afp_codigo': pedir_texto("AFP (EMPART/SSS/CAPITAL/CUPRUM/HABITAT/MODELO/PLANVITAL/PROVIDA/UNO)"),
            'isapre_codigo': pedir_texto("Isapre (FONASA/VIDATRES/CONSALUD/BANMEDICA/MASVIDA/CRUZBLANCA)"),
            'modalidad_salud': pedir_texto("Modalidad Salud (7%/UF/Pesos)", obligatorio=False),
            'cotizacion_pactada': pedir_monto("Cotización Pactada (%)"),
            'tipo_trabajador': pedir_texto("Tipo Trabajador (Activo No Pensionado/Pensionado y cotiza/etc)"),
        }
        insert('datos_previsionales', datos_previsionales)
        
        print(f"  ✓ Trabajador {data['nombre']} creado")
        pausar()
    except Exception as e:
        print(f"  ✗ Error: {str(e)}")
        pausar()


def listar_trabajadores():
    """
    Lista todos los trabajadores
    """
    titulo("Listado de Trabajadores")
    
    trabajadores = fetch_all('trabajador')
    
    if trabajadores:
        columnas = ['rut', 'nombre', 'ap_paterno', 'cargo']
        imprimir_tabla(trabajadores, columnas)
    else:
        print("  * Sin trabajadores registrados")
    
    pausar()


def modificar_trabajador():
    """
    Modifica un trabajador existente
    """
    titulo("Modificar Trabajador")
    
    rut = pedir_rut("RUT del Trabajador a modificar")
    trabajador = fetch_one('trabajador', {'rut': rut})
    
    if not trabajador:
        print("  ✗ Trabajador no encontrado")
        pausar()
        return
    
    print(f"  Trabajador: {trabajador['nombre']}")
    
    data = {
        'nombre': pedir_texto("Nombre", default=trabajador.get('nombre', '')),
        'correo': pedir_texto("Correo", obligatorio=False, default=trabajador.get('correo', '')),
        'fono': pedir_texto("Fono", obligatorio=False, default=trabajador.get('fono', '')),
    }
    
    try:
        update('trabajador', data, {'rut': rut})
        print("  ✓ Trabajador actualizado")
        pausar()
    except Exception as e:
        print(f"  ✗ Error: {str(e)}")
        pausar()


def menu_cargas_familiares():
    """
    Menú de gestión de cargas familiares
    """
    opciones = {
        0: ("Volver", lambda: None),
        1: ("Agregar Carga Familiar", agregar_carga_familiar),
        2: ("Listar Cargas Familiares", listar_cargas_familiares),
        3: ("Eliminar Carga Familiar", eliminar_carga_familiar),
    }
    from ui.menus import _menu
    _menu(opciones, "Gestión de Cargas Familiares")


def agregar_carga_familiar():
    """
    Agrega una carga familiar a un trabajador
    """
    titulo("Agregar Carga Familiar")
    
    rut_trabajador = pedir_rut("RUT del Trabajador")
    
    if not fetch_one('trabajador', {'rut': rut_trabajador}):
        print("  ✗ Trabajador no encontrado")
        pausar()
        return
    
    data = {
        'trabajador_rut': rut_trabajador,
        'rut_carga': pedir_rut("RUT de la Carga"),
        'nombre': pedir_texto("Nombre"),
        'fecha_inicio': pedir_fecha("Fecha Inicio"),
        'fecha_vencimiento': pedir_fecha("Fecha Vencimiento", obligatorio=False),
        'tipo': pedir_texto("Tipo (Simple/Materna/Invalidez)"),
        'parentesco': pedir_texto("Parentesco (Hijo/Cónyuge/Progenitor/Hermano)"),
    }
    
    try:
        insert('carga_familiar', data)
        print("  ✓ Carga familiar agregada")
        pausar()
    except Exception as e:
        print(f"  ✗ Error: {str(e)}")
        pausar()


def listar_cargas_familiares():
    """
    Lista cargas familiares de un trabajador
    """
    titulo("Listado de Cargas Familiares")
    
    rut_trabajador = pedir_rut("RUT del Trabajador")
    cargas = fetch_all('carga_familiar', {'trabajador_rut': rut_trabajador})
    
    if cargas:
        columnas = ['nombre', 'tipo', 'parentesco', 'fecha_inicio']
        imprimir_tabla(cargas, columnas)
    else:
        print("  * Sin cargas familiares registradas")
    
    pausar()


def eliminar_carga_familiar():
    """
    Elimina una carga familiar
    """
    titulo("Eliminar Carga Familiar")
    
    id_carga = pedir_texto("ID de la Carga Familiar a eliminar")
    
    try:
        delete('carga_familiar', {'id': int(id_carga)})
        print("  ✓ Carga familiar eliminada")
        pausar()
    except Exception as e:
        print(f"  ✗ Error: {str(e)}")
        pausar()
