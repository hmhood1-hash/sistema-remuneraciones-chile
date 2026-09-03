"""
Módulo de cálculo y gestión de liquidaciones de sueldo
"""
from database.models import fetch_all, fetch_one, insert, update
from ui.utils import titulo, pedir_rut, pedir_entero, pedir_monto, imprimir_tabla, pausar, formatear_moneda
from datetime import datetime, date
from calculos.impuesto_unico import calcular_impuesto_unico
from calculos.previsiones import calcular_afp, calcular_salud, calcular_afc, calcular_seguro_cesantia
from calculos.aportes import calcular_aporte_patronal, calcular_aporte_afc_empleador, calcular_aporte_sis, calcular_aporte_ccaf


def menu_liquidacion():
    """
    Menú de liquidaciones de sueldo
    """
    opciones = {
        0: ("Volver", lambda: None),
        1: ("Calcular Liquidación Individual", calcular_liquidacion_individual),
        2: ("Listar Liquidaciones", listar_liquidaciones),
        3: ("Ver Detalle de Liquidación", ver_detalle_liquidacion),
    }
    from ui.menus import _menu
    _menu(opciones, "Liquidaciones de Sueldo")


def calcular_liquidacion_individual():
    """
    Calcula liquidación individual de un trabajador
    """
    titulo("Calcular Liquidación Individual")
    
    rut_trabajador = pedir_rut("RUT del Trabajador")
    anio = pedir_entero("Año")
    mes = pedir_entero("Mes (1-12)")
    
    trabajador = fetch_one('trabajador', {'rut': rut_trabajador})
    if not trabajador:
        print("  ✗ Trabajador no encontrado")
        pausar()
        return
    
    liq = calcular_liquidacion(rut_trabajador, trabajador['empresa_codigo'], anio, mes)
    
    # Mostrar resumen
    print(f"\n  Liquidación de {trabajador['nombre']} - {mes}/{anio}")
    print(f"  Sueldo Base: {formatear_moneda(liq['sueldo_base'])}")
    print(f"  Total Haberes: {formatear_moneda(liq['total_haberes'])}")
    print(f"  AFP: {formatear_moneda(liq['monto_afp'])}")
    print(f"  Salud: {formatear_moneda(liq['monto_salud'])}")
    print(f"  Impuesto Único: {formatear_moneda(liq['impuesto_unico'])}")
    print(f"  Total Descuentos: {formatear_moneda(liq['total_descuentos'])}")
    print(f"  Sueldo Líquido: {formatear_moneda(liq['sueldo_liquido'])}")
    
    # Guardar
    try:
        guardar_liquidacion(liq)
        print("\n  ✓ Liquidación guardada")
    except Exception as e:
        print(f"  ✗ Error al guardar: {str(e)}")
    
    pausar()


def calcular_liquidacion(rut_trabajador, empresa_codigo, anio, mes):
    """
    Calcula una liquidación de sueldo completa
    """
    # Obtener datos del trabajador
    trabajador = fetch_one('trabajador', {'rut': rut_trabajador})
    datos_laborales = fetch_one('datos_laborales', {'trabajador_rut': rut_trabajador})
    datos_previsionales = fetch_one('datos_previsionales', {'trabajador_rut': rut_trabajador})
    
    if not datos_laborales or not datos_previsionales:
        raise Exception("Datos laborales o previsionales incompletos")
    
    # Sueldo base
    sueldo_base = float(datos_laborales['sueldo_base'])
    
    # Gratificación
    gratificacion = 0
    if datos_laborales['gratificacion_tipo'] == 'Mensual':
        gratificacion = float(datos_laborales.get('gratificacion_monto', 0) or 0)
    
    # Total haberes
    total_haberes_imponibles = sueldo_base + gratificacion
    total_haberes = total_haberes_imponibles
    
    # Cálculos de descuentos previsionales
    monto_afp = calcular_afp(total_haberes_imponibles, datos_previsionales['afp_codigo'], anio, mes)
    monto_salud = calcular_salud(total_haberes_imponibles, datos_previsionales['isapre_codigo'], datos_previsionales['modalidad_salud'], anio, mes)
    monto_afc = calcular_afc(sueldo_base, datos_previsionales['tipo_trabajador'], anio, mes)
    monto_apv = 0  # Opcional
    
    # Base tributable (para cálculo de impuesto)
    base_tributable = total_haberes_imponibles - monto_afp - monto_salud - monto_afc
    
    # Impuesto Único
    cargas = len(fetch_all('carga_familiar', {'trabajador_rut': rut_trabajador}))
    impuesto_unico = calcular_impuesto_unico(base_tributable, anio, cargas)
    
    # Total descuentos
    total_descuentos = monto_afp + monto_salud + monto_afc + monto_apv + impuesto_unico
    
    # Sueldo líquido
    sueldo_liquido = total_haberes - total_descuentos
    
    # Aportes patronales (no se descuentan del trabajador)
    aporte_patronal_sis = calcular_aporte_sis(sueldo_base, datos_laborales['aplica_sis'], anio, mes) if datos_laborales['aplica_sis'] == 'S' else 0
    aporte_patronal_afc = calcular_aporte_afc_empleador(sueldo_base, 'Indefinido', anio, mes)
    aporte_patronal_ccaf = calcular_aporte_ccaf(sueldo_base, anio, mes)
    aporte_patronal_mutual = 0  # Opcional
    
    # Compilar resultado
    liquidacion = {
        'trabajador_rut': rut_trabajador,
        'empresa_codigo': empresa_codigo,
        'anio': anio,
        'mes': mes,
        'sueldo_base': sueldo_base,
        'gratificacion': gratificacion,
        'total_haberes_imponibles': total_haberes_imponibles,
        'total_haberes_no_imponibles': 0,
        'total_haberes': total_haberes,
        'monto_afp': monto_afp,
        'monto_salud': monto_salud,
        'monto_afc': monto_afc,
        'monto_apv': monto_apv,
        'base_tributable': base_tributable,
        'impuesto_unico': impuesto_unico,
        'otros_descuentos': 0,
        'total_descuentos': total_descuentos,
        'sueldo_liquido': sueldo_liquido,
        'aporte_patronal_sis': aporte_patronal_sis,
        'aporte_patronal_afc': aporte_patronal_afc,
        'aporte_patronal_ccaf': aporte_patronal_ccaf,
        'aporte_patronal_mutual': aporte_patronal_mutual,
        'fecha_calculo': datetime.now().isoformat(),
    }
    
    return liquidacion


