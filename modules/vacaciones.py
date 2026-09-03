"""
Módulo de Control de Vacaciones.
"""
from datetime import datetime

from database.models import fetch_all, insert, delete
from ui.utils import titulo, pedir_rut, pedir_fecha, pedir_entero, pedir_opcion, imprimir_tabla, pausar
from modules.trabajador import listar_trabajadores, obtener_trabajador


def listar_vacaciones(rut=None):
    if rut:
        return fetch_all("SELECT * FROM vacaciones WHERE trabajador_rut = ? ORDER BY fecha_inicio", (rut,))
    return fetch_all("SELECT * FROM vacaciones ORDER BY fecha_inicio")


def crear_vacaciones(data):
    return insert("vacaciones", data)


def dias_disponibles(rut, dias_legales_por_anio=15):
    """Calcula referencialmente los días de vacaciones disponibles según antigüedad
    (15 días hábiles legales por año trabajado) menos los días ya utilizados."""
    trabajador = obtener_trabajador(rut)
    if not trabajador:
        return 0
    from modules.trabajador import obtener_datos_laborales
    datos_laborales = obtener_datos_laborales(rut)
    if not datos_laborales or not datos_laborales.get("fecha_contrato"):
        return 0
    fecha_contrato = datetime.strptime(datos_laborales["fecha_contrato"], "%d-%m-%Y")
    anios_trabajados = (datetime.today() - fecha_contrato).days / 365.25
    dias_devengados = round(anios_trabajados * dias_legales_por_anio)
    usados = sum(v["dias_habiles"] for v in listar_vacaciones(rut))
    return max(0, dias_devengados - usados)


def menu_registrar_vacaciones():
    titulo("Registrar Vacaciones")
    imprimir_tabla(listar_trabajadores())
    rut = pedir_rut("RUT del trabajador")
    if not obtener_trabajador(rut):
        print("Trabajador no encontrado.")
        pausar()
        return

    print(f"Días de vacaciones disponibles (referencial): {dias_disponibles(rut)}")
    data = {
        "trabajador_rut": rut,
        "fecha_inicio": pedir_fecha("Fecha de Inicio"),
        "fecha_termino": pedir_fecha("Fecha de Término"),
        "dias_habiles": pedir_entero("Días Hábiles"),
        "tipo": pedir_opcion("Tipo", ["Legal", "Progresivo", "Anticipado"]),
    }
    crear_vacaciones(data)
    print("Vacaciones registradas.")
    pausar()


def menu_listar_vacaciones():
    titulo("Control de Vacaciones")
    imprimir_tabla(listar_trabajadores())
    rut = pedir_rut("RUT del trabajador (o Enter para ver todas)", obligatorio=False)
    if rut:
        imprimir_tabla(listar_vacaciones(rut))
    else:
        imprimir_tabla(listar_vacaciones())
    pausar()


def menu_eliminar_vacaciones():
    titulo("Eliminar Registro de Vacaciones")
    imprimir_tabla(listar_vacaciones())
    id_vacacion = pedir_entero("ID a eliminar")
    delete("vacaciones", "id = ?", (id_vacacion,))
    print("Registro eliminado.")
    pausar()
