"""
Módulo de gestión de contratos y finiquitos
"""
from database.models import fetch_all, insert, delete
from ui.utils import titulo, pedir_texto, pedir_rut, pedir_fecha, pedir_monto, imprimir_tabla, pausar


def menu_contratos():
    """
    Menú de gestión de contratos y finiquitos
    """
    opciones = {
        0: ("Volver", lambda: None),
        1: ("Crear Contrato", crear_contrato),
        2: ("Listar Contratos", listar_contratos),
        3: ("Crear Finiquito", crear_finiquito),
        4: ("Listar Finiquitos", listar_finiquitos),
    }
    from ui.menus import _menu
    _menu(opciones, "Contratos y Finiquitos")


def crear_contrato():
    """
    Crea un nuevo contrato
    """
    titulo("Crear Contrato")
    
    rut_trabajador = pedir_rut("RUT del Trabajador")
    
    from database.models import fetch_one
    if not fetch_one('trabajador', {'rut': rut_trabajador}):
        print("  ✗ Trabajador no encontrado")
        pausar()
        return
    
    data = {
        'trabajador_rut': rut_trabajador,
        'nacionalidad': pedir_texto("Nacionalidad", obligatorio=False),
        'labor_ejecutar': pedir_texto("Labor a Ejecutar", obligatorio=False),
        'establecimiento': pedir_texto("Establecimiento", obligatorio=False),
        'horarios': pedir_texto("Horarios", obligatorio=False),
        'duracion_contrato': pedir_texto("Duración (fecha inicio - fecha termino)", obligatorio=False),
        'tipo_contrato_codigo': pedir_texto("Tipo Contrato (INDEFINIDO/PLAZO_FIJO/APRENDIZ/PRACTICA)"),
        'frecuencia_pago': pedir_texto("Frecuencia de Pago (Mensual/Quincenal/Diario)", obligatorio=False),
        'sueldo_base': pedir_monto("Sueldo Base"),
        'movilizacion': pedir_monto("Movilización", permitir_cero=True),
        'colacion': pedir_monto("Colación", permitir_cero=True),
        'gratificacion': pedir_monto("Gratificación", permitir_cero=True),
        'remuneracion_adicional': pedir_monto("Remuneración Adicional", permitir_cero=True),
        'fecha_inicio': pedir_fecha("Fecha Inicio"),
        'fecha_termino': pedir_fecha("Fecha Término", obligatorio=False),
    }
    
    try:
        codigo = insert('contrato', data)
        print(f"  ✓ Contrato creado con ID {codigo}")
        pausar()
    except Exception as e:
        print(f"  ✗ Error: {str(e)}")
        pausar()


def listar_contratos():
    """
    Lista todos los contratos
    """
    titulo("Listado de Contratos")
    
    contratos = fetch_all('contrato')
    
    if contratos:
        columnas = ['id', 'trabajador_rut', 'tipo_contrato_codigo', 'sueldo_base']
        imprimir_tabla(contratos, columnas)
    else:
        print("  * Sin contratos registrados")
    
    pausar()


def crear_finiquito():
    """
    Crea un finiquito
    """
    titulo("Crear Finiquito")
    
    rut_trabajador = pedir_rut("RUT del Trabajador")
    
    from database.models import fetch_one
    if not fetch_one('trabajador', {'rut': rut_trabajador}):
        print("  ✗ Trabajador no encontrado")
        pausar()
        return
    
    data = {
        'trabajador_rut': rut_trabajador,
        'fecha_inicio': pedir_fecha("Fecha Inicio del Contrato"),
        'fecha_termino': pedir_fecha("Fecha Término"),
        'cargo': pedir_texto("Cargo", obligatorio=False),
        'causal_finiquito_codigo': pedir_texto("Causal (RENUNCIA/DESPIDO/VENCIMIENTO/etc)"),
        'sueldo_proporcional': pedir_monto("Sueldo Proporcional"),
        'gratificacion_proporcional': pedir_monto("Gratificación Proporcional", permitir_cero=True),
        'vacaciones_proporcional': pedir_monto("Vacaciones Proporcional", permitir_cero=True),
        'indemnizacion': pedir_monto("Indemnización", permitir_cero=True),
        'otras_prestaciones': pedir_monto("Otras Prestaciones", permitir_cero=True),
    }
    
    # Calcular totales
    data['total_haber'] = data['sueldo_proporcional'] + data['gratificacion_proporcional'] + data['vacaciones_proporcional'] + data['indemnizacion'] + data['otras_prestaciones']
    data['descuentos'] = pedir_monto("Descuentos", permitir_cero=True)
    data['liquido_finiquito'] = data['total_haber'] - data['descuentos']
    
    from datetime import datetime
    data['fecha_calculo'] = datetime.now().isoformat()
    
    try:
        codigo = insert('finiquito', data)
        print(f"  ✓ Finiquito creado con ID {codigo}")
        print(f"  Líquido a pagar: ${data['liquido_finiquito']:,.0f}")
        pausar()
    except Exception as e:
        print(f"  ✗ Error: {str(e)}")
        pausar()


def listar_finiquitos():
    """
    Lista todos los finiquitos
    """
    titulo("Listado de Finiquitos")
    
    finiquitos = fetch_all('finiquito')
    
    if finiquitos:
        columnas = ['id', 'trabajador_rut', 'fecha_termino', 'liquido_finiquito']
        imprimir_tabla(finiquitos, columnas)
    else:
        print("  * Sin finiquitos registrados")
    
    pausar()
