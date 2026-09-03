"""
Módulo de Cálculo de Liquidaciones de Sueldo.

Orquesta el cálculo profesional de la liquidación mensual de un trabajador:
haberes imponibles/no imponibles, descuentos previsionales, impuesto único,
descuentos adicionales, neto a pagar y aportes patronales.
"""
from datetime import date, datetime

from database.models import fetch_all, fetch_one, insert, delete
from ui.utils import titulo, pedir_rut, pedir_entero, imprimir_tabla, pausar, formatear_pesos
from modules.trabajador import obtener_trabajador, obtener_datos_laborales, obtener_datos_previsionales
from modules.parametros import obtener_parametros, obtener_factor_actualizacion, listar_tramos_impuesto_unico
from modules.haberes import listar_haberes_descuentos, calcular_monto_haber_descuento
from calculos.impuesto_unico import calcular_impuesto_unico
from calculos.previsiones import calcular_afp, calcular_salud, calcular_afc, calcular_tope_imponible_pesos
from calculos.aportes import calcular_aportes_patronales


def calcular_liquidacion(rut, empresa_codigo, anio, mes, haberes_adicionales=None, descuentos_adicionales=None):
    """
    Calcula la liquidación de sueldo de un trabajador para un período (anio, mes).

    haberes_adicionales / descuentos_adicionales: lista opcional de dicts
        {"descripcion": str, "monto": float, "imponible": bool}

    Retorna un dict con el detalle completo de la liquidación.
    """
    haberes_adicionales = haberes_adicionales or []
    descuentos_adicionales = descuentos_adicionales or []

    trabajador = obtener_trabajador(rut)
    if not trabajador:
        raise ValueError(f"Trabajador con RUT {rut} no encontrado.")

    datos_laborales = obtener_datos_laborales(rut)
    if not datos_laborales:
        raise ValueError(f"El trabajador {rut} no tiene datos laborales registrados.")

    datos_previsionales = obtener_datos_previsionales(rut) or {}

    parametros = obtener_parametros(anio)
    if not parametros:
        raise ValueError(f"No hay parámetros configurados para el año {anio}.")

    factor_mes = obtener_factor_actualizacion(anio, mes)
    if not factor_mes:
        raise ValueError(f"No hay factor de actualización (UTM/UF) configurado para {mes}/{anio}.")

    valor_utm = factor_mes["utm"]
    valor_uf = factor_mes["uf"]

    sueldo_base = datos_laborales["sueldo_base"]
    gratificacion = 0.0
    if datos_laborales["gratificacion_tipo"] == "Mensual":
        gratificacion = min(sueldo_base * 0.25, parametros["tope_gratificacion_mensual"])

    total_haberes_imponibles = sueldo_base + gratificacion
    total_haberes_no_imponibles = 0.0

    detalle_haberes = [
        {"descripcion": "Sueldo Base", "tipo": "Haber", "monto": sueldo_base},
    ]
    if gratificacion:
        detalle_haberes.append({"descripcion": "Gratificación Legal", "tipo": "Haber", "monto": gratificacion})

    for haber in haberes_adicionales:
        monto = haber["monto"]
        if haber.get("imponible", True):
            total_haberes_imponibles += monto
        else:
            total_haberes_no_imponibles += monto
        detalle_haberes.append({"descripcion": haber["descripcion"], "tipo": "Haber", "monto": monto})

    total_haberes = total_haberes_imponibles + total_haberes_no_imponibles

    tope_imponible_afp = calcular_tope_imponible_pesos(parametros["tope_imponible_afp_uf"], valor_uf)
    tope_afc = calcular_tope_imponible_pesos(parametros["tope_afc_uf"], valor_uf)

    afp_codigo = datos_previsionales.get("afp_codigo")
    afp = fetch_one("SELECT * FROM afp WHERE codigo = ?", (afp_codigo,)) if afp_codigo else None
    factor_cotizacion = afp["factor_cotizacion"] if afp else 0.0
    aplica_sis = datos_laborales.get("aplica_sis") == "S"

    resultado_afp = calcular_afp(
        total_haberes_imponibles, factor_cotizacion, tope_imponible_afp,
        aplica_sis=aplica_sis, sis_pct=parametros["sis_empleador_pct"],
    )

    resultado_salud = calcular_salud(
        total_haberes_imponibles, tope_imponible_afp,
        modalidad=datos_previsionales.get("modalidad_salud", "7%"),
        cotizacion_pactada=datos_previsionales.get("cotizacion_pactada", 7.0),
        plan_uf=datos_previsionales.get("cotizacion_pactada", 0.0),
        valor_uf=valor_uf,
    )

    tipo_contrato_afc = datos_previsionales.get("seguro_cesantia_tipo", "Indefinido")
    resultado_afc = calcular_afc(total_haberes_imponibles, tope_afc, tipo_contrato=tipo_contrato_afc)

    monto_apv = 0.0

    base_tributable = (
        total_haberes_imponibles
        - resultado_afp["monto_afp"]
        - resultado_salud["monto_salud"]
        - resultado_afc["monto_trabajador"]
        - monto_apv
    )
    base_tributable = max(0.0, base_tributable)

    tramos_impuesto = listar_tramos_impuesto_unico()
    resultado_impuesto = calcular_impuesto_unico(base_tributable, valor_utm, tramos_impuesto)

    otros_descuentos = 0.0
    detalle_descuentos = [
        {"descripcion": f"AFP {afp_codigo or ''}", "tipo": "Descuento", "monto": resultado_afp["monto_afp"]},
        {"descripcion": "Salud", "tipo": "Descuento", "monto": resultado_salud["monto_salud"]},
    ]
    if resultado_afc["monto_trabajador"]:
        detalle_descuentos.append({
            "descripcion": "Seguro de Cesantía (AFC)", "tipo": "Descuento",
            "monto": resultado_afc["monto_trabajador"],
        })
    if resultado_impuesto["impuesto_pesos"]:
        detalle_descuentos.append({
            "descripcion": "Impuesto Único", "tipo": "Descuento", "monto": resultado_impuesto["impuesto_pesos"],
        })

    for descuento in descuentos_adicionales:
        otros_descuentos += descuento["monto"]
        detalle_descuentos.append(
            {"descripcion": descuento["descripcion"], "tipo": "Descuento", "monto": descuento["monto"]}
        )

    total_descuentos = (
        resultado_afp["monto_afp"]
        + resultado_salud["monto_salud"]
        + resultado_afc["monto_trabajador"]
        + resultado_impuesto["impuesto_pesos"]
        + otros_descuentos
    )

    sueldo_liquido = total_haberes - total_descuentos

    aportes = calcular_aportes_patronales(
        total_haberes_imponibles, tope_imponible_afp, parametros, tipo_contrato=tipo_contrato_afc,
        aplica_sis=aplica_sis,
    )

    liquidacion = {
        "trabajador_rut": rut,
        "empresa_codigo": empresa_codigo,
        "anio": anio,
        "mes": mes,
        "sueldo_base": sueldo_base,
        "gratificacion": gratificacion,
        "total_haberes_imponibles": round(total_haberes_imponibles),
        "total_haberes_no_imponibles": round(total_haberes_no_imponibles),
        "total_haberes": round(total_haberes),
        "monto_afp": resultado_afp["monto_afp"],
        "monto_salud": resultado_salud["monto_salud"],
        "monto_afc": resultado_afc["monto_trabajador"],
        "monto_apv": round(monto_apv),
        "base_tributable": round(base_tributable),
        "impuesto_unico": resultado_impuesto["impuesto_pesos"],
        "otros_descuentos": round(otros_descuentos),
        "total_descuentos": round(total_descuentos),
        "sueldo_liquido": round(sueldo_liquido),
        "aporte_patronal_sis": aportes["aporte_sis"],
        "aporte_patronal_afc": aportes["aporte_afc"],
        "aporte_patronal_ccaf": aportes["aporte_ccaf"],
        "aporte_patronal_mutual": aportes["aporte_mutual"],
        "fecha_calculo": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        "detalle_haberes": detalle_haberes,
        "detalle_descuentos": detalle_descuentos,
    }
    return liquidacion


