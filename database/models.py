# -*- coding: utf-8 -*-
"""
Definición del esquema relacional completo de la base de datos SQLite.

Cada constante ``SQL_CREATE_*`` contiene la sentencia DDL de una tabla del
sistema. La lista :data:`TABLAS` se usa para crearlas todas en orden (respeta
las dependencias de claves foráneas).
"""

SQL_CREATE_EMPRESA = """
CREATE TABLE IF NOT EXISTS empresa (
    codigo_empresa INTEGER PRIMARY KEY AUTOINCREMENT,
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
    rep_legal_apellido_paterno TEXT,
    rep_legal_apellido_materno TEXT
);
"""

SQL_CREATE_SUCURSAL = """
CREATE TABLE IF NOT EXISTS sucursal (
    codigo_sucursal INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_empresa INTEGER NOT NULL,
    nombre TEXT NOT NULL,
    direccion TEXT,
    region TEXT,
    ciudad TEXT,
    comuna TEXT,
    fono TEXT,
    FOREIGN KEY (codigo_empresa) REFERENCES empresa (codigo_empresa)
);
"""

SQL_CREATE_CENTRO_COSTO = """
CREATE TABLE IF NOT EXISTS centro_costo (
    codigo_centro_costo TEXT PRIMARY KEY,
    descripcion TEXT NOT NULL,
    codigo_empresa INTEGER,
    FOREIGN KEY (codigo_empresa) REFERENCES empresa (codigo_empresa)
);
"""

SQL_CREATE_AFP = """
CREATE TABLE IF NOT EXISTS afp (
    codigo_afp TEXT PRIMARY KEY,
    nombre TEXT NOT NULL,
    factor_cotizacion REAL NOT NULL DEFAULT 0,
    sistema_previsional TEXT NOT NULL DEFAULT 'Nuevo'
);
"""

SQL_CREATE_ISAPRE = """
CREATE TABLE IF NOT EXISTS isapre (
    codigo_isapre TEXT PRIMARY KEY,
    nombre TEXT NOT NULL
);
"""

SQL_CREATE_CCAF = """
CREATE TABLE IF NOT EXISTS ccaf (
    codigo_ccaf TEXT PRIMARY KEY,
    nombre TEXT NOT NULL
);
"""

SQL_CREATE_MUTUAL = """
CREATE TABLE IF NOT EXISTS mutual (
    codigo_mutual TEXT PRIMARY KEY,
    nombre TEXT NOT NULL
);
"""

SQL_CREATE_AHORRO_PREVISIONAL = """
CREATE TABLE IF NOT EXISTS ahorro_previsional (
    codigo_ahorro TEXT PRIMARY KEY,
    nombre TEXT NOT NULL
);
"""

SQL_CREATE_TRABAJADOR = """
CREATE TABLE IF NOT EXISTS trabajador (
    codigo_empleado INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_empresa INTEGER NOT NULL,
    rut TEXT NOT NULL UNIQUE,
    nombres TEXT NOT NULL,
    apellido_paterno TEXT NOT NULL,
    apellido_materno TEXT,
    fecha_nacimiento TEXT,
    sexo TEXT CHECK (sexo IN ('M', 'F', 'O')),
    estado_civil TEXT CHECK (estado_civil IN ('Soltero', 'Casado', 'Viudo', 'Separado')),
    calle TEXT,
    numero TEXT,
    dpto TEXT,
    comuna TEXT,
    correo TEXT,
    fono TEXT,

    -- Datos laborales
    sueldo_tipo TEXT CHECK (sueldo_tipo IN ('Mensual', 'Diario', 'Part Time', 'Empresarial')),
    sueldo_base REAL DEFAULT 0,
    gratificacion_tipo TEXT CHECK (gratificacion_tipo IN ('Mensual', 'Anual')),
    horas_semanales REAL DEFAULT 45,
    dias_laborales_semana INTEGER DEFAULT 5,
    fecha_contrato TEXT,
    cargo TEXT,
    horarios TEXT,
    codigo_sucursal INTEGER,
    codigo_centro_costo TEXT,
    aplica_sis TEXT CHECK (aplica_sis IN ('S', 'N')) DEFAULT 'N',

    -- Datos previsionales
    codigo_afp TEXT,
    codigo_isapre TEXT,
    modalidad_salud TEXT CHECK (
        modalidad_salud IN ('Pesos', 'UF', '7%', '7%+UF', '7%+UF+pesos')
    ),
    cotizacion_pactada REAL DEFAULT 0,
    tope_salud TEXT,
    seguro_cesantia TEXT CHECK (seguro_cesantia IN ('Plazo Fijo', 'Indefinido')),
    fecha_inicio_afc TEXT,
    fecha_termino_afc TEXT,
    afp_cotiza_afc TEXT CHECK (afp_cotiza_afc IN ('S', 'N')) DEFAULT 'S',
    tipo_trabajador TEXT CHECK (
        tipo_trabajador IN (
            'Activo No Pensionado',
            'Pensionado y cotiza',
            'Pensionado no cotiza',
            'Activo > 60 o 65 años'
        )
    ) DEFAULT 'Activo No Pensionado',

    activo INTEGER NOT NULL DEFAULT 1,

    FOREIGN KEY (codigo_empresa) REFERENCES empresa (codigo_empresa),
    FOREIGN KEY (codigo_sucursal) REFERENCES sucursal (codigo_sucursal),
    FOREIGN KEY (codigo_centro_costo) REFERENCES centro_costo (codigo_centro_costo),
    FOREIGN KEY (codigo_afp) REFERENCES afp (codigo_afp),
    FOREIGN KEY (codigo_isapre) REFERENCES isapre (codigo_isapre)
);
"""