def guardar_liquidacion(liquidacion):
    """
    Guarda una liquidación en la BD
    """
    # Verificar si ya existe
    existente = fetch_one('liquidacion', {
        'trabajador_rut': liquidacion['trabajador_rut'],
        'anio': liquidacion['anio'],
        'mes': liquidacion['mes']
    })
    
    if existente:
        update('liquidacion', liquidacion, {
            'trabajador_rut': liquidacion['trabajador_rut'],
            'anio': liquidacion['anio'],
            'mes': liquidacion['mes']
        })
    else:
        insert('liquidacion', liquidacion)


def listar_liquidaciones():
    """
    Lista todas las liquidaciones
    """
    titulo("Listado de Liquidaciones")
    
    liquidaciones = fetch_all('liquidacion')
    
    if liquidaciones:
        columnas = ['trabajador_rut', 'anio', 'mes', 'sueldo_base', 'sueldo_liquido']
        imprimir_tabla(liquidaciones, columnas)
    else:
        print("  * Sin liquidaciones registradas")
    
    pausar()


def ver_detalle_liquidacion():
    """
    Ver detalle de una liquidación
    """
    titulo("Detalle de Liquidación")
    
    rut = pedir_rut("RUT del Trabajador")
    anio = pedir_entero("Año")
    mes = pedir_entero("Mes")
    
    liq = fetch_one('liquidacion', {'trabajador_rut': rut, 'anio': anio, 'mes': mes})
    
    if not liq:
        print("  * Liquidación no encontrada")
    else:
        print(f"\n  Liquidación {mes}/{anio}")
        print(f"  Sueldo Base: {formatear_moneda(liq['sueldo_base'])}")
        print(f"  Gratificación: {formatear_moneda(liq['gratificacion'])}")
        print(f"  Total Haberes: {formatear_moneda(liq['total_haberes'])}")
        print(f"  --- Descuentos ---")
        print(f"  AFP: {formatear_moneda(liq['monto_afp'])}")
        print(f"  Salud: {formatear_moneda(liq['monto_salud'])}")
        print(f"  AFC: {formatear_moneda(liq['monto_afc'])}")
        print(f"  Impuesto Único: {formatear_moneda(liq['impuesto_unico'])}")
        print(f"  Total Descuentos: {formatear_moneda(liq['total_descuentos'])}")
        print(f"  Sueldo Líquido: {formatear_moneda(liq['sueldo_liquido'])}")
        print(f"  --- Aportes Patronales ---")
        print(f"  SIS: {formatear_moneda(liq['aporte_patronal_sis'])}")
        print(f"  AFC: {formatear_moneda(liq['aporte_patronal_afc'])}")
        print(f"  CCAF: {formatear_moneda(liq['aporte_patronal_ccaf'])}")
    
    pausar()