def guardar_liquidacion(liquidacion):
    """Persiste la liquidación calculada (cabecera + detalle) en la base de datos."""
    detalle_haberes = liquidacion.pop("detalle_haberes", [])
    detalle_descuentos = liquidacion.pop("detalle_descuentos", [])

    delete(
        "liquidacion",
        "trabajador_rut = ? AND anio = ? AND mes = ?",
        (liquidacion["trabajador_rut"], liquidacion["anio"], liquidacion["mes"]),
    )
    liquidacion_id = insert("liquidacion", liquidacion)

    for item in detalle_haberes + detalle_descuentos:
        insert("liquidacion_detalle", {
            "liquidacion_id": liquidacion_id,
            "haber_descuento_codigo": None,
            "descripcion": item["descripcion"],
            "tipo": item["tipo"],
            "monto": item["monto"],
        })

    liquidacion["detalle_haberes"] = detalle_haberes
    liquidacion["detalle_descuentos"] = detalle_descuentos
    return liquidacion_id


def obtener_liquidacion(rut, anio, mes):
    return fetch_one(
        "SELECT * FROM liquidacion WHERE trabajador_rut = ? AND anio = ? AND mes = ?", (rut, anio, mes)
    )


def listar_detalle_liquidacion(liquidacion_id):
    return fetch_all("SELECT * FROM liquidacion_detalle WHERE liquidacion_id = ?", (liquidacion_id,))