SQL_CREATE_CARGA_FAMILIAR = """
CREATE TABLE IF NOT EXISTS carga_familiar (
    id_carga INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_empleado INTEGER NOT NULL,
    rut_carga TEXT NOT NULL,
    nombre TEXT NOT NULL,
    fecha_inicio TEXT,
    fecha_vencimiento TEXT,
    tipo TEXT CHECK (tipo IN ('Simple', 'Materna', 'Invalidez')) DEFAULT 'Simple',
    parentesco TEXT CHECK (parentesco IN ('Hijo', 'Cónyuge', 'Progenitor', 'Hermano')),
    FOREIGN KEY (codigo_empleado) REFERENCES trabajador (codigo_empleado)
);
"""

SQL_CREATE_HABERES_DESCUENTOS = """
CREATE TABLE IF NOT EXISTS haber_descuento (
    codigo TEXT PRIMARY KEY,
    nombre TEXT NOT NULL,
    clasificacion TEXT CHECK (
        clasificacion IN (
            'Imponible', 'Tributable', 'Adicional HE',
            'Adicional Valor Dia-Hora', 'Horas Extras', 'Descuento'
        )
    ) NOT NULL,
    clase TEXT CHECK (
        clase IN ('Fijo', 'Variable', 'Valor diario', 'Semana corrida', 'Porcentaje')
    ) NOT NULL,
    monto REAL DEFAULT 0,
    porcentaje REAL DEFAULT 0,
    base_porcentaje TEXT CHECK (
        base_porcentaje IN ('Sueldo base', 'Sueldo imponible', 'N/A')
    ) DEFAULT 'N/A'
);
"""

SQL_CREATE_FACTOR_MENSUAL = """
CREATE TABLE IF NOT EXISTS factor_mensual (
    anio INTEGER NOT NULL,
    mes INTEGER NOT NULL CHECK (mes BETWEEN 1 AND 12),
    factor REAL DEFAULT 1,
    utm REAL DEFAULT 0,
    uf REAL DEFAULT 0,
    PRIMARY KEY (anio, mes)
);
"""

SQL_CREATE_TIPO_CONTRATO = """
CREATE TABLE IF NOT EXISTS tipo_contrato (
    codigo TEXT PRIMARY KEY,
    descripcion TEXT NOT NULL
);
"""

SQL_CREATE_CAUSAL_FINIQUITO = """
CREATE TABLE IF NOT EXISTS causal_finiquito (
    codigo TEXT PRIMARY KEY,
    descripcion TEXT NOT NULL
);
"""

