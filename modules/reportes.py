"""
Módulo de informes y reportes
"""
from database.models import fetch_all, fetch_one
from ui.utils import titulo, pedir_rut, pedir_entero, imprimir_tabla, pausar


def menu_reportes():
    """
    Menú de informes y reportes
    """
    opciones = {
        0: ("Volver", lambda: None),
        1: ("Libro de Remuneraciones", libro_remuneraciones),
        2: ("Detalle Pago de Imposiciones", detalle_imposiciones),
        3: ("Ficha del Trabajador", ficha_trabajador),
        4: ("Informe de Vacaciones", informe_vacaciones),
        5: ("Resumen Empresa", resumen_empresa),
    }
    from ui.menus import _menu
    _menu(opciones, "Informes y Reportes")


def libro_remuneraciones():
    """
    Genera libro de remuneraciones
    """
    titulo("Libro de Remuneraciones")
    
    anio = pedir_entero("Año")
    mes = pedir_entero("Mes (1-12)")
    
    liquidaciones = fetch_all('liquidacion', {'anio': anio, 'mes': mes})
    
    if liquidaciones:
        print(f"\nMes {mes}/{anio}\n")
        columnas = ['trabajador_rut', 'sueldo_base', 'total_haberes', 'total_descuentos', 'sueldo_liquido']
        imprimir_tabla(liquidaciones, columnas)
        
        # Totales
        total_haberes = sum(l['total_haberes'] for l in liquidaciones)
        total_descuentos = sum(l['total_descuentos'] for l in liquidaciones)
        total_liquido = sum(l['sueldo_liquido'] for l in liquidaciones)
        
        print(f"\n  Total Haberes: ${total_haberes:,.0f}")
        print(f"  Total Descuentos: ${total_descuentos:,.0f}")
        print(f"  Total Líquido a Pagar: ${total_liquido:,.0f}")
    else:
        print("  * Sin liquidaciones para este período")
    
    pausar()


def detalle_imposiciones():
    """
    Detalle de pago de imposiciones
    """
    titulo("Detalle Pago de Imposiciones")
    
    anio = pedir_entero("Año")
    mes = pedir_entero("Mes (1-12)")
    
    liquidaciones = fetch_all('liquidacion', {'anio': anio, 'mes': mes})
    
    if liquidaciones:
        print(f"\nMes {mes}/{anio}\n")
        columnas = ['trabajador_rut', 'monto_afp', 'monto_salud', 'impuesto_unico']
        imprimir_tabla(liquidaciones, columnas)
        
        # Totales
        total_afp = sum(l['monto_afp'] for l in liquidaciones)
        total_salud = sum(l['monto_salud'] for l in liquidaciones)
        total_impuesto = sum(l['impuesto_unico'] for l in liquidaciones)
        
        print(f"\n  Total AFP: ${total_afp:,.0f}")
        print(f"  Total Salud: ${total_salud:,.0f}")
        print(f"  Total Impuesto: ${total_impuesto:,.0f}")
    else:
        print("  * Sin liquidaciones para este período")
    
    pausar()


def ficha_trabajador():
    """
    Genera ficha del trabajador
    """
    titulo("Ficha del Trabajador")
    
    rut = pedir_rut("RUT del Trabajador")
    
    trabajador = fetch_one('trabajador', {'rut': rut})
    if not trabajador:
        print("  * Trabajador no encontrado")
        pausar()
        return
    
    datos_laborales = fetch_one('datos_laborales', {'trabajador_rut': rut})
    datos_previsionales = fetch_one('datos_previsionales', {'trabajador_rut': rut})
    cargas = fetch_all('carga_familiar', {'trabajador_rut': rut})
    
    print(f"\n  Nombre: {trabajador['nombre']} {trabajador.get('ap_paterno', '')} {trabajador.get('ap_materno', '')}")
    print(f"  RUT: {rut}")
    print(f"  Sexo: {trabajador.get('sexo', '')}")
    print(f"  Estado Civil: {trabajador.get('estado_civil', '')}")
    
    if datos_laborales:
        print(f"\n  --- Datos Laborales ---")
        print(f"  Sueldo Base: ${datos_laborales['sueldo_base']:,.0f}")
        print(f"  Cargo: {datos_laborales.get('cargo', '')}")
        print(f"  Fecha Contrato: {datos_laborales.get('fecha_contrato', '')}")
    
    if datos_previsionales:
        print(f"\n  --- Datos Previsionales ---")
        print(f"  AFP: {datos_previsionales.get('afp_codigo', '')}")
        print(f"  Isapre: {datos_previsionales.get('isapre_codigo', '')}")
        print(f"  Tipo Trabajador: {datos_previsionales.get('tipo_trabajador', '')}")
    
    if cargas:
        print(f"\n  --- Cargas Familiares ---")
        for carga in cargas:
            print(f"    {carga['nombre']} ({carga['parentesco']})")
    
    pausar()


def informe_vacaciones():
    """
    Informe de vacaciones
    """
    titulo("Informe de Vacaciones")
    
    anio = pedir_entero("Año")
    
    vacaciones = fetch_all('vacacion', {'anio_laboral': anio})
    
    if vacaciones:
        print(f"\nAño {anio}\n")
        columnas = ['trabajador_rut', 'dias_acumulados', 'dias_tomados', 'dias_disponibles']
        imprimir_tabla(vacaciones, columnas)
    else:
        print("  * Sin registros de vacaciones para este año")
    
    pausar()


def resumen_empresa():
    """
    Resumen de nómina de la empresa
    """
    titulo("Resumen de Nómina de Empresa")
    
    empresa_codigo = pedir_entero("Código de Empresa")
    anio = pedir_entero("Año")
    mes = pedir_entero("Mes")
    
    liquidaciones = fetch_all('liquidacion', {'empresa_codigo': empresa_codigo, 'anio': anio, 'mes': mes})
    
    if liquidaciones:
        print(f"\nEmpresa {empresa_codigo} - {mes}/{anio}\n")
        print(f"  Número de Trabajadores: {len(liquidaciones)}")
        print(f"  Total Haberes: ${sum(l['total_haberes'] for l in liquidaciones):,.0f}")
        print(f"  Total Descuentos: ${sum(l['total_descuentos'] for l in liquidaciones):,.0f}")
        print(f"  Total Líquido: ${sum(l['sueldo_liquido'] for l in liquidaciones):,.0f}")
        print(f"  Costo Total (incluye aportes): ${sum(l['sueldo_liquido'] + l['aporte_patronal_sis'] + l['aporte_patronal_afc'] for l in liquidaciones):,.0f}")
    else:
        print("  * Sin liquidaciones para este período")
    
    pausar()