def listar_liquidaciones(empresa_codigo=None, anio=None, mes=None):
    query = "SELECT * FROM liquidacion WHERE 1=1"
    params = []
    if empresa_codigo:
        query += " AND empresa_codigo = ?"
        params.append(empresa_codigo)
    if anio:
        query += " AND anio = ?"
        params.append(anio)
    if mes:
        query += " AND mes = ?"
        params.append(mes)
    query += " ORDER BY trabajador_rut"
    return fetch_all(query, tuple(params))


def _imprimir_liquidacion(liquidacion, trabajador):
    titulo("LIQUIDACIÓN DE SUELDO")
    print(f"Trabajador: {trabajador['nombre']} {trabajador['ap_paterno']} {trabajador['ap_materno'] or ''}")
    print(f"RUT: {trabajador['rut']}    Período: {liquidacion['mes']:02d}/{liquidacion['anio']}")
    print("-" * 60)
    print("HABERES:")
    for h in liquidacion["detalle_haberes"]:
        print(f"  {h['descripcion']:<35}{formatear_pesos(h['monto']):>15}")
    print(f"  {'TOTAL HABERES':<35}{formatear_pesos(liquidacion['total_haberes']):>15}")
    print("-" * 60)
    print("DESCUENTOS:")
    for d in liquidacion["detalle_descuentos"]:
        print(f"  {d['descripcion']:<35}{formatear_pesos(d['monto']):>15}")
    print(f"  {'TOTAL DESCUENTOS':<35}{formatear_pesos(liquidacion['total_descuentos']):>15}")
    print("-" * 60)
    print(f"  {'SUELDO LÍQUIDO A PAGAR':<35}{formatear_pesos(liquidacion['sueldo_liquido']):>15}")
    print("-" * 60)
    print("APORTES PATRONALES (informativo):")
    print(f"  {'SIS':<35}{formatear_pesos(liquidacion['aporte_patronal_sis']):>15}")
    print(f"  {'AFC Empleador':<35}{formatear_pesos(liquidacion['aporte_patronal_afc']):>15}")
    print(f"  {'CCAF':<35}{formatear_pesos(liquidacion['aporte_patronal_ccaf']):>15}")
    print(f"  {'Mutual':<35}{formatear_pesos(liquidacion['aporte_patronal_mutual']):>15}")


