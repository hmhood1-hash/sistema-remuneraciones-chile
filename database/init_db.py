"""
Inicialización de la base de datos SQLite para Sistema de Remuneraciones Chile.
Crea todas las tablas necesarias con esquema relacional completo.
"""
import sqlite3
import os
from datetime import datetime


DB_PATH = "data/remuneraciones.db"


def init_database():
    """Inicializa la base de datos SQLite."""
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Tabla: Empresa
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS empresa (
            codigo INTEGER PRIMARY KEY AUTOINCREMENT,
            rut TEXT UNIQUE NOT NULL,
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
            rep_legal_ap_materno TEXT,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Tabla: Sucursal
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sucursal (
            codigo INTEGER PRIMARY KEY AUTOINCREMENT,
            empresa_codigo INTEGER NOT NULL,
            nombre TEXT NOT NULL,
            direccion TEXT,
            region TEXT,
            ciudad TEXT,
            comuna TEXT,
            fono TEXT,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (empresa_codigo) REFERENCES empresa(codigo)
        )
    """)

    # Tabla: Centro de Costo
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS centro_costo (
            codigo INTEGER PRIMARY KEY AUTOINCREMENT,
            empresa_codigo INTEGER NOT NULL,
            descripcion TEXT NOT NULL,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (empresa_codigo) REFERENCES empresa(codigo)
        )
    """)

    # Tabla: Trabajador
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS trabajador (
            rut TEXT PRIMARY KEY,
            empresa_codigo INTEGER NOT NULL,
            codigo_empleado INTEGER UNIQUE,
            nombre TEXT NOT NULL,
            ap_paterno TEXT,
            ap_materno TEXT,
            fecha_nacimiento TEXT,
            sexo TEXT,
            estado_civil TEXT,
            calle TEXT,
            numero TEXT,
            depto TEXT,
            comuna TEXT,
            correo TEXT,
            fono TEXT,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (empresa_codigo) REFERENCES empresa(codigo)
        )
    """)

    # Tabla: Datos Laborales
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS datos_laborales (
            trabajador_rut TEXT PRIMARY KEY,
            sueldo_tipo TEXT,
            sueldo_base REAL,
            gratificacion_tipo TEXT,
            gratificacion_monto REAL,
            horas_semanales INTEGER,
            dias_laborales_semana INTEGER,
            fecha_contrato TEXT,
            cargo TEXT,
            horarios TEXT,
            sucursal_codigo INTEGER,
            centro_costo_codigo INTEGER,
            aplica_sis TEXT,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (trabajador_rut) REFERENCES trabajador(rut),
            FOREIGN KEY (sucursal_codigo) REFERENCES sucursal(codigo),
            FOREIGN KEY (centro_costo_codigo) REFERENCES centro_costo(codigo)
        )
    """)

    # Tabla: Datos Previsionales
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS datos_previsionales (
            trabajador_rut TEXT PRIMARY KEY,
            afp_codigo TEXT,
            isapre_codigo TEXT,
            modalidad_salud TEXT,
            cotizacion_pactada REAL,
            tope_salud TEXT,
            seguro_cesantia_tipo TEXT,
            fecha_inicio_afc TEXT,
            fecha_termino_afc TEXT,
            afp_cotiza_afc TEXT,
            tipo_trabajador TEXT,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (trabajador_rut) REFERENCES trabajador(rut)
        )
    """)

    # Tabla: Cargas Familiares
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS carga_familiar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trabajador_rut TEXT NOT NULL,
            rut_carga TEXT,
            nombre TEXT,
            fecha_inicio TEXT,
            fecha_vencimiento TEXT,
            tipo TEXT,
            parentesco TEXT,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (trabajador_rut) REFERENCES trabajador(rut)
        )
    """)

    # Tabla: AFP
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS afp (
            codigo TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            factor_cotizacion REAL,
            sistema_previsional TEXT,
            comision_afiliacion REAL,
            seguro_invalidez REAL,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Tabla: Isapre
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS isapre (
            codigo TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Tabla: CCAF
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ccaf (
            codigo TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Tabla: Mutual
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mutual (
            codigo TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Tabla: Ahorro Previsional (APV)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ahorro_previsional (
            codigo TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Tabla: Haberes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS haber (
            codigo INTEGER PRIMARY KEY AUTOINCREMENT,
            empresa_codigo INTEGER,
            nombre TEXT NOT NULL,
            clasificacion TEXT,
            tipo TEXT,
            monto_pesos REAL,
            porcentaje REAL,
            base_calculo TEXT,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (empresa_codigo) REFERENCES empresa(codigo)
        )
    """)

    # Tabla: Descuentos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS descuento (
            codigo INTEGER PRIMARY KEY AUTOINCREMENT,
            empresa_codigo INTEGER,
            nombre TEXT NOT NULL,
            tipo TEXT,
            monto_pesos REAL,
            porcentaje REAL,
            base_calculo TEXT,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (empresa_codigo) REFERENCES empresa(codigo)
        )
    """)

    # Tabla: Parámetros
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS parametro (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            anio INTEGER,
            mes INTEGER,
            sueldo_minimo REAL,
            sueldo_minimo_menor_18 REAL,
            sueldo_minimo_mayor_65 REAL,
            tope_gratificacion_mensual REAL,
            tope_imponible_afp_uf REAL,
            tope_imponible_reg_antiguo_uf REAL,
            tope_afc_uf REAL,
            tope_apv_mensual_uf REAL,
            tope_apv_anual_uf REAL,
            utm REAL,
            uf REAL,
            factor_actualizacion REAL,
            aporte_patronal_porcentaje REAL,
            aporte_adicional_porcentaje REAL,
            factor_sss_porcentaje REAL,
            factor_empart_porcentaje REAL,
            ccaf_porcentaje REAL,
            salud_porcentaje REAL,
            afp_empleador_porcentaje REAL,
            sis_empleador_porcentaje REAL,
            afc_trabajador_indefinido_porcentaje REAL,
            afc_empleador_indefinido_porcentaje REAL,
            afc_empleador_plazo_fijo_porcentaje REAL,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(anio, mes)
        )
    """)

    # Tabla: Tramos de Cargas Familiares
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tramo_carga_familiar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            empresa_codigo INTEGER,
            numero_tramo INTEGER,
            sueldo_desde REAL,
            sueldo_hasta REAL,
            valor_carga REAL,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (empresa_codigo) REFERENCES empresa(codigo)
        )
    """)

    # Tabla: Impuesto Único (tabla progresiva)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS impuesto_unico (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            anio INTEGER,
            sueldo_desde REAL,
            sueldo_hasta REAL,
            factor REAL,
            rebaja REAL,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(anio, sueldo_desde)
        )
    """)

    # Tabla: Tipos de Contrato
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tipo_contrato (
            codigo TEXT PRIMARY KEY,
            descripcion TEXT NOT NULL,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Tabla: Causales de Finiquito
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS causal_finiquito (
            codigo TEXT PRIMARY KEY,
            descripcion TEXT NOT NULL,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Tabla: Contrato
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contrato (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trabajador_rut TEXT NOT NULL,
            nacionalidad TEXT,
            labor_ejecutar TEXT,
            establecimiento TEXT,
            horarios TEXT,
            duracion_contrato TEXT,
            tipo_contrato_codigo TEXT,
            frecuencia_pago TEXT,
            sueldo_base REAL,
            movilizacion REAL,
            colacion REAL,
            gratificacion REAL,
            remuneracion_adicional REAL,
            fecha_inicio TEXT,
            fecha_termino TEXT,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (trabajador_rut) REFERENCES trabajador(rut),
            FOREIGN KEY (tipo_contrato_codigo) REFERENCES tipo_contrato(codigo)
        )
    """)

    # Tabla: Finiquito
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS finiquito (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trabajador_rut TEXT NOT NULL,
            fecha_inicio TEXT,
            fecha_termino TEXT,
            cargo TEXT,
            causal_finiquito_codigo TEXT,
            sueldo_proporcional REAL,
            gratificacion_proporcional REAL,
            vacaciones_proporcional REAL,
            indemnizacion REAL,
            otras_prestaciones REAL,
            total_haber REAL,
            descuentos REAL,
            liquido_finiquito REAL,
            fecha_calculo TIMESTAMP,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (trabajador_rut) REFERENCES trabajador(rut),
            FOREIGN KEY (causal_finiquito_codigo) REFERENCES causal_finiquito(codigo)
        )
    """)

    # Tabla: Vacaciones
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vacacion (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trabajador_rut TEXT NOT NULL,
            anio_laboral INTEGER,
            dias_acumulados INTEGER,
            dias_tomados INTEGER,
            dias_disponibles INTEGER,
            fecha_inicio_vacacion TEXT,
            fecha_termino_vacacion TEXT,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (trabajador_rut) REFERENCES trabajador(rut)
        )
    """)

    # Tabla: Liquidación de Sueldo
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS liquidacion (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trabajador_rut TEXT NOT NULL,
            empresa_codigo INTEGER NOT NULL,
            anio INTEGER,
            mes INTEGER,
            sueldo_base REAL,
            gratificacion REAL,
            total_haberes_imponibles REAL,
            total_haberes_no_imponibles REAL,
            total_haberes REAL,
            monto_afp REAL,
            monto_salud REAL,
            monto_afc REAL,
            monto_apv REAL,
            base_tributable REAL,
            impuesto_unico REAL,
            otros_descuentos REAL,
            total_descuentos REAL,
            sueldo_liquido REAL,
            aporte_patronal_sis REAL,
            aporte_patronal_afc REAL,
            aporte_patronal_ccaf REAL,
            aporte_patronal_mutual REAL,
            fecha_calculo TIMESTAMP,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (trabajador_rut) REFERENCES trabajador(rut),
            FOREIGN KEY (empresa_codigo) REFERENCES empresa(codigo),
            UNIQUE(trabajador_rut, anio, mes)
        )
    """)

    # Insertar datos base (AFP, Isapres, etc.)
    _insertar_datos_base(cursor)

    conn.commit()
    return conn


def _insertar_datos_base(cursor):
    """Inserta datos base (AFP, Isapres, etc.) si no existen."""
    # AFP
    afps = [
        ('EMPART', 'Empart', 10.0, 'Nuevo', 0.57, 1.53),
        ('SSS', 'Sistema de Seguridad Social', 10.0, 'Nuevo', 0.77, 1.60),
        ('CAPITAL', 'Capital', 10.0, 'Nuevo', 0.77, 1.63),
        ('CUPRUM', 'Cuprum', 10.0, 'Nuevo', 0.77, 1.46),
        ('HABITAT', 'Hábitat', 10.0, 'Nuevo', 0.57, 1.42),
        ('MODELO', 'Modelo', 10.0, 'Nuevo', 0.57, 1.59),
        ('PLANVITAL', 'PlanVital', 10.0, 'Nuevo', 0.60, 1.47),
        ('PROVIDA', 'Provida', 10.0, 'Nuevo', 0.57, 1.65),
        ('UNO', 'Uno', 10.0, 'Nuevo', 0.77, 1.50),
    ]
    for codigo, nombre, factor, sistema, comision, seguro in afps:
        cursor.execute(
            "INSERT OR IGNORE INTO afp (codigo, nombre, factor_cotizacion, sistema_previsional, comision_afiliacion, seguro_invalidez) VALUES (?, ?, ?, ?, ?, ?)",
            (codigo, nombre, factor, sistema, comision, seguro)
        )

    # Isapres
    isapres = [
        ('FONASA', 'Fonasa'),
        ('VIDATRES', 'Vida Tres'),
        ('CONSALUD', 'Consalud'),
        ('BANMEDICA', 'Banmédica'),
        ('MASVIDA', 'Más Vida'),
        ('CRUZBLANCA', 'Cruz Blanca'),
    ]
    for codigo, nombre in isapres:
        cursor.execute(
            "INSERT OR IGNORE INTO isapre (codigo, nombre) VALUES (?, ?)",
            (codigo, nombre)
        )

    # Tipos de Contrato
    tipos_contrato = [
        ('INDEFINIDO', 'Contrato Indefinido'),
        ('PLAZO_FIJO', 'Contrato Plazo Fijo'),
        ('APRENDIZ', 'Contrato Aprendiz'),
        ('PRACTICA', 'Contrato de Práctica'),
    ]
    for codigo, descripcion in tipos_contrato:
        cursor.execute(
            "INSERT OR IGNORE INTO tipo_contrato (codigo, descripcion) VALUES (?, ?)",
            (codigo, descripcion)
        )

    # Causales de Finiquito
    causales = [
        ('RENUNCIA', 'Renuncia Voluntaria'),
        ('DESPIDO', 'Despido'),
        ('VENCIMIENTO', 'Vencimiento de Contrato'),
        ('INVALIDEZ', 'Invalidez'),
        ('JUBILACION', 'Jubilación'),
        ('FALLECIMIENTO', 'Fallecimiento'),
    ]
    for codigo, descripcion in causales:
        cursor.execute(
            "INSERT OR IGNORE INTO causal_finiquito (codigo, descripcion) VALUES (?, ?)",
            (codigo, descripcion)
        )