SQL_CREATE_PARAMETROS = """
CREATE TABLE IF NOT EXISTS parametros (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    sueldo_minimo REAL DEFAULT 500000,
    sueldo_minimo_menor_18_mayor_65 REAL DEFAULT 373304,
    tope_gratificacion_mensual REAL DEFAULT 209396,
    tope_imponible_afp_uf REAL DEFAULT 87.8,
    tope_imponible_regimen_antiguo_uf REAL DEFAULT 60,
    tope_afc_uf REAL DEFAULT 131.9,
    tope_apv_mensual_uf REAL DEFAULT 50,
    tope_apv_anual_uf REAL DEFAULT 600,
    tope_deposito_convenido_anual_uf REAL DEFAULT 900,
    utm REAL DEFAULT 0,
    uf_afp_isapre REAL DEFAULT 0,
    uf_regimen_antiguo REAL DEFAULT 0,

    aporte_patronal_pct REAL DEFAULT 0,
    aporte_adicional_pct REAL DEFAULT 0,
    factor_sss_pct REAL DEFAULT 0,
    factor_empart_pct REAL DEFAULT 0,
    ccaf_pct REAL DEFAULT 0,
    salud_pct REAL DEFAULT 7,
    afp_empleador_pct REAL DEFAULT 0,
    sis_empleador_pct REAL DEFAULT 1.53,
    expectativa_vida_pct REAL DEFAULT 0,
    rentabilidad_protegida_pct REAL DEFAULT 0,
    afc_trabajador_indefinido_pct REAL DEFAULT 0.6,
    afc_empleador_indefinido_pct REAL DEFAULT 2.4,
    afc_empleador_plazo_fijo_pct REAL DEFAULT 3.0,
    plazo_indefinido_11_anios_pct REAL DEFAULT 0,
    afc_casa_particular_pct REAL DEFAULT 0
);
"""

SQL_CREATE_TRAMO_CARGA_FAMILIAR = """
CREATE TABLE IF NOT EXISTS tramo_carga_familiar (
    tramo INTEGER PRIMARY KEY,
    descripcion TEXT,
    desde REAL DEFAULT 0,
    hasta REAL DEFAULT 0,
    valor REAL DEFAULT 0
);
"""

SQL_CREATE_TRAMO_IMPUESTO_UNICO = """
CREATE TABLE IF NOT EXISTS tramo_impuesto_unico (
    tramo INTEGER PRIMARY KEY,
    desde_utm REAL DEFAULT 0,
    hasta_utm REAL,
    factor REAL DEFAULT 0,
    rebaja_utm REAL DEFAULT 0
);
"""

SQL_CREATE_CONTRATO = """
CREATE TABLE IF NOT EXISTS contrato (
    id_contrato INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_empleado INTEGER NOT NULL,
    nacionalidad TEXT,
    labor_ejecutar TEXT,
    establecimiento TEXT,
    horarios TEXT,
    duracion_contrato TEXT,
    codigo_tipo_contrato TEXT,
    pago TEXT CHECK (pago IN ('Mensual', 'Quincenal', 'Diario')) DEFAULT 'Mensual',
    sueldo_base REAL DEFAULT 0,
    movilizacion REAL DEFAULT 0,
    colacion REAL DEFAULT 0,
    gratificacion REAL DEFAULT 0,
    remuneracion_adicional REAL DEFAULT 0,
    fecha_creacion TEXT,
    FOREIGN KEY (codigo_empleado) REFERENCES trabajador (codigo_empleado),
    FOREIGN KEY (codigo_tipo_contrato) REFERENCES tipo_contrato (codigo)
);
"""

SQL_CREATE_FINIQUITO = """
CREATE TABLE IF NOT EXISTS finiquito (
    id_finiquito INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_empleado INTEGER NOT NULL,
    fecha_inicio TEXT,
    fecha_termino TEXT,
    cargo TEXT,
    codigo_causal TEXT,
    monto_total REAL DEFAULT 0,
    fecha_creacion TEXT,
    FOREIGN KEY (codigo_empleado) REFERENCES trabajador (codigo_empleado),
    FOREIGN KEY (codigo_causal) REFERENCES causal_finiquito (codigo)
);
"""

SQL_CREATE_VACACIONES = """
CREATE TABLE IF NOT EXISTS vacaciones (
    id_vacacion INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_empleado INTEGER NOT NULL,
    fecha_inicio TEXT NOT NULL,
    fecha_termino TEXT NOT NULL,
    dias_habiles INTEGER NOT NULL,
    dias_acumulados_antes REAL DEFAULT 0,
    observaciones TEXT,
    FOREIGN KEY (codigo_empleado) REFERENCES trabajador (codigo_empleado)
);
"""