def menu_calcular_liquidacion():
    titulo("Calcular Liquidación Individual")
    rut = pedir_rut("RUT del trabajador")
    trabajador = obtener_trabajador(rut)
    if not trabajador:
        print("Trabajador no encontrado.")
        pausar()
        return

    empresa_codigo = trabajador.get("empresa_codigo") or pedir_entero("Código de empresa")
    anio = pedir_entero("Año", default=date.today().year)
    mes = pedir_entero("Mes (1-12)", default=date.today().month)

    haberes_adicionales = []
    descuentos_adicionales = []
    catalogo = listar_haberes_descuentos()
    if catalogo:
        print("Haberes/Descuentos disponibles en catálogo:")
        imprimir_tabla(catalogo)
        agregar = input("¿Desea agregar algún haber/descuento del catálogo? (s/n): ").strip().lower()
        while agregar == "s":
            codigo = pedir_entero("Código del haber/descuento")
            item = next((i for i in catalogo if i["codigo"] == codigo), None)
            if not item:
                print("Código no encontrado.")
            else:
                sueldo_base_ref = obtener_datos_laborales(rut)["sueldo_base"]
                monto = calcular_monto_haber_descuento(item, sueldo_base_ref, sueldo_base_ref)
                if item["tipo"] == "Haber":
                    haberes_adicionales.append({
                        "descripcion": item["nombre"], "monto": monto,
                        "imponible": item["clasificacion"] in ("Imponible", "Tributable"),
                    })
                else:
                    descuentos_adicionales.append({"descripcion": item["nombre"], "monto": monto})
            agregar = input("¿Agregar otro? (s/n): ").strip().lower()

    try:
        liquidacion = calcular_liquidacion(
            rut, empresa_codigo, anio, mes,
            haberes_adicionales=haberes_adicionales, descuentos_adicionales=descuentos_adicionales,
        )
    except ValueError as e:
        print(f"Error: {e}")
        pausar()
        return

    _imprimir_liquidacion(liquidacion, trabajador)
    guardar = input("\n¿Desea guardar esta liquidación? (s/n): ").strip().lower()
    if guardar == "s":
        guardar_liquidacion(liquidacion)
        print("Liquidación guardada.")
    pausar()


def menu_calcular_liquidaciones_empresa():
    titulo("Calcular Liquidaciones por Empresa")
    empresa_codigo = pedir_entero("Código de empresa")
    anio = pedir_entero("Año", default=date.today().year)
    mes = pedir_entero("Mes (1-12)", default=date.today().month)

    trabajadores = fetch_all("SELECT * FROM trabajador WHERE empresa_codigo = ?", (empresa_codigo,))
    if not trabajadores:
        print("No hay trabajadores para esta empresa.")
        pausar()
        return

    exitosas, con_error = 0, 0
    for trabajador in trabajadores:
        try:
            liquidacion = calcular_liquidacion(trabajador["rut"], empresa_codigo, anio, mes)
            guardar_liquidacion(liquidacion)
            exitosas += 1
        except ValueError as e:
            print(f"  - {trabajador['rut']}: {e}")
            con_error += 1

    print(f"\nLiquidaciones calculadas: {exitosas}. Con error: {con_error}.")
    pausar()


def menu_ver_liquidacion():
    titulo("Ver Liquidación Individual")
    rut = pedir_rut("RUT del trabajador")
    anio = pedir_entero("Año")
    mes = pedir_entero("Mes (1-12)")
    liquidacion = obtener_liquidacion(rut, anio, mes)
    if not liquidacion:
        print("No existe liquidación guardada para ese período.")
        pausar()
        return
    detalle = listar_detalle_liquidacion(liquidacion["id"])
    liquidacion["detalle_haberes"] = [d for d in detalle if d["tipo"] == "Haber"]
    liquidacion["detalle_descuentos"] = [d for d in detalle if d["tipo"] == "Descuento"]
    trabajador = obtener_trabajador(rut)
    _imprimir_liquidacion(liquidacion, trabajador)
    pausar()
