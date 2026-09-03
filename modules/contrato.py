"""
Módulo de gestión de Tipos de Contrato, Contratos individuales y Causales de Finiquito.
"""
from database.models import fetch_all, insert, delete
from ui.utils import (
    titulo, pedir_texto, pedir_rut, pedir_monto, pedir_fecha, pedir_opcion, pedir_entero,
    imprimir_tabla, pausar,
)
from modules.trabajador import listar_trabajadores, obtener_trabajador


# ---------- Tipos de Contrato ----------

def listar_tipos_contrato():
    return fetch_all("SELECT * FROM tipo_contrato ORDER BY codigo")


def menu_crear_tipo_contrato():
    titulo("Nuevo Tipo de Contrato")
    data = {"codigo": pedir_texto("Código"), "descripcion": pedir_texto("Descripción")}
    insert("tipo_contrato", data)
    print("Tipo de contrato creado.")
    pausar()


def menu_listar_tipos_contrato():
    titulo("Tipos de Contrato")
    imprimir_tabla(listar_tipos_contrato())
    pausar()


def menu_eliminar_tipo_contrato():
    titulo("Eliminar Tipo de Contrato")
    imprimir_tabla(listar_tipos_contrato())
    codigo = pedir_texto("Código a eliminar")
    delete("tipo_contrato", "codigo = ?", (codigo,))
    print("Tipo de contrato eliminado.")
    pausar()


# ---------- Contratos ----------

def listar_contratos(rut=None):
    if rut:
        return fetch_all("SELECT * FROM contrato WHERE trabajador_rut = ? ORDER BY id", (rut,))
    return fetch_all("SELECT * FROM contrato ORDER BY id")


def crear_contrato(data):
    return insert("contrato", data)


def menu_crear_contrato():
    titulo("Nuevo Contrato de Trabajo")
    imprimir_tabla(listar_trabajadores())
    rut = pedir_rut("RUT del trabajador")
    if not obtener_trabajador(rut):
        print("Trabajador no encontrado.")
        pausar()
        return

    imprimir_tabla(listar_tipos_contrato())
    data = {
        "trabajador_rut": rut,
        "nombre": pedir_texto("Nombre"),
        "nacionalidad": pedir_texto("Nacionalidad"),
        "labor_ejecutar": pedir_texto("Labor a Ejecutar"),
        "establecimiento": pedir_texto("Establecimiento", obligatorio=False),
        "horario": pedir_texto("Horarios", obligatorio=False),
        "duracion_contrato": pedir_texto("Duración del Contrato"),
        "tipo_contrato_codigo": pedir_texto("Código Tipo de Contrato"),
        "forma_pago": pedir_opcion("Forma de Pago", ["Mensual", "Quincenal", "Diario"]),
        "sueldo_base": pedir_monto("Sueldo Base"),
        "movilizacion": pedir_monto("Movilización", default=0),
        "colacion": pedir_monto("Colación", default=0),
        "gratificacion": pedir_monto("Gratificación", default=0),
        "remuneracion_adicional": pedir_monto("Remuneración Adicional", default=0),
        "fecha_inicio": pedir_fecha("Fecha de Inicio"),
    }
    codigo = crear_contrato(data)
    print(f"Contrato creado con ID: {codigo}")
    pausar()


def menu_listar_contratos():
    titulo("Listado de Contratos")
    imprimir_tabla(listar_contratos())
    pausar()


def menu_eliminar_contrato():
    titulo("Eliminar Contrato")
    imprimir_tabla(listar_contratos())
    id_contrato = pedir_entero("ID del contrato a eliminar")
    delete("contrato", "id = ?", (id_contrato,))
    print("Contrato eliminado.")
    pausar()


# ---------- Causales de Finiquito ----------

def listar_causales_finiquito():
    return fetch_all("SELECT * FROM causal_finiquito ORDER BY codigo")


def menu_crear_causal_finiquito():
    titulo("Nueva Causal de Finiquito")
    data = {"codigo": pedir_texto("Código"), "descripcion": pedir_texto("Descripción")}
    insert("causal_finiquito", data)
    print("Causal de finiquito creada.")
    pausar()


def menu_listar_causales_finiquito():
    titulo("Causales de Finiquito")
    imprimir_tabla(listar_causales_finiquito())
    pausar()


def menu_eliminar_causal_finiquito():
    titulo("Eliminar Causal de Finiquito")
    imprimir_tabla(listar_causales_finiquito())
    codigo = pedir_texto("Código a eliminar")
    delete("causal_finiquito", "codigo = ?", (codigo,))
    print("Causal de finiquito eliminada.")
    pausar()
