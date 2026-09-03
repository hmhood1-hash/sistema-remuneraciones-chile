"""
Módulo de gestión de Trabajadores: datos personales, datos laborales,
datos previsionales y cargas familiares.
"""
from database.models import fetch_all, fetch_one, insert, update, delete
from ui.utils import (
    titulo, pedir_texto, pedir_rut, pedir_fecha, pedir_monto, pedir_entero, pedir_opcion,
    imprimir_tabla, pausar,
)
from modules.empresa import listar_empresas, listar_sucursales, listar_centros_costo


# ---------- Datos personales ----------

def listar_trabajadores(empresa_codigo=None):
    if empresa_codigo:
        return fetch_all(
            "SELECT * FROM trabajador WHERE empresa_codigo = ? ORDER BY nombre", (empresa_codigo,)
        )
    return fetch_all("SELECT * FROM trabajador ORDER BY nombre")


def obtener_trabajador(rut):
    return fetch_one("SELECT * FROM trabajador WHERE rut = ?", (rut,))


def crear_trabajador(data):
    insert("trabajador", data)
    return data["rut"]


def actualizar_trabajador(rut, data):
    return update("trabajador", data, "rut = ?", (rut,))


def eliminar_trabajador(rut):
    return delete("trabajador", "rut = ?", (rut,))


def _pedir_datos_personales(rut=None):
    data = {}
    data["rut"] = rut or pedir_rut("RUT Trabajador")
    data["nombre"] = pedir_texto("Nombre")
    data["ap_paterno"] = pedir_texto("Apellido Paterno")
    data["ap_materno"] = pedir_texto("Apellido Materno", obligatorio=False)
    data["fecha_nacimiento"] = pedir_fecha("Fecha de Nacimiento")
    data["codigo_empleado"] = pedir_texto("Código Empleado", obligatorio=False)
    data["calle"] = pedir_texto("Calle", obligatorio=False)
    data["numero"] = pedir_texto("Número", obligatorio=False)
    data["dpto"] = pedir_texto("Dpto", obligatorio=False)
    data["comuna"] = pedir_texto("Comuna", obligatorio=False)
    data["correo"] = pedir_texto("Correo electrónico", obligatorio=False)
    data["fono"] = pedir_texto("Fono", obligatorio=False)
    data["sexo"] = pedir_opcion("Sexo", ["M", "F", "O"])
    data["estado_civil"] = pedir_opcion("Estado Civil", ["Soltero", "Casado", "Viudo", "Separado"])
    imprimir_tabla(listar_empresas())
    data["empresa_codigo"] = pedir_entero("Código de empresa")
    return data


def menu_crear_trabajador():
    titulo("Nuevo Trabajador")
    data = _pedir_datos_personales()
    crear_trabajador(data)
    print(f"Trabajador creado: {data['rut']}")
    pausar()


def menu_listar_trabajadores():
    titulo("Listado de Trabajadores")
    imprimir_tabla(listar_trabajadores())
    pausar()


def menu_editar_trabajador():
    titulo("Editar Trabajador")
    imprimir_tabla(listar_trabajadores())
    rut = pedir_rut("RUT del trabajador a editar")
    trabajador = obtener_trabajador(rut)
    if not trabajador:
        print("Trabajador no encontrado.")
        pausar()
        return
    data = _pedir_datos_personales(rut=rut)
    actualizar_trabajador(rut, data)
    print("Trabajador actualizado.")
    pausar()


def menu_eliminar_trabajador():
    titulo("Eliminar Trabajador")
    imprimir_tabla(listar_trabajadores())
    rut = pedir_rut("RUT del trabajador a eliminar")
    eliminar_trabajador(rut)
    print("Trabajador eliminado.")
    pausar()


# ---------- Datos laborales ----------

def obtener_datos_laborales(rut):
    return fetch_one("SELECT * FROM datos_laborales WHERE trabajador_rut = ?", (rut,))


def guardar_datos_laborales(rut, data):
    existente = obtener_datos_laborales(rut)
    if existente:
        return update("datos_laborales", data, "trabajador_rut = ?", (rut,))
    data["trabajador_rut"] = rut
    return insert("datos_laborales", data)


def menu_datos_laborales():
    titulo("Datos Laborales del Trabajador")
    imprimir_tabla(listar_trabajadores())
    rut = pedir_rut("RUT del trabajador")
    if not obtener_trabajador(rut):
        print("Trabajador no encontrado.")
        pausar()
        return

    sueldo_tipo = pedir_opcion("Sueldo Tipo", ["Mensual", "Diario", "Part Time", "Empresarial"])
    sueldo_base = pedir_monto("Sueldo Base")
    gratificacion_tipo = pedir_opcion("Gratificación", ["Mensual", "Anual", "Ninguna"])
    horas_semanales = pedir_monto("Horas Semanales")
    dias_laborales_semana = pedir_entero("Días laborales a la semana")
    fecha_contrato = pedir_fecha("Fecha de Contrato")
    cargo = pedir_texto("Cargo")
    horario = pedir_texto("Horarios", obligatorio=False)

    print("Sucursales disponibles:")
    imprimir_tabla(listar_sucursales())
    sucursal_codigo = pedir_entero("Código de sucursal", default=None)

    print("Centros de costo disponibles:")
    imprimir_tabla(listar_centros_costo())
    centro_costo_codigo = pedir_entero("Código de centro de costo", default=None)

    aplica_sis = pedir_opcion("Aplica SIS", ["S", "N"])

    data = {
        "sueldo_tipo": sueldo_tipo,
        "sueldo_base": sueldo_base,
        "gratificacion_tipo": gratificacion_tipo,
        "horas_semanales": horas_semanales,
        "dias_laborales_semana": dias_laborales_semana,
        "fecha_contrato": fecha_contrato,
        "cargo": cargo,
        "horario": horario,
        "sucursal_codigo": sucursal_codigo,
        "centro_costo_codigo": centro_costo_codigo,
        "aplica_sis": aplica_sis,
    }
    guardar_datos_laborales(rut, data)
    print("Datos laborales guardados.")
    pausar()


