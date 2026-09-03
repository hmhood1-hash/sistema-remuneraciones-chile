"""
Creación e inicialización de la base de datos SQLite del sistema de remuneraciones.
Define el esquema relacional completo y carga datos base (AFP, Isapres, tablas, etc).
"""
import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "remuneraciones.db")

SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS empresa (
    codigo INTEGER PRIMARY KEY AUTOINCREMENT,
    rut TEXT NOT NULL UNIQUE,
    razon_social TEXT NOT NULL,
    calle TEXT,
    numero TEXT,
    depto TEXT,
    poblacion_villa TEXT,
    comuna TEXT,
    ciudad TEXT,
    region TEXT,
    correo TEXT,
    fono TEXT,
    giro_comercial TEXT,
    codigo_actividad_economica TEXT,
    rep_legal_rut TEXT,
    rep_legal_nombres TEXT,
    rep_legal_ap_paterno TEXT,
    rep_legal_ap_materno TEXT
);

CREATE TABLE IF NOT EXISTS sucursal (
    codigo INTEGER PRIMARY KEY AUTOINCREMENT,
    empresa_codigo INTEGER NOT NULL REFERENCES empresa(codigo) ON DELETE CASCADE,
    nombre TEXT NOT NULL,
    direccion TEXT,
    region TEXT,
    ciudad TEXT,
    comuna TEXT,
    fono TEXT
);

