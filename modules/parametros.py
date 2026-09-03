"""
Módulo de gestión de Parámetros y Factores: sueldo mínimo, límites imponibles,
factores de cotización, tabla de impuesto único, factores de actualización
mensuales (UTM/UF) y tramos de cargas familiares.
"""
from datetime import date

from database.models import fetch_all, fetch_one, insert, update
from ui.utils import titulo, pedir_monto, pedir_entero, imprimir_tabla, pausar


MESES = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
]


# ---------- Parámetros anuales ----------

def obtener_parametros(anio=None):
    anio = anio or date.today().year
    return fetch_one("SELECT * FROM parametros WHERE anio = ?", (anio,))


def guardar_parametros(anio, data):
    if obtener_parametros(anio):
        return update("parametros", data, "anio = ?", (anio,))
    data["anio"] = anio
    return insert("parametros", data)


CAMPOS_PARAMETROS = [
    ("sueldo_minimo", "Sueldo Mínimo"),
    ("sueldo_minimo_menor_mayor", "Sueldo Mínimo Menores 18 / Mayores 65"),
    ("tope_gratificacion_mensual", "Tope Gratificación Mensual"),
    ("tope_imponible_afp_uf", "Tope Imponible AFP (UF)"),
    ("tope_imponible_reg_antiguo_uf", "Tope Imponible Régimen Antiguo (UF)"),
    ("tope_afc_uf", "Tope AFC (UF)"),
    ("tope_apv_mensual_uf", "Tope APV Mensual (UF)"),
    ("tope_apv_anual_uf", "Tope APV Anual (UF)"),
    ("tope_deposito_convenido_anual_uf", "Tope Depósito Convenido Anual (UF)"),
    ("aporte_patronal_pct", "Aporte Patronal (%)"),
    ("aporte_adicional_pct", "Aporte Adicional (%)"),
    ("factor_sss_pct", "Factor SSS (%)"),
    ("factor_empart_pct", "Factor Empart (%)"),
    ("ccaf_pct", "CCAF (%)"),
    ("salud_pct", "Salud (%)"),
    ("afp_empleador_pct", "AFP Empleador (%)"),
    ("sis_empleador_pct", "SIS Empleador (%)"),
    ("expectativa_vida_pct", "Expectativa de Vida (%)"),
    ("rentabilidad_protegida_pct", "Rentabilidad Protegida (%)"),
    ("afc_trabajador_indefinido_pct", "AFC Trabajador Indefinido (%)"),
    ("afc_empleador_indefinido_pct", "AFC Empleador Indefinido (%)"),
    ("afc_empleador_pfijo_pct", "AFC Empleador Plazo Fijo (%)"),
    ("plazo_indefinido_11anios_pct", "Plazo Indefinido 11 años o más (%)"),
    ("afc_casa_particular_pct", "AFC Casa Particular (%)"),
]


def menu_parametros():
    anio = pedir_entero("Año de parámetros", default=date.today().year)
    actuales = obtener_parametros(anio) or {}
    titulo(f"Parámetros del año {anio}")
    if actuales:
        imprimir_tabla([actuales])
    print("Ingrese los nuevos valores (parámetros generales):")
    data = {}
    for campo, etiqueta in CAMPOS_PARAMETROS:
        default = actuales.get(campo, 0) if actuales else 0
        data[campo] = pedir_monto(etiqueta, default=default)
    guardar_parametros(anio, data)
    print("Parámetros guardados.")
    pausar()


# ---------- Factores de actualización mensual (UTM, UF, factor) ----------

def obtener_factor_actualizacion(anio, mes):
    return fetch_one("SELECT * FROM factor_actualizacion WHERE anio = ? AND mes = ?", (anio, mes))


def guardar_factor_actualizacion(anio, mes, data):
    if obtener_factor_actualizacion(anio, mes):
        return update("factor_actualizacion", data, "anio = ? AND mes = ?", (anio, mes))
    data["anio"] = anio
    data["mes"] = mes
    return insert("factor_actualizacion", data)


def menu_factores_actualizacion():
    titulo("Factores de Actualización Mensuales")
    anio = pedir_entero("Año", default=date.today().year)
    print(f"Ingrese Factor, UTM y UF para cada mes del año {anio}:")
    for idx, nombre_mes in enumerate(MESES, start=1):
        actual = obtener_factor_actualizacion(anio, idx) or {}
        print(f"-- {nombre_mes} --")
        factor = pedir_monto("  Factor", default=actual.get("factor", 0))
        utm = pedir_monto("  UTM", default=actual.get("utm", 0))
        uf = pedir_monto("  UF", default=actual.get("uf", 0))
        guardar_factor_actualizacion(anio, idx, {"factor": factor, "utm": utm, "uf": uf})
    print("Factores de actualización guardados.")
    pausar()