SQL_CREATE_LIQUIDACION = """
CREATE TABLE IF NOT EXISTS liquidacion (
    id_liquidacion INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_empleado INTEGER NOT NULL,
    codigo_empresa INTEGER NOT NULL,
    anio INTEGER NOT NULL,
    mes INTEGER NOT NULL,
    dias_trabajados INTEGER DEFAULT 30,

    sueldo_base REAL DEFAULT 0,
    total_haberes_imponibles REAL DEFAULT 0,
    total_haberes_no_imponibles REAL DEFAULT 0,
    total_ingreso_bruto REAL DEFAULT 0,

    monto_afp REAL DEFAULT 0,
    monto_salud REAL DEFAULT 0,
    monto_seguro_cesantia REAL DEFAULT 0,
    monto_apv REAL DEFAULT 0,
    total_descuentos_previsionales REAL DEFAULT 0,

    base_tributable REAL DEFAULT 0,
    impuesto_unico REAL DEFAULT 0,

    total_otros_descuentos REAL DEFAULT 0,
    total_descuentos REAL DEFAULT 0,
    sueldo_liquido REAL DEFAULT 0,

    aporte_patronal_afp REAL DEFAULT 0,
    aporte_sis REAL DEFAULT 0,
    aporte_afc_empleador REAL DEFAULT 0,
    aporte_ccaf REAL DEFAULT 0,
    total_aportes_patronales REAL DEFAULT 0,
    costo_total_empresa REAL DEFAULT 0,

    fecha_creacion TEXT,
    UNIQUE (codigo_empleado, anio, mes),
    FOREIGN KEY (codigo_empleado) REFERENCES trabajador (codigo_empleado),
    FOREIGN KEY (codigo_empresa) REFERENCES empresa (codigo_empresa)
);
"""

SQL_CREATE_LIQUIDACION_DETALLE = """
CREATE TABLE IF NOT EXISTS liquidacion_detalle (
    id_detalle INTEGER PRIMARY KEY AUTOINCREMENT,
    id_liquidacion INTEGER NOT NULL,
    codigo_haber_descuento TEXT NOT NULL,
    descripcion TEXT,
    cantidad REAL DEFAULT 1,
    monto REAL DEFAULT 0,
    tipo TEXT CHECK (tipo IN ('Haber', 'Descuento')) NOT NULL,
    FOREIGN KEY (id_liquidacion) REFERENCES liquidacion (id_liquidacion),
    FOREIGN KEY (codigo_haber_descuento) REFERENCES haber_descuento (codigo)
);
"""

SQL_CREATE_ANTICIPO = """
CREATE TABLE IF NOT EXISTS anticipo (
    id_anticipo INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_empleado INTEGER NOT NULL,
    anio INTEGER NOT NULL,
    mes INTEGER NOT NULL,
    fecha_pago TEXT,
    monto REAL NOT NULL DEFAULT 0,
    observaciones TEXT,
    FOREIGN KEY (codigo_empleado) REFERENCES trabajador (codigo_empleado)
);
"""

TABLAS = [
    SQL_CREATE_EMPRESA,
    SQL_CREATE_SUCURSAL,
    SQL_CREATE_CENTRO_COSTO,
    SQL_CREATE_AFP,
    SQL_CREATE_ISAPRE,
    SQL_CREATE_CCAF,
    SQL_CREATE_MUTUAL,
    SQL_CREATE_AHORRO_PREVISIONAL,
    SQL_CREATE_TRABAJADOR,
    SQL_CREATE_CARGA_FAMILIAR,
    SQL_CREATE_HABERES_DESCUENTOS,
    SQL_CREATE_FACTOR_MENSUAL,
    SQL_CREATE_TIPO_CONTRATO,
    SQL_CREATE_CAUSAL_FINIQUITO,
    SQL_CREATE_PARAMETROS,
    SQL_CREATE_TRAMO_CARGA_FAMILIAR,
    SQL_CREATE_TRAMO_IMPUESTO_UNICO,
    SQL_CREATE_CONTRATO,
    SQL_CREATE_FINIQUITO,
    SQL_CREATE_VACACIONES,
    SQL_CREATE_LIQUIDACION,
    SQL_CREATE_LIQUIDACION_DETALLE,
    SQL_CREATE_ANTICIPO,
]