CREATE TABLE IF NOT EXISTS centro_costo (
    codigo INTEGER PRIMARY KEY AUTOINCREMENT,
    empresa_codigo INTEGER NOT NULL REFERENCES empresa(codigo) ON DELETE CASCADE,
    descripcion TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS afp (
    codigo TEXT PRIMARY KEY,
    nombre TEXT NOT NULL,
    factor_cotizacion REAL NOT NULL DEFAULT 0,
    sistema_previsional TEXT NOT NULL DEFAULT 'Nuevo'
);

CREATE TABLE IF NOT EXISTS isapre (
    codigo TEXT PRIMARY KEY,
    nombre TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS ccaf (
    codigo TEXT PRIMARY KEY,
    nombre TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS mutual (
    codigo TEXT PRIMARY KEY,
    nombre TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS apv (
    codigo TEXT PRIMARY KEY,
    nombre TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tipo_contrato (
    codigo TEXT PRIMARY KEY,
    descripcion TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS causal_finiquito (
    codigo TEXT PRIMARY KEY,
    descripcion TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS trabajador (
    rut TEXT PRIMARY KEY,
    nombre TEXT NOT NULL,
    ap_paterno TEXT,
    ap_materno TEXT,
    fecha_nacimiento TEXT,
    codigo_empleado TEXT UNIQUE,
    calle TEXT,
    numero TEXT,
    dpto TEXT,
    comuna TEXT,
    correo TEXT,
    fono TEXT,
    sexo TEXT CHECK (sexo IN ('M', 'F', 'O')),
    estado_civil TEXT CHECK (estado_civil IN ('Soltero', 'Casado', 'Viudo', 'Separado')),
    empresa_codigo INTEGER REFERENCES empresa(codigo) ON DELETE SET NULL,
    activo INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS datos_laborales (
    trabajador_rut TEXT PRIMARY KEY REFERENCES trabajador(rut) ON DELETE CASCADE,
    sueldo_tipo TEXT CHECK (sueldo_tipo IN ('Mensual', 'Diario', 'Part Time', 'Empresarial')),
    sueldo_base REAL NOT NULL DEFAULT 0,
    gratificacion_tipo TEXT CHECK (gratificacion_tipo IN ('Mensual', 'Anual', 'Ninguna')),
    horas_semanales REAL,
    dias_laborales_semana INTEGER,
    fecha_contrato TEXT,
    cargo TEXT,
    horario TEXT,
    sucursal_codigo INTEGER REFERENCES sucursal(codigo),
    centro_costo_codigo INTEGER REFERENCES centro_costo(codigo),
    aplica_sis TEXT CHECK (aplica_sis IN ('S', 'N')) DEFAULT 'S'
);

CREATE TABLE IF NOT EXISTS datos_previsionales (
    trabajador_rut TEXT PRIMARY KEY REFERENCES trabajador(rut) ON DELETE CASCADE,
    afp_codigo TEXT REFERENCES afp(codigo),
    isapre_codigo TEXT REFERENCES isapre(codigo),
    modalidad_salud TEXT CHECK (modalidad_salud IN ('Pesos', 'UF', '7%', '7%+UF', '7%+UF+Pesos')) DEFAULT '7%',
    cotizacion_pactada REAL DEFAULT 0,
    tope_salud TEXT CHECK (tope_salud IN ('UF Actual', 'UF Anterior')) DEFAULT 'UF Actual',
    seguro_cesantia_tipo TEXT CHECK (seguro_cesantia_tipo IN ('Plazo Fijo', 'Indefinido')) DEFAULT 'Indefinido',
    fecha_inicio_afc TEXT,
    fecha_termino_afc TEXT,
    afp_cotiza_afc TEXT CHECK (afp_cotiza_afc IN ('S', 'N')) DEFAULT 'S',
    tipo_trabajador TEXT CHECK (tipo_trabajador IN (
        'Activo No Pensionado', 'Pensionado y Cotiza', 'Pensionado No Cotiza', 'Activo Mayor 60/65'
    )) DEFAULT 'Activo No Pensionado'
);

CREATE TABLE IF NOT EXISTS carga_familiar (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    trabajador_rut TEXT NOT NULL REFERENCES trabajador(rut) ON DELETE CASCADE,
    rut_carga TEXT NOT NULL,
    nombre TEXT NOT NULL,
    fecha_inicio TEXT,
    fecha_vencimiento TEXT,
    tipo TEXT CHECK (tipo IN ('Simple', 'Materna', 'Invalidez')) DEFAULT 'Simple',
    parentesco TEXT CHECK (parentesco IN ('Hijo', 'Conyuge', 'Progenitor', 'Hermano'))
);

CREATE TABLE IF NOT EXISTS haber_descuento (
    codigo INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    tipo TEXT CHECK (tipo IN ('Haber', 'Descuento')) NOT NULL DEFAULT 'Haber',
    clasificacion TEXT CHECK (clasificacion IN (
        'Imponible', 'Tributable', 'Adicional HE', 'Adicional Valor Dia/Hora', 'Horas Extras', 'No Imponible'
    )) NOT NULL,
    clase TEXT CHECK (clase IN ('Fijo', 'Variable', 'Valor Diario', 'Semana Corrida', 'Porcentaje')) NOT NULL,
    monto REAL DEFAULT 0,
    porcentaje REAL DEFAULT 0,
    base_calculo TEXT CHECK (base_calculo IN ('Sueldo Base', 'Sueldo Imponible', 'Ninguna')) DEFAULT 'Ninguna'
);

CREATE TABLE IF NOT EXISTS parametros (
    anio INTEGER PRIMARY KEY,
    sueldo_minimo REAL NOT NULL,
    sueldo_minimo_menor_mayor REAL NOT NULL,
    tope_gratificacion_mensual REAL NOT NULL,
    tope_imponible_afp_uf REAL NOT NULL,
    tope_imponible_reg_antiguo_uf REAL NOT NULL,
    tope_afc_uf REAL NOT NULL,
    tope_apv_mensual_uf REAL NOT NULL,
    tope_apv_anual_uf REAL NOT NULL,
    tope_deposito_convenido_anual_uf REAL NOT NULL,
    aporte_patronal_pct REAL DEFAULT 0,
    aporte_adicional_pct REAL DEFAULT 0,
    factor_sss_pct REAL DEFAULT 0,
    factor_empart_pct REAL DEFAULT 0,
    ccaf_pct REAL DEFAULT 0,
    salud_pct REAL DEFAULT 7.0,
    afp_empleador_pct REAL DEFAULT 0,
    sis_empleador_pct REAL DEFAULT 1.88,
    expectativa_vida_pct REAL DEFAULT 0,
    rentabilidad_protegida_pct REAL DEFAULT 0,
    afc_trabajador_indefinido_pct REAL DEFAULT 0.6,
    afc_empleador_indefinido_pct REAL DEFAULT 2.4,
    afc_empleador_pfijo_pct REAL DEFAULT 3.0,
    plazo_indefinido_11anios_pct REAL DEFAULT 0,
    afc_casa_particular_pct REAL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS factor_actualizacion (
    anio INTEGER NOT NULL,
    mes INTEGER NOT NULL CHECK (mes BETWEEN 1 AND 12),
    factor REAL DEFAULT 0,
    utm REAL NOT NULL,
    uf REAL NOT NULL,
    PRIMARY KEY (anio, mes)
);

CREATE TABLE IF NOT EXISTS carga_familiar_tramo (
    tramo INTEGER PRIMARY KEY,
    desde REAL NOT NULL,
    hasta REAL NOT NULL,
    valor REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS impuesto_unico_tramo (
    tramo INTEGER PRIMARY KEY,
    desde_utm REAL NOT NULL,
    hasta_utm REAL,
    factor REAL NOT NULL,
    rebaja_utm REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS contrato (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    trabajador_rut TEXT NOT NULL REFERENCES trabajador(rut) ON DELETE CASCADE,
    nombre TEXT,
    nacionalidad TEXT,
    labor_ejecutar TEXT,
    establecimiento TEXT,
    horario TEXT,
    duracion_contrato TEXT,
    tipo_contrato_codigo TEXT REFERENCES tipo_contrato(codigo),
    forma_pago TEXT CHECK (forma_pago IN ('Mensual', 'Quincenal', 'Diario')) DEFAULT 'Mensual',
    sueldo_base REAL DEFAULT 0,
    movilizacion REAL DEFAULT 0,
    colacion REAL DEFAULT 0,
    gratificacion REAL DEFAULT 0,
    remuneracion_adicional REAL DEFAULT 0,
    fecha_inicio TEXT
);

CREATE TABLE IF NOT EXISTS finiquito (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    trabajador_rut TEXT NOT NULL REFERENCES trabajador(rut) ON DELETE CASCADE,
    nombre TEXT,
    fecha_inicio TEXT,
    fecha_termino TEXT,
    cargo TEXT,
    causal_codigo TEXT REFERENCES causal_finiquito(codigo)
);

CREATE TABLE IF NOT EXISTS vacaciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    trabajador_rut TEXT NOT NULL REFERENCES trabajador(rut) ON DELETE CASCADE,
    fecha_inicio TEXT NOT NULL,
    fecha_termino TEXT NOT NULL,
    dias_habiles INTEGER NOT NULL,
    tipo TEXT CHECK (tipo IN ('Legal', 'Progresivo', 'Anticipado')) DEFAULT 'Legal'
);

CREATE TABLE IF NOT EXISTS liquidacion (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    trabajador_rut TEXT NOT NULL REFERENCES trabajador(rut) ON DELETE CASCADE,
    empresa_codigo INTEGER NOT NULL REFERENCES empresa(codigo),
    anio INTEGER NOT NULL,
    mes INTEGER NOT NULL,
    sueldo_base REAL DEFAULT 0,
    gratificacion REAL DEFAULT 0,
    total_haberes_imponibles REAL DEFAULT 0,
    total_haberes_no_imponibles REAL DEFAULT 0,
    total_haberes REAL DEFAULT 0,
    monto_afp REAL DEFAULT 0,
    monto_salud REAL DEFAULT 0,
    monto_afc REAL DEFAULT 0,
    monto_apv REAL DEFAULT 0,
    base_tributable REAL DEFAULT 0,
    impuesto_unico REAL DEFAULT 0,
    otros_descuentos REAL DEFAULT 0,
    total_descuentos REAL DEFAULT 0,
    sueldo_liquido REAL DEFAULT 0,
    aporte_patronal_sis REAL DEFAULT 0,
    aporte_patronal_afc REAL DEFAULT 0,
    aporte_patronal_ccaf REAL DEFAULT 0,
    aporte_patronal_mutual REAL DEFAULT 0,
    fecha_calculo TEXT,
    UNIQUE (trabajador_rut, anio, mes)
);

CREATE TABLE IF NOT EXISTS liquidacion_detalle (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    liquidacion_id INTEGER NOT NULL REFERENCES liquidacion(id) ON DELETE CASCADE,
    haber_descuento_codigo INTEGER REFERENCES haber_descuento(codigo),
    descripcion TEXT NOT NULL,
    tipo TEXT CHECK (tipo IN ('Haber', 'Descuento')) NOT NULL,
    monto REAL NOT NULL DEFAULT 0
);
"""


def get_connection(db_path=DB_PATH):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    return conn


def _seed_data(conn):
    cur = conn.cursor()

    afps = [
        ("EMPART", "Empart", 0.0, "Antiguo"),
        ("SSS", "SSS", 0.0, "Antiguo"),
        ("CAPITAL", "Capital", 1.44, "Nuevo"),
        ("CUPRUM", "Cuprum", 1.44, "Nuevo"),
        ("HABITAT", "Habitat", 1.27, "Nuevo"),
        ("MODELO", "Modelo", 0.58, "Nuevo"),
        ("PLANVITAL", "PlanVital", 1.16, "Nuevo"),
        ("PROVIDA", "Provida", 1.45, "Nuevo"),
        ("UNO", "Uno", 0.49, "Nuevo"),
    ]
    cur.executemany(
        "INSERT OR IGNORE INTO afp (codigo, nombre, factor_cotizacion, sistema_previsional) VALUES (?, ?, ?, ?)",
        afps,
    )

    isapres = [
        ("FONASA", "Fonasa"),
        ("VIDATRES", "Vida Tres"),
        ("CONSALUD", "Consalud"),
        ("BANMEDICA", "Banmedica"),
        ("MASVIDA", "Mas Vida"),
        ("CRUZBLANCA", "Cruz Blanca"),
    ]
    cur.executemany("INSERT OR IGNORE INTO isapre (codigo, nombre) VALUES (?, ?)", isapres)

    cur.executemany(
        "INSERT OR IGNORE INTO tipo_contrato (codigo, descripcion) VALUES (?, ?)",
        [
            ("INDEF", "Contrato Indefinido"),
            ("PFIJO", "Contrato a Plazo Fijo"),
            ("FAENA", "Contrato por Obra o Faena"),
            ("PTIME", "Contrato Part Time"),
        ],
    )

    cur.executemany(
        "INSERT OR IGNORE INTO causal_finiquito (codigo, descripcion) VALUES (?, ?)",
        [
            ("ART159N2", "Renuncia Voluntaria"),
            ("ART159N4", "Vencimiento del Plazo Convenido"),
            ("ART159N5", "Conclusión del Trabajo o Servicio"),
            ("ART160", "Caducidad del Contrato (Falta grave)"),
            ("ART161", "Necesidades de la Empresa"),
            ("MUTUOACUERDO", "Mutuo Acuerdo de las Partes"),
        ],
    )

    # Tabla de impuesto único (valores referenciales en UTM, 8 tramos vigentes en Chile)
    tramos_impuesto = [
        (1, 0.0, 13.5, 0.0, 0.0),
        (2, 13.5, 30.0, 0.04, 0.54),
        (3, 30.0, 50.0, 0.08, 1.74),
        (4, 50.0, 70.0, 0.135, 4.49),
        (5, 70.0, 90.0, 0.23, 11.14),
        (6, 90.0, 120.0, 0.304, 17.80),
        (7, 120.0, 310.0, 0.35, 23.32),
        (8, 310.0, None, 0.40, 38.72),
    ]
    cur.executemany(
        "INSERT OR IGNORE INTO impuesto_unico_tramo (tramo, desde_utm, hasta_utm, factor, rebaja_utm) "
        "VALUES (?, ?, ?, ?, ?)",
        tramos_impuesto,
    )

    # Tramos de asignación familiar (referenciales, editables)
    tramos_carga = [
        (1, 0, 500000, 15000),
        (2, 500001, 750000, 9200),
        (3, 750001, 1200000, 2900),
        (4, 1200001, 99999999, 0),
        (5, 0, 0, 0),
    ]
    cur.executemany(
        "INSERT OR IGNORE INTO carga_familiar_tramo (tramo, desde, hasta, valor) VALUES (?, ?, ?, ?)",
        tramos_carga,
    )

    cur.execute("SELECT COUNT(*) AS c FROM parametros")
    if cur.fetchone()["c"] == 0:
        from datetime import date

        cur.execute(
            """INSERT INTO parametros (
                anio, sueldo_minimo, sueldo_minimo_menor_mayor, tope_gratificacion_mensual,
                tope_imponible_afp_uf, tope_imponible_reg_antiguo_uf, tope_afc_uf,
                tope_apv_mensual_uf, tope_apv_anual_uf, tope_deposito_convenido_anual_uf,
                aporte_patronal_pct, aporte_adicional_pct, factor_sss_pct, factor_empart_pct,
                ccaf_pct, salud_pct, afp_empleador_pct, sis_empleador_pct,
                expectativa_vida_pct, rentabilidad_protegida_pct,
                afc_trabajador_indefinido_pct, afc_empleador_indefinido_pct,
                afc_empleador_pfijo_pct, plazo_indefinido_11anios_pct, afc_casa_particular_pct
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                date.today().year,
                460000, 344337, 4.75 * 460000,
                87.8, 60.0, 131.9,
                50.0, 600.0, 900.0,
                0, 0, 0, 0,
                2.0, 7.0, 0, 1.88,
                0, 0,
                0.6, 2.4,
                3.0, 0, 0,
            ),
        )

    conn.commit()


def init_database(db_path=DB_PATH, seed=True):
    """Crea el esquema de la base de datos (si no existe) y carga datos base."""
    conn = get_connection(db_path)
    conn.executescript(SCHEMA)
    if seed:
        _seed_data(conn)
    conn.commit()
    return conn


if __name__ == "__main__":
    conn = init_database()
    print(f"Base de datos inicializada correctamente en: {DB_PATH}")
    conn.close()
