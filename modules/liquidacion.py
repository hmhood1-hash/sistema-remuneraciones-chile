# -*- coding: utf-8 -*-
"""Cálculo y persistencia de Liquidaciones de Sueldo."""
from datetime import datetime

from database.conexion import conexion_bd
from modules.parametros import (
    obtener_parametros,
    obtener_factor_mensual,
    listar_tramos_impuesto_unico,
    obtener_valor_carga_familiar,
)
from modules.trabajador import obtener_trabajador, contar_cargas_familiares_vigentes
from modules.previsional import obtener_afp
from calculos.previsiones import calcular_afp, calcular_salud, calcular_seguro_cesantia
from calculos.impuesto_unico import calcular_impuesto_unico
from calculos.aportes import calcular_aportes_patronales


def calcular_liquidacion(codigo_empleado, anio, mes, haberes_adicionales=None,
                          dias_trabajados=30, ruta_bd=None):
    """Calcula la liquidación de sueldo de un trabajador para un período dado.

    ``haberes_adicionales`` es una lista opcional de dicts con llaves:
    ``codigo``, ``descripcion``, ``monto``, ``imponible`` (bool) y
    ``tributable`` (bool, por defecto igual a ``imponible``).

    Devuelve un diccionario con el detalle completo de la liquidación
    (sin guardar en la base de datos).
    """
    trabajador = obtener_trabajador(codigo_empleado, ruta_bd)
    if trabajador is None:
        raise ValueError("Trabajador no encontrado: {}".format(codigo_empleado))

    parametros = obtener_parametros(ruta_bd)
    factor_mes = obtener_factor_mensual(anio, mes, ruta_bd) or {}
    valor_utm = factor_mes.get("utm") or parametros["utm"]
    valor_uf = factor_mes.get("uf") or parametros["uf_afp_isapre"]

    afp = obtener_afp(trabajador["codigo_afp"], ruta_bd) if trabajador["codigo_afp"] else None
    factor_cotizacion_afp = afp["factor_cotizacion"] if afp else 0.0

    haberes_adicionales = haberes_adicionales or []

    sueldo_base = trabajador["sueldo_base"] or 0
    # Proporción de días trabajados sobre 30 (para sueldos mensuales).
    proporcion_dias = min(dias_trabajados, 30) / 30.0
    sueldo_base_proporcional = round(sueldo_base * proporcion_dias, 0)

    total_haberes_imponibles = sueldo_base_proporcional
    total_haberes_no_imponibles = 0.0

    for haber in haberes_adicionales:
        monto = haber.get("monto", 0) or 0
        if haber.get("imponible", False):
            total_haberes_imponibles += monto
        else:
            total_haberes_no_imponibles += monto

    total_ingreso_bruto = total_haberes_imponibles + total_haberes_no_imponibles

    # --- Descuentos previsionales ---
    tope_afp_uf = parametros["tope_imponible_afp_uf"]
    tipo_trabajador = trabajador["tipo_trabajador"] or "Activo No Pensionado"

    monto_afp = calcular_afp(
        total_haberes_imponibles, factor_cotizacion_afp, tope_afp_uf, valor_uf, tipo_trabajador
    )
    monto_salud = calcular_salud(
        total_haberes_imponibles,
        tope_afp_uf,
        valor_uf,
        trabajador["cotizacion_pactada"],
        tipo_trabajador,
    )
    monto_seguro_cesantia = calcular_seguro_cesantia(
        total_haberes_imponibles,
        tope_afp_uf,
        valor_uf,
        trabajador["seguro_cesantia"],
        parametros["afc_trabajador_indefinido_pct"],
    )
    monto_apv = 0.0  # Opcional, según pacto (se puede sumar vía haberes_adicionales).

    total_descuentos_previsionales = (
        monto_afp + monto_salud + monto_seguro_cesantia + monto_apv
    )

    # --- Impuesto único ---
    fecha_referencia = "{:04d}-{:02d}-01".format(anio, mes)
    num_cargas = contar_cargas_familiares_vigentes(codigo_empleado, fecha_referencia, ruta_bd)
    valor_carga = obtener_valor_carga_familiar(total_haberes_imponibles, ruta_bd)
    monto_cargas_familiares = num_cargas * valor_carga

    base_tributable = total_ingreso_bruto - total_descuentos_previsionales
    tramos_impuesto = listar_tramos_impuesto_unico(ruta_bd)
    impuesto_unico = calcular_impuesto_unico(
        base_tributable, valor_utm, tramos_impuesto, monto_cargas_familiares
    )

    total_otros_descuentos = 0.0
    total_descuentos = total_descuentos_previsionales + impuesto_unico + total_otros_descuentos
    sueldo_liquido = total_ingreso_bruto - total_descuentos

    # --- Aportes patronales ---
    aportes = calcular_aportes_patronales(
        total_haberes_imponibles,
        tope_afp_uf,
        valor_uf,
        parametros,
        trabajador["aplica_sis"],
        trabajador["seguro_cesantia"],
    )
    costo_total_empresa = sueldo_liquido + total_descuentos_previsionales + impuesto_unico \
        + aportes["total_aportes_patronales"]
    # El costo total para la empresa es el líquido más todo lo que la empresa paga:
    # sus propios aportes patronales más lo que ya estaba incluido en el bruto.
    costo_total_empresa = total_ingreso_bruto + aportes["total_aportes_patronales"]

    return {
        "codigo_empleado": codigo_empleado,
        "codigo_empresa": trabajador["codigo_empresa"],
        "anio": anio,
        "mes": mes,
        "dias_trabajados": dias_trabajados,
        "sueldo_base": sueldo_base_proporcional,
        "total_haberes_imponibles": total_haberes_imponibles,
        "total_haberes_no_imponibles": total_haberes_no_imponibles,
        "total_ingreso_bruto": total_ingreso_bruto,
        "monto_afp": monto_afp,
        "monto_salud": monto_salud,
        "monto_seguro_cesantia": monto_seguro_cesantia,
        "monto_apv": monto_apv,
        "total_descuentos_previsionales": total_descuentos_previsionales,
        "base_tributable": base_tributable,
        "impuesto_unico": impuesto_unico,
        "total_otros_descuentos": total_otros_descuentos,
        "total_descuentos": total_descuentos,
        "sueldo_liquido": sueldo_liquido,
        "aporte_patronal_afp": aportes["aporte_patronal_afp"],
        "aporte_sis": aportes["aporte_sis"],
        "aporte_afc_empleador": aportes["aporte_afc_empleador"],
        "aporte_ccaf": aportes["aporte_ccaf"],
        "total_aportes_patronales": aportes["total_aportes_patronales"],
        "costo_total_empresa": costo_total_empresa,
        "haberes_adicionales": haberes_adicionales,
    }


