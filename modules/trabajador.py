# -*- coding: utf-8 -*-
"""CRUD de Trabajadores y Cargas Familiares."""
from database.conexion import conexion_bd

CAMPOS_TRABAJADOR = (
    "codigo_empresa", "rut", "nombres", "apellido_paterno", "apellido_materno",
    "fecha_nacimiento", "sexo", "estado_civil", "calle", "numero", "dpto",
    "comuna", "correo", "fono",
    "sueldo_tipo", "sueldo_base", "gratificacion_tipo", "horas_semanales",
    "dias_laborales_semana", "fecha_contrato", "cargo", "horarios",
    "codigo_sucursal", "codigo_centro_costo", "aplica_sis",
    "codigo_afp", "codigo_isapre", "modalidad_salud", "cotizacion_pactada",
    "tope_salud", "seguro_cesantia", "fecha_inicio_afc", "fecha_termino_afc",
    "afp_cotiza_afc", "tipo_trabajador",
)


def crear_trabajador(datos, ruta_bd=None):
    """Crea un trabajador nuevo. El código de empleado se asigna automáticamente."""
    valores = tuple(datos.get(campo) for campo in CAMPOS_TRABAJADOR)
    with conexion_bd(ruta_bd) as conexion:
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO trabajador ({}) VALUES ({})".format(
                ", ".join(CAMPOS_TRABAJADOR), ", ".join(["?"] * len(CAMPOS_TRABAJADOR))
            ),
            valores,
        )
        return cursor.lastrowid


def actualizar_trabajador(codigo_empleado, datos, ruta_bd=None):
    campos = [campo for campo in datos.keys() if campo in CAMPOS_TRABAJADOR]
    valores = [datos[campo] for campo in campos]
    valores.append(codigo_empleado)
    with conexion_bd(ruta_bd) as conexion:
        conexion.execute(
            "UPDATE trabajador SET {} WHERE codigo_empleado = ?".format(
                ", ".join("{} = ?".format(campo) for campo in campos)
            ),
            valores,
        )


def eliminar_trabajador(codigo_empleado, ruta_bd=None):
    """Elimina lógicamente (inactiva) a un trabajador, preservando su historial."""
    with conexion_bd(ruta_bd) as conexion:
        conexion.execute(
            "UPDATE trabajador SET activo = 0 WHERE codigo_empleado = ?", (codigo_empleado,)
        )


def listar_trabajadores(codigo_empresa=None, solo_activos=True, ruta_bd=None):
    with conexion_bd(ruta_bd) as conexion:
        condiciones = []
        parametros = []
        if codigo_empresa:
            condiciones.append("codigo_empresa = ?")
            parametros.append(codigo_empresa)
        if solo_activos:
            condiciones.append("activo = 1")
        where = " WHERE " + " AND ".join(condiciones) if condiciones else ""
        cursor = conexion.execute(
            "SELECT * FROM trabajador{} ORDER BY apellido_paterno, nombres".format(where),
            parametros,
        )
        return [dict(fila) for fila in cursor.fetchall()]


def obtener_trabajador(codigo_empleado, ruta_bd=None):
    with conexion_bd(ruta_bd) as conexion:
        cursor = conexion.execute(
            "SELECT * FROM trabajador WHERE codigo_empleado = ?", (codigo_empleado,)
        )
        fila = cursor.fetchone()
        return dict(fila) if fila else None


def buscar_trabajadores(texto, ruta_bd=None):
    """Búsqueda por RUT, nombres o apellidos (usada en filtros de la interfaz)."""
    patron = "%{}%".format(texto or "")
    with conexion_bd(ruta_bd) as conexion:
        cursor = conexion.execute(
            "SELECT * FROM trabajador WHERE activo = 1 AND ("
            "rut LIKE ? OR nombres LIKE ? OR apellido_paterno LIKE ? OR apellido_materno LIKE ?"
            ") ORDER BY apellido_paterno, nombres",
            (patron, patron, patron, patron),
        )
        return [dict(fila) for fila in cursor.fetchall()]


# ---------------------------------------------------------------------------
# Cargas Familiares
# ---------------------------------------------------------------------------
def crear_carga_familiar(datos, ruta_bd=None):
    campos = (
        "codigo_empleado", "rut_carga", "nombre", "fecha_inicio",
        "fecha_vencimiento", "tipo", "parentesco",
    )
    valores = tuple(datos.get(campo) for campo in campos)
    with conexion_bd(ruta_bd) as conexion:
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO carga_familiar ({}) VALUES ({})".format(
                ", ".join(campos), ", ".join(["?"] * len(campos))
            ),
            valores,
        )
        return cursor.lastrowid


def actualizar_carga_familiar(id_carga, datos, ruta_bd=None):
    campos = list(datos.keys())
    valores = list(datos.values())
    valores.append(id_carga)
    with conexion_bd(ruta_bd) as conexion:
        conexion.execute(
            "UPDATE carga_familiar SET {} WHERE id_carga = ?".format(
                ", ".join("{} = ?".format(campo) for campo in campos)
            ),
            valores,
        )


def eliminar_carga_familiar(id_carga, ruta_bd=None):
    with conexion_bd(ruta_bd) as conexion:
        conexion.execute("DELETE FROM carga_familiar WHERE id_carga = ?", (id_carga,))


def listar_cargas_familiares(codigo_empleado, ruta_bd=None):
    with conexion_bd(ruta_bd) as conexion:
        cursor = conexion.execute(
            "SELECT * FROM carga_familiar WHERE codigo_empleado = ? ORDER BY nombre",
            (codigo_empleado,),
        )
        return [dict(fila) for fila in cursor.fetchall()]


def contar_cargas_familiares_vigentes(codigo_empleado, fecha_referencia, ruta_bd=None):
    """Cuenta las cargas familiares vigentes a una fecha determinada (YYYY-MM-DD)."""
    with conexion_bd(ruta_bd) as conexion:
        cursor = conexion.execute(
            "SELECT COUNT(*) AS n FROM carga_familiar WHERE codigo_empleado = ? "
            "AND (fecha_vencimiento IS NULL OR fecha_vencimiento >= ?) "
            "AND (fecha_inicio IS NULL OR fecha_inicio <= ?)",
            (codigo_empleado, fecha_referencia, fecha_referencia),
        )
        return cursor.fetchone()[0]
