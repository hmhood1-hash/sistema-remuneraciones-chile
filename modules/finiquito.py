"""
Módulo de gestión de Finiquitos.
"""
from database.models import fetch_all, insert, delete
from ui.utils import titulo, pedir_texto, pedir_rut, pedir_fecha, pedir_entero, imprimir_tabla, pausar
from modules.trabajador import listar_trabajadores, obtener_trabajador
from modules.contrato import listar_causales_finiquito


def listar_finiquitos():
    return fetch_all("SELECT * FROM finiquito ORDER BY id")


def crear_finiquito(data):
    return insert("finiquito", data)


def menu_crear_finiquito():
    titulo("Nuevo Finiquito")
    imprimir_tabla(listar_trabajadores())
    rut = pedir_rut("RUT del trabajador")
    trabajador = obtener_trabajador(rut)
    if not trabajador:
        print("Trabajador no encontrado.")
        pausar()
        return

    imprimir_tabla(listar_causales_finiquito())
    data = {
        "trabajador_rut": rut,
        "nombre": pedir_texto("Nombre", default=f"{trabajador['nombre']} {trabajador['ap_paterno']}"),
        "fecha_inicio": pedir_fecha("Fecha de Inicio"),
        "fecha_termino": pedir_fecha("Fecha de Término"),
        "cargo": pedir_texto("Cargo", obligatorio=False),
        "causal_codigo": pedir_texto("Código Causal de Despido"),
    }
    codigo = crear_finiquito(data)
    print(f"Finiquito registrado con ID: {codigo}")
    pausar()


def menu_listar_finiquitos():
    titulo("Listado de Finiquitos")
    imprimir_tabla(listar_finiquitos())
    pausar()


def menu_eliminar_finiquito():
    titulo("Eliminar Finiquito")
    imprimir_tabla(listar_finiquitos())
    id_finiquito = pedir_entero("ID del finiquito a eliminar")
    delete("finiquito", "id = ?", (id_finiquito,))
    print("Finiquito eliminado.")
    pausar()