def guardar_liquidacion(liquidacion, ruta_bd=None):
    """Persiste una liquidación calculada (ver :func:`calcular_liquidacion`)."""
    campos = (
        "codigo_empleado", "codigo_empresa", "anio", "mes", "dias_trabajados",
        "sueldo_base", "total_haberes_imponibles", "total_haberes_no_imponibles",
        "total_ingreso_bruto", "monto_afp", "monto_salud", "monto_seguro_cesantia",
        "monto_apv", "total_descuentos_previsionales", "base_tributable",
        "impuesto_unico", "total_otros_descuentos", "total_descuentos",
        "sueldo_liquido", "aporte_patronal_afp", "aporte_sis",
        "aporte_afc_empleador", "aporte_ccaf", "total_aportes_patronales",
        "costo_total_empresa",
    )
    valores = [liquidacion[campo] for campo in campos]
    fecha_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with conexion_bd(ruta_bd) as conexion:
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO liquidacion ({}, fecha_creacion) VALUES ({}, ?) "
            "ON CONFLICT(codigo_empleado, anio, mes) DO UPDATE SET {}".format(
                ", ".join(campos),
                ", ".join(["?"] * len(campos)),
                ", ".join("{0} = excluded.{0}".format(campo) for campo in campos),
            ),
            valores + [fecha_creacion],
        )
        id_liquidacion = cursor.lastrowid
        if not id_liquidacion:
            fila = conexion.execute(
                "SELECT id_liquidacion FROM liquidacion "
                "WHERE codigo_empleado = ? AND anio = ? AND mes = ?",
                (liquidacion["codigo_empleado"], liquidacion["anio"], liquidacion["mes"]),
            ).fetchone()
            id_liquidacion = fila[0] if fila else None

        cursor.execute("DELETE FROM liquidacion_detalle WHERE id_liquidacion = ?", (id_liquidacion,))
        for haber in liquidacion.get("haberes_adicionales", []):
            cursor.execute(
                "INSERT INTO liquidacion_detalle "
                "(id_liquidacion, codigo_haber_descuento, descripcion, cantidad, monto, tipo) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (
                    id_liquidacion,
                    haber.get("codigo"),
                    haber.get("descripcion", ""),
                    haber.get("cantidad", 1),
                    haber.get("monto", 0),
                    "Haber" if haber.get("monto", 0) >= 0 else "Descuento",
                ),
            )
        return id_liquidacion