# ---------- Datos previsionales ----------

def obtener_datos_previsionales(rut):
    return fetch_one("SELECT * FROM datos_previsionales WHERE trabajador_rut = ?", (rut,))


def guardar_datos_previsionales(rut, data):
    existente = obtener_datos_previsionales(rut)
    if existente:
        return update("datos_previsionales", data, "trabajador_rut = ?", (rut,))
    data["trabajador_rut"] = rut
    return insert("datos_previsionales", data)


def menu_datos_previsionales():
    titulo("Datos Previsionales del Trabajador")
    imprimir_tabla(listar_trabajadores())
    rut = pedir_rut("RUT del trabajador")
    if not obtener_trabajador(rut):
        print("Trabajador no encontrado.")
        pausar()
        return

    print("AFP disponibles:")
    imprimir_tabla(fetch_all("SELECT * FROM afp"))
    afp_codigo = pedir_texto("Código AFP")

    print("Isapres disponibles:")
    imprimir_tabla(fetch_all("SELECT * FROM isapre"))
    isapre_codigo = pedir_texto("Código Isapre/Salud")

    modalidad_salud = pedir_opcion("Modalidad Salud", ["Pesos", "UF", "7%", "7%+UF", "7%+UF+Pesos"])
    cotizacion_pactada = pedir_monto("Cotización Pactada (% o monto según modalidad)")
    tope_salud = pedir_opcion("Tope Salud", ["UF Actual", "UF Anterior"])
    seguro_cesantia_tipo = pedir_opcion("Seguro de Cesantía", ["Plazo Fijo", "Indefinido"])
    fecha_inicio_afc = pedir_fecha("Fecha inicio AFC", obligatorio=False)
    fecha_termino_afc = pedir_fecha("Fecha término AFC", obligatorio=False)
    afp_cotiza_afc = pedir_opcion("¿AFP cotiza AFC?", ["S", "N"])
    tipo_trabajador = pedir_opcion(
        "Tipo Trabajador",
        ["Activo No Pensionado", "Pensionado y Cotiza", "Pensionado No Cotiza", "Activo Mayor 60/65"],
    )

    data = {
        "afp_codigo": afp_codigo,
        "isapre_codigo": isapre_codigo,
        "modalidad_salud": modalidad_salud,
        "cotizacion_pactada": cotizacion_pactada,
        "tope_salud": tope_salud,
        "seguro_cesantia_tipo": seguro_cesantia_tipo,
        "fecha_inicio_afc": fecha_inicio_afc,
        "fecha_termino_afc": fecha_termino_afc,
        "afp_cotiza_afc": afp_cotiza_afc,
        "tipo_trabajador": tipo_trabajador,
    }
    guardar_datos_previsionales(rut, data)
    print("Datos previsionales guardados.")
    pausar()


# ---------- Cargas familiares ----------

def listar_cargas_familiares(rut):
    return fetch_all("SELECT * FROM carga_familiar WHERE trabajador_rut = ?", (rut,))


def crear_carga_familiar(data):
    return insert("carga_familiar", data)


def eliminar_carga_familiar(id_carga):
    return delete("carga_familiar", "id = ?", (id_carga,))


def menu_cargas_familiares():
    titulo("Cargas Familiares")
    imprimir_tabla(listar_trabajadores())
    rut = pedir_rut("RUT del trabajador")
    if not obtener_trabajador(rut):
        print("Trabajador no encontrado.")
        pausar()
        return

    print("Cargas familiares actuales:")
    imprimir_tabla(listar_cargas_familiares(rut))

    opcion = pedir_opcion("Desea (1) Agregar carga (2) Eliminar carga (0) Volver", ["0", "1", "2"])
    if opcion == "1":
        data = {
            "trabajador_rut": rut,
            "rut_carga": pedir_rut("RUT de la carga"),
            "nombre": pedir_texto("Nombre"),
            "fecha_inicio": pedir_fecha("Fecha inicio"),
            "fecha_vencimiento": pedir_fecha("Fecha vencimiento", obligatorio=False),
            "tipo": pedir_opcion("Tipo", ["Simple", "Materna", "Invalidez"]),
            "parentesco": pedir_opcion("Parentesco", ["Hijo", "Conyuge", "Progenitor", "Hermano"]),
        }
        crear_carga_familiar(data)
        print("Carga familiar agregada.")
    elif opcion == "2":
        id_carga = pedir_entero("ID de la carga a eliminar")
        eliminar_carga_familiar(id_carga)
        print("Carga familiar eliminada.")
    pausar()
