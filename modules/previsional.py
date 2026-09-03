"""
Módulo de gestión de Instituciones Previsionales: AFP, Isapres, CCAF, Mutuales
y Ahorro Previsional Voluntario (APV).
"""
from database.models import fetch_all, fetch_one, insert, update, delete
from ui.utils import titulo, pedir_texto, pedir_monto, pedir_opcion, imprimir_tabla, pausar


# ---------- AFP ----------

def listar_afp():
    return fetch_all("SELECT * FROM afp ORDER BY codigo")


def menu_crear_afp():
    titulo("Nueva AFP")
    data = {
        "codigo": pedir_texto("Código AFP"),
        "nombre": pedir_texto("Nombre AFP"),
        "factor_cotizacion": pedir_monto("Factor de Cotización (%)"),
        "sistema_previsional": pedir_opcion("Sistema Previsional", ["Nuevo", "Antiguo"]),
    }
    insert("afp", data)
    print("AFP creada.")
    pausar()


def menu_listar_afp():
    titulo("Listado de AFP")
    imprimir_tabla(listar_afp())
    pausar()


def menu_editar_afp():
    titulo("Editar AFP")
    imprimir_tabla(listar_afp())
    codigo = pedir_texto("Código AFP a editar")
    if not fetch_one("SELECT * FROM afp WHERE codigo = ?", (codigo,)):
        print("AFP no encontrada.")
        pausar()
        return
    data = {
        "nombre": pedir_texto("Nombre AFP"),
        "factor_cotizacion": pedir_monto("Factor de Cotización (%)"),
        "sistema_previsional": pedir_opcion("Sistema Previsional", ["Nuevo", "Antiguo"]),
    }
    update("afp", data, "codigo = ?", (codigo,))
    print("AFP actualizada.")
    pausar()


def menu_eliminar_afp():
    titulo("Eliminar AFP")
    imprimir_tabla(listar_afp())
    codigo = pedir_texto("Código AFP a eliminar")
    delete("afp", "codigo = ?", (codigo,))
    print("AFP eliminada.")
    pausar()


# ---------- Isapre ----------

def listar_isapres():
    return fetch_all("SELECT * FROM isapre ORDER BY codigo")


def menu_crear_isapre():
    titulo("Nueva Isapre")
    data = {"codigo": pedir_texto("Código"), "nombre": pedir_texto("Nombre")}
    insert("isapre", data)
    print("Isapre creada.")
    pausar()


def menu_listar_isapres():
    titulo("Listado de Isapres")
    imprimir_tabla(listar_isapres())
    pausar()


def menu_eliminar_isapre():
    titulo("Eliminar Isapre")
    imprimir_tabla(listar_isapres())
    codigo = pedir_texto("Código a eliminar")
    delete("isapre", "codigo = ?", (codigo,))
    print("Isapre eliminada.")
    pausar()


# ---------- CCAF ----------

def listar_ccaf():
    return fetch_all("SELECT * FROM ccaf ORDER BY codigo")


def menu_crear_ccaf():
    titulo("Nueva CCAF")
    data = {"codigo": pedir_texto("Código"), "nombre": pedir_texto("Nombre")}
    insert("ccaf", data)
    print("CCAF creada.")
    pausar()


def menu_listar_ccaf():
    titulo("Listado de CCAF")
    imprimir_tabla(listar_ccaf())
    pausar()


def menu_eliminar_ccaf():
    titulo("Eliminar CCAF")
    imprimir_tabla(listar_ccaf())
    codigo = pedir_texto("Código a eliminar")
    delete("ccaf", "codigo = ?", (codigo,))
    print("CCAF eliminada.")
    pausar()


# ---------- Mutual ----------

def listar_mutuales():
    return fetch_all("SELECT * FROM mutual ORDER BY codigo")


def menu_crear_mutual():
    titulo("Nueva Mutual")
    data = {"codigo": pedir_texto("Código"), "nombre": pedir_texto("Nombre")}
    insert("mutual", data)
    print("Mutual creada.")
    pausar()


def menu_listar_mutuales():
    titulo("Listado de Mutuales")
    imprimir_tabla(listar_mutuales())
    pausar()


def menu_eliminar_mutual():
    titulo("Eliminar Mutual")
    imprimir_tabla(listar_mutuales())
    codigo = pedir_texto("Código a eliminar")
    delete("mutual", "codigo = ?", (codigo,))
    print("Mutual eliminada.")
    pausar()


# ---------- APV ----------

def listar_apv():
    return fetch_all("SELECT * FROM apv ORDER BY codigo")


def menu_crear_apv():
    titulo("Nueva Institución APV")
    data = {"codigo": pedir_texto("Código"), "nombre": pedir_texto("Nombre")}
    insert("apv", data)
    print("Institución APV creada.")
    pausar()


def menu_listar_apv():
    titulo("Listado de Instituciones APV")
    imprimir_tabla(listar_apv())
    pausar()


def menu_eliminar_apv():
    titulo("Eliminar Institución APV")
    imprimir_tabla(listar_apv())
    codigo = pedir_texto("Código a eliminar")
    delete("apv", "codigo = ?", (codigo,))
    print("Institución APV eliminada.")
    pausar()