def listar_liquidaciones(codigo_empresa=None, anio=None, mes=None, ruta_bd=None):
    condiciones = []
    parametros = []
    if codigo_empresa:
        condiciones.append("codigo_empresa = ?")
        parametros.append(codigo_empresa)
    if anio:
        condiciones.append("anio = ?")
        parametros.append(anio)
    if mes:
        condiciones.append("mes = ?")
        parametros.append(mes)
    where = " WHERE " + " AND ".join(condiciones) if condiciones else ""
    with conexion_bd(ruta_bd) as conexion:
        cursor = conexion.execute(
            "SELECT * FROM liquidacion{} ORDER BY anio DESC, mes DESC, codigo_empleado".format(where),
            parametros,
        )
        return [dict(fila) for fila in cursor.fetchall()]


def obtener_liquidacion(codigo_empleado, anio, mes, ruta_bd=None):
    with conexion_bd(ruta_bd) as conexion:
        cursor = conexion.execute(
            "SELECT * FROM liquidacion WHERE codigo_empleado = ? AND anio = ? AND mes = ?",
            (codigo_empleado, anio, mes),
        )
        fila = cursor.fetchone()
        return dict(fila) if fila else None


# ---------------------------------------------------------------------------
# Anticipos
# ---------------------------------------------------------------------------
def registrar_anticipo(datos, ruta_bd=None):
    campos = ("codigo_empleado", "anio", "mes", "fecha_pago", "monto", "observaciones")
    valores = tuple(datos.get(campo) for campo in campos)
    with conexion_bd(ruta_bd) as conexion:
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO anticipo ({}) VALUES ({})".format(
                ", ".join(campos), ", ".join(["?"] * len(campos))
            ),
            valores,
        )
        return cursor.lastrowid


def eliminar_anticipo(id_anticipo, ruta_bd=None):
    with conexion_bd(ruta_bd) as conexion:
        conexion.execute("DELETE FROM anticipo WHERE id_anticipo = ?", (id_anticipo,))


def listar_anticipos(codigo_empleado=None, anio=None, mes=None, ruta_bd=None):
    condiciones = []
    parametros = []
    if codigo_empleado:
        condiciones.append("codigo_empleado = ?")
        parametros.append(codigo_empleado)
    if anio:
        condiciones.append("anio = ?")
        parametros.append(anio)
    if mes:
        condiciones.append("mes = ?")
        parametros.append(mes)
    where = " WHERE " + " AND ".join(condiciones) if condiciones else ""
    with conexion_bd(ruta_bd) as conexion:
        cursor = conexion.execute(
            "SELECT * FROM anticipo{} ORDER BY fecha_pago DESC".format(where), parametros
        )
        return [dict(fila) for fila in cursor.fetchall()]
