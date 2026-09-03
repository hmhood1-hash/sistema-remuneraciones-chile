# -*- coding: utf-8 -*-
"""Inicialización de la base de datos: creación de tablas y datos por defecto."""
from database.conexion import conexion_bd, obtener_ruta_base_datos
from database.models import TABLAS


def crear_tablas(conexion):
    cursor = conexion.cursor()
    for sentencia in TABLAS:
        cursor.execute(sentencia)


def _tabla_vacia(cursor, nombre_tabla):
    cursor.execute("SELECT COUNT(*) AS n FROM {}".format(nombre_tabla))
    return cursor.fetchone()[0] == 0


def cargar_datos_iniciales(conexion):
    """Carga datos base (AFP, Isapres, parámetros, tramos) si no existen aún."""
    cursor = conexion.cursor()

    if _tabla_vacia(cursor, "afp"):
        afps = [
            ("EMPART", "Empart", 10.49, "Antiguo"),
            ("SSS", "SSS", 10.49, "Antiguo"),
            ("CAPITAL", "Capital", 11.44, "Nuevo"),
            ("CUPRUM", "Cuprum", 11.44, "Nuevo"),
            ("HABITAT", "Hábitat", 11.27, "Nuevo"),
            ("MODELO", "Modelo", 10.58, "Nuevo"),
            ("PLANVITAL", "PlanVital", 11.10, "Nuevo"),
            ("PROVIDA", "Provida", 11.45, "Nuevo"),
            ("UNO", "Uno", 10.49, "Nuevo"),
        ]
        cursor.executemany(
            "INSERT INTO afp (codigo_afp, nombre, factor_cotizacion, sistema_previsional) "
            "VALUES (?, ?, ?, ?)",
            afps,
        )

    if _tabla_vacia(cursor, "isapre"):
        isapres = [
            ("FONASA", "Fonasa"),
            ("VIDATRES", "Vida Tres"),
            ("CONSALUD", "Consalud"),
            ("BANMEDICA", "Banmédica"),
            ("MASVIDA", "Más Vida"),
            ("CRUZBLANCA", "Cruz Blanca"),
        ]
        cursor.executemany(
            "INSERT INTO isapre (codigo_isapre, nombre) VALUES (?, ?)", isapres
        )

    if _tabla_vacia(cursor, "ccaf"):
        ccaf = [
            ("LOSANDES", "Los Andes"),
            ("LOSHEROES", "Los Héroes"),
            ("18DESEP", "18 de Septiembre"),
            ("LAARAUCANA", "La Araucana"),
        ]
        cursor.executemany("INSERT INTO ccaf (codigo_ccaf, nombre) VALUES (?, ?)", ccaf)

    if _tabla_vacia(cursor, "mutual"):
        mutuales = [
            ("ACHS", "Asociación Chilena de Seguridad"),
            ("IST", "Instituto de Seguridad del Trabajo"),
            ("MUSEG", "Mutual de Seguridad CChC"),
        ]
        cursor.executemany(
            "INSERT INTO mutual (codigo_mutual, nombre) VALUES (?, ?)", mutuales
        )

    if _tabla_vacia(cursor, "ahorro_previsional"):
        ahorros = [
            ("APV", "Ahorro Previsional Voluntario"),
            ("APVC", "Ahorro Previsional Voluntario Colectivo"),
            ("DEPCONV", "Depósito Convenido"),
        ]
        cursor.executemany(
            "INSERT INTO ahorro_previsional (codigo_ahorro, nombre) VALUES (?, ?)",
            ahorros,
        )

    if _tabla_vacia(cursor, "tipo_contrato"):
        tipos = [
            ("INDEF", "Indefinido"),
            ("PFIJO", "Plazo Fijo"),
            ("OBRA", "Por Obra o Faena"),
            ("PARCIAL", "Jornada Parcial"),
        ]
        cursor.executemany(
            "INSERT INTO tipo_contrato (codigo, descripcion) VALUES (?, ?)", tipos
        )

    if _tabla_vacia(cursor, "causal_finiquito"):
        causales = [
            ("ART159N2", "Renuncia Voluntaria"),
            ("ART159N4", "Vencimiento del Plazo Convenido"),
            ("ART159N5", "Conclusión del Trabajo o Servicio"),
            ("ART160", "Caducidad del Contrato (Art. 160)"),
            ("ART161", "Necesidades de la Empresa"),
            ("MUTUOACUERDO", "Mutuo Acuerdo de las Partes"),
        ]
        cursor.executemany(
            "INSERT INTO causal_finiquito (codigo, descripcion) VALUES (?, ?)",
            causales,
        )

    if _tabla_vacia(cursor, "parametros"):
        cursor.execute("INSERT INTO parametros (id) VALUES (1)")

    if _tabla_vacia(cursor, "tramo_carga_familiar"):
        tramos = [
            (1, "Tramo A", 0, 566512, 22006),
            (2, "Tramo B", 566513, 827919, 13505),
            (3, "Tramo C", 827920, 1291234, 4267),
            (4, "Tramo D", 1291235, None, 0),
            (5, "Tramo Especial", 0, 0, 0),
        ]
        cursor.executemany(
            "INSERT INTO tramo_carga_familiar (tramo, descripcion, desde, hasta, valor) "
            "VALUES (?, ?, ?, ?, ?)",
            tramos,
        )

    if _tabla_vacia(cursor, "tramo_impuesto_unico"):
        # Tabla de impuesto único mensual expresada en UTM (valores referenciales,
        # totalmente editables desde el módulo de parámetros).
        tramos_impuesto = [
            (1, 0, 13.5, 0.0, 0.0),
            (2, 13.5, 30, 0.04, 0.54),
            (3, 30, 50, 0.08, 1.74),
            (4, 50, 70, 0.135, 4.49),
            (5, 70, 90, 0.23, 11.14),
            (6, 90, 120, 0.304, 17.80),
            (7, 120, 150, 0.355, 23.92),
            (8, 150, 310, 0.37, 26.17),
            (9, 310, None, 0.40, 35.47),
        ]
        cursor.executemany(
            "INSERT INTO tramo_impuesto_unico (tramo, desde_utm, hasta_utm, factor, rebaja_utm) "
            "VALUES (?, ?, ?, ?, ?)",
            tramos_impuesto,
        )

    if _tabla_vacia(cursor, "haber_descuento"):
        haberes = [
            ("SBASE", "Sueldo Base", "Imponible", "Fijo", 0, 0, "N/A"),
            ("GRATIF", "Gratificación", "Imponible", "Porcentaje", 0, 25, "Sueldo base"),
            ("MOVIL", "Movilización", "Adicional Valor Dia-Hora", "Fijo", 0, 0, "N/A"),
            ("COLAC", "Colación", "Adicional Valor Dia-Hora", "Fijo", 0, 0, "N/A"),
            ("HHEE50", "Horas Extras 50%", "Horas Extras", "Variable", 0, 50, "Sueldo imponible"),
            ("APVDESC", "APV", "Descuento", "Variable", 0, 0, "N/A"),
        ]
        cursor.executemany(
            "INSERT INTO haber_descuento "
            "(codigo, nombre, clasificacion, clase, monto, porcentaje, base_porcentaje) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            haberes,
        )


def inicializar_base_datos(ruta_bd=None):
    """Crea (si es necesario) el archivo de base de datos, sus tablas y datos base.

    Devuelve la ruta absoluta de la base de datos utilizada.
    """
    with conexion_bd(ruta_bd) as conexion:
        crear_tablas(conexion)
        cargar_datos_iniciales(conexion)
    return ruta_bd or obtener_ruta_base_datos()


if __name__ == "__main__":
    ruta = inicializar_base_datos()
    print("Base de datos inicializada en: {}".format(ruta))
