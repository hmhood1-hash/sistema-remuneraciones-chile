"""
Módulo de Informes y Reportes:
- Libro de remuneraciones
- Detalle de pago de imposiciones
- Detalle de anticipos
- Ficha del trabajador
- Informe de vacaciones
- Certificado tributario de remuneraciones
"""
from datetime import date

from database.models import fetch_all
from ui.utils import titulo, pedir_entero, pedir_rut, imprimir_tabla, pausar, formatear_pesos
from modules.trabajador import obtener_trabajador, obtener_datos_laborales, obtener_datos_previsionales
from modules.liquidacion import listar_liquidaciones, listar_detalle_liquidacion
from modules.vacaciones import listar_vacaciones, dias_disponibles


def libro_remuneraciones(empresa_codigo, anio, mes):
    liquidaciones = listar_liquidaciones(empresa_codigo=empresa_codigo, anio=anio, mes=mes)
    filas = []
    for liq in liquidaciones:
        trabajador = obtener_trabajador(liq["trabajador_rut"])
        filas.append({
            "RUT": liq["trabajador_rut"],
            "Nombre": f"{trabajador['nombre']} {trabajador['ap_paterno']}" if trabajador else "",
            "Sueldo Base": formatear_pesos(liq["sueldo_base"]),
            "Total Haberes": formatear_pesos(liq["total_haberes"]),
            "Total Descuentos": formatear_pesos(liq["total_descuentos"]),
            "Líquido": formatear_pesos(liq["sueldo_liquido"]),
        })
    return filas


def menu_libro_remuneraciones():
    titulo("Libro de Remuneraciones")
    empresa_codigo = pedir_entero("Código de empresa")
    anio = pedir_entero("Año", default=date.today().year)
    mes = pedir_entero("Mes (1-12)", default=date.today().month)
    filas = libro_remuneraciones(empresa_codigo, anio, mes)
    imprimir_tabla(filas)
    if filas:
        total_liquido = sum(
            liq["sueldo_liquido"] for liq in listar_liquidaciones(empresa_codigo=empresa_codigo, anio=anio, mes=mes)
        )
        print(f"\nTotal líquido a pagar: {formatear_pesos(total_liquido)}")
    pausar()


def menu_detalle_pago_imposiciones():
    titulo("Detalle de Pago de Imposiciones")
    empresa_codigo = pedir_entero("Código de empresa")
    anio = pedir_entero("Año", default=date.today().year)
    mes = pedir_entero("Mes (1-12)", default=date.today().month)
    liquidaciones = listar_liquidaciones(empresa_codigo=empresa_codigo, anio=anio, mes=mes)
    filas = []
    total_afp = total_salud = total_afc = 0
    for liq in liquidaciones:
        datos_prev = obtener_datos_previsionales(liq["trabajador_rut"]) or {}
        filas.append({
            "RUT": liq["trabajador_rut"],
            "AFP": datos_prev.get("afp_codigo", ""),
            "Monto AFP": formatear_pesos(liq["monto_afp"]),
            "Isapre": datos_prev.get("isapre_codigo", ""),
            "Monto Salud": formatear_pesos(liq["monto_salud"]),
            "Monto AFC": formatear_pesos(liq["monto_afc"]),
        })
        total_afp += liq["monto_afp"]
        total_salud += liq["monto_salud"]
        total_afc += liq["monto_afc"]
    imprimir_tabla(filas)
    print(f"\nTotal AFP: {formatear_pesos(total_afp)}  Total Salud: {formatear_pesos(total_salud)}"
          f"  Total AFC: {formatear_pesos(total_afc)}")
    pausar()


def menu_detalle_anticipos():
    titulo("Detalle de Anticipos")
    empresa_codigo = pedir_entero("Código de empresa")
    anio = pedir_entero("Año", default=date.today().year)
    mes = pedir_entero("Mes (1-12)", default=date.today().month)
    liquidaciones = listar_liquidaciones(empresa_codigo=empresa_codigo, anio=anio, mes=mes)
    filas = []
    for liq in liquidaciones:
        detalle = listar_detalle_liquidacion(liq["id"])
        anticipos = [d for d in detalle if "anticipo" in d["descripcion"].lower()]
        for a in anticipos:
            filas.append({
                "RUT": liq["trabajador_rut"], "Descripción": a["descripcion"],
                "Monto": formatear_pesos(a["monto"]),
            })
    imprimir_tabla(filas)
    pausar()


def menu_ficha_trabajador():
    titulo("Ficha del Trabajador")
    rut = pedir_rut("RUT del trabajador")
    trabajador = obtener_trabajador(rut)
    if not trabajador:
        print("Trabajador no encontrado.")
        pausar()
        return
    datos_laborales = obtener_datos_laborales(rut) or {}
    datos_prev = obtener_datos_previsionales(rut) or {}

    print("DATOS PERSONALES")
    imprimir_tabla([trabajador])
    print("\nDATOS LABORALES")
    imprimir_tabla([datos_laborales] if datos_laborales else [])
    print("\nDATOS PREVISIONALES")
    imprimir_tabla([datos_prev] if datos_prev else [])
    print("\nCARGAS FAMILIARES")
    imprimir_tabla(fetch_all("SELECT * FROM carga_familiar WHERE trabajador_rut = ?", (rut,)))
    pausar()


def menu_informe_vacaciones():
    titulo("Informe de Vacaciones")
    rut = pedir_rut("RUT del trabajador (o Enter para ver todos)", obligatorio=False)
    if rut:
        imprimir_tabla(listar_vacaciones(rut))
        print(f"\nDías disponibles (referencial): {dias_disponibles(rut)}")
    else:
        imprimir_tabla(listar_vacaciones())
    pausar()


def menu_certificado_tributario():
    titulo("Certificado Tributario de Remuneraciones")
    rut = pedir_rut("RUT del trabajador")
    anio = pedir_entero("Año", default=date.today().year)
    trabajador = obtener_trabajador(rut)
    if not trabajador:
        print("Trabajador no encontrado.")
        pausar()
        return
    liquidaciones = fetch_all(
        "SELECT * FROM liquidacion WHERE trabajador_rut = ? AND anio = ? ORDER BY mes", (rut, anio)
    )
    if not liquidaciones:
        print("No hay liquidaciones registradas para ese año.")
        pausar()
        return

    total_haberes = sum(liq["total_haberes"] for liq in liquidaciones)
    total_imponible = sum(liq["total_haberes_imponibles"] for liq in liquidaciones)
    total_impuesto = sum(liq["impuesto_unico"] for liq in liquidaciones)

    print(f"Trabajador: {trabajador['nombre']} {trabajador['ap_paterno']}  RUT: {rut}")
    print(f"Año Tributario: {anio}")
    print("-" * 60)
    print(f"Total Rentas Brutas: {formatear_pesos(total_haberes)}")
    print(f"Total Rentas Imponibles: {formatear_pesos(total_imponible)}")
    print(f"Total Impuesto Único Retenido: {formatear_pesos(total_impuesto)}")
    pausar()