def menu_listar_factores_actualizacion():
    titulo("Listado de Factores de Actualización")
    anio = pedir_entero("Año", default=date.today().year)
    filas = fetch_all("SELECT * FROM factor_actualizacion WHERE anio = ? ORDER BY mes", (anio,))
    imprimir_tabla(filas)
    pausar()


# ---------- Tramos de Cargas Familiares ----------

def listar_tramos_carga_familiar():
    return fetch_all("SELECT * FROM carga_familiar_tramo ORDER BY tramo")


def menu_tramos_carga_familiar():
    titulo("Tramos de Cargas Familiares (editables)")
    imprimir_tabla(listar_tramos_carga_familiar())
    tramo = pedir_entero("Tramo a editar (1-5)")
    actual = fetch_one("SELECT * FROM carga_familiar_tramo WHERE tramo = ?", (tramo,))
    if not actual:
        print("Tramo inválido.")
        pausar()
        return
    desde = pedir_monto("Desde", default=actual["desde"])
    hasta = pedir_monto("Hasta", default=actual["hasta"])
    valor = pedir_monto("Valor", default=actual["valor"])
    update("carga_familiar_tramo", {"desde": desde, "hasta": hasta, "valor": valor}, "tramo = ?", (tramo,))
    print("Tramo actualizado.")
    pausar()


# ---------- Tabla de Impuesto Único (editable, en UTM) ----------

def listar_tramos_impuesto_unico():
    return fetch_all("SELECT * FROM impuesto_unico_tramo ORDER BY tramo")


def menu_tabla_impuesto_unico():
    titulo("Tabla de Impuesto Único (en UTM)")
    imprimir_tabla(listar_tramos_impuesto_unico())
    print("¿Desea editar un tramo o agregar uno nuevo?")
    tramo = pedir_entero("Número de tramo (8 o 9 tramos habituales)")
    actual = fetch_one("SELECT * FROM impuesto_unico_tramo WHERE tramo = ?", (tramo,))
    desde_utm = pedir_monto("Desde (UTM)", default=actual["desde_utm"] if actual else 0)
    hasta_utm_str = input(
        f"Hasta (UTM) [dejar vacío para tramo sin límite superior"
        f"{', actual: ' + str(actual['hasta_utm']) if actual and actual['hasta_utm'] is not None else ''}]: "
    ).strip()
    hasta_utm = float(hasta_utm_str) if hasta_utm_str else None
    factor = pedir_monto("Factor", default=actual["factor"] if actual else 0)
    rebaja_utm = pedir_monto("Rebaja (UTM)", default=actual["rebaja_utm"] if actual else 0)

    if actual:
        update(
            "impuesto_unico_tramo",
            {"desde_utm": desde_utm, "hasta_utm": hasta_utm, "factor": factor, "rebaja_utm": rebaja_utm},
            "tramo = ?",
            (tramo,),
        )
    else:
        insert(
            "impuesto_unico_tramo",
            {
                "tramo": tramo, "desde_utm": desde_utm, "hasta_utm": hasta_utm,
                "factor": factor, "rebaja_utm": rebaja_utm,
            },
        )
    print("Tramo de impuesto único guardado.")
    pausar()


def menu_tabla_impuesto_unico_pesos():
    """Muestra la tabla de impuesto único convertida a pesos según la UTM del mes/año indicado."""
    titulo("Tabla de Impuesto Único ($)")
    anio = pedir_entero("Año", default=date.today().year)
    mes = pedir_entero("Mes (1-12)")
    factor_mes = obtener_factor_actualizacion(anio, mes)
    if not factor_mes:
        print("No hay UTM registrada para ese año/mes.")
        pausar()
        return
    valor_utm = factor_mes["utm"]
    tramos = listar_tramos_impuesto_unico()
    filas = []
    for t in tramos:
        filas.append({
            "tramo": t["tramo"],
            "desde_$": round(t["desde_utm"] * valor_utm),
            "hasta_$": round(t["hasta_utm"] * valor_utm) if t["hasta_utm"] is not None else "Sin límite",
            "factor": t["factor"],
            "rebaja_$": round(t["rebaja_utm"] * valor_utm),
        })
    imprimir_tabla(filas)
    pausar()
