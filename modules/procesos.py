"""
Módulo de Procesos: Centralización Mensual y Actualización de Base de Datos.
"""
from datetime import date

from database.init_db import init_database
from ui.utils import titulo, pedir_entero, pausar, formatear_pesos
from modules.liquidacion import listar_liquidaciones


def menu_centralizacion_mensual():
    """Genera un resumen contable (centralización) de las liquidaciones de un período."""
    titulo("Centralización Mensual")
    empresa_codigo = pedir_entero("Código de empresa")
    anio = pedir_entero("Año", default=date.today().year)
    mes = pedir_entero("Mes (1-12)", default=date.today().month)

    liquidaciones = listar_liquidaciones(empresa_codigo=empresa_codigo, anio=anio, mes=mes)
    if not liquidaciones:
        print("No hay liquidaciones calculadas para ese período.")
        pausar()
        return

    resumen = {
        "Total Haberes": sum(liq["total_haberes"] for liq in liquidaciones),
        "Total AFP": sum(liq["monto_afp"] for liq in liquidaciones),
        "Total Salud": sum(liq["monto_salud"] for liq in liquidaciones),
        "Total AFC Trabajador": sum(liq["monto_afc"] for liq in liquidaciones),
        "Total Impuesto Único": sum(liq["impuesto_unico"] for liq in liquidaciones),
        "Total Líquido a Pagar": sum(liq["sueldo_liquido"] for liq in liquidaciones),
        "Total Aporte SIS": sum(liq["aporte_patronal_sis"] for liq in liquidaciones),
        "Total Aporte AFC Empleador": sum(liq["aporte_patronal_afc"] for liq in liquidaciones),
        "Total Aporte CCAF": sum(liq["aporte_patronal_ccaf"] for liq in liquidaciones),
        "Total Aporte Mutual": sum(liq["aporte_patronal_mutual"] for liq in liquidaciones),
    }

    print(f"\nCentralización Contable {mes:02d}/{anio} - Empresa {empresa_codigo}")
    print("-" * 60)
    for concepto, monto in resumen.items():
        print(f"  {concepto:<35}{formatear_pesos(monto):>15}")
    pausar()


def menu_actualiza_base_datos():
    """Re-ejecuta la creación del esquema de la base de datos (idempotente) y recarga datos base."""
    titulo("Actualiza Base de Datos")
    confirmar = input(
        "Esto recreará el esquema y verificará los datos base (AFP, Isapres, tablas, etc). ¿Continuar? (s/n): "
    ).strip().lower()
    if confirmar != "s":
        print("Operación cancelada.")
        pausar()
        return
    conn = init_database(seed=True)
    conn.close()
    print("Base de datos actualizada correctamente.")
    pausar()
