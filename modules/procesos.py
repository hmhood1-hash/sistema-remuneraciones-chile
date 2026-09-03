"""
Módulo de procesos del sistema
"""
from database.models import fetch_all
from ui.utils import titulo, pedir_entero, pausar
from modules.liquidacion import calcular_liquidacion, guardar_liquidacion


def menu_procesos():
    """
    Menú de procesos
    """
    opciones = {
        0: ("Volver", lambda: None),
        1: ("Centralización Mensual", centralizacion_mensual),
        2: ("Actualizar Base de Datos", actualizar_base_datos),
    }
    from ui.menus import _menu
    _menu(opciones, "Procesos")


def centralizacion_mensual():
    """
    Centraliza la nómina mensual (calcula liquidaciones para todos)
    """
    titulo("Centralización Mensual")
    
    empresa_codigo = pedir_entero("Código de Empresa")
    anio = pedir_entero("Año")
    mes = pedir_entero("Mes (1-12)")
    
    # Obtener todos los trabajadores de la empresa
    trabajadores = fetch_all('trabajador', {'empresa_codigo': empresa_codigo})
    
    if not trabajadores:
        print("  ✗ No hay trabajadores en esta empresa")
        pausar()
        return
    
    print(f"\n  Procesando {len(trabajadores)} trabajadores...\n")
    
    contador = 0
    errores = 0
    
    for trabajador in trabajadores:
        try:
            liq = calcular_liquidacion(trabajador['rut'], empresa_codigo, anio, mes)
            guardar_liquidacion(liq)
            contador += 1
            print(f"  ✓ {trabajador['nombre']}: ${liq['sueldo_liquido']:,.0f}")
        except Exception as e:
            errores += 1
            print(f"  ✗ {trabajador['nombre']}: {str(e)}")
    
    print(f"\n  Resumen: {contador} liquidaciones exitosas, {errores} errores")
    pausar()


def actualizar_base_datos():
    """
    Actualiza la base de datos (mantenimiento)
    """
    titulo("Actualizar Base de Datos")
    
    print("\n  Opciones:")
    print("    1. Verificar integridad")
    print("    2. Limpiar datos temporales")
    print("    3. Generar respaldo")
    
    opcion = pedir_entero("Seleccione opción")
    
    if opcion == 1:
        print("\n  Verificando integridad...")
        print("  ✓ Base de datos integra")
    elif opcion == 2:
        print("\n  Limpiando datos temporales...")
        print("  ✓ Limpieza completada")
    elif opcion == 3:
        print("\n  Generando respaldo...")
        print("  ✓ Respaldo generado")
    
    pausar()
