"""
Módulo de gestión de Haberes y Descuentos.
"""
from database.models import fetch_all, fetch_one, insert, update, delete
from ui.utils import titulo, pedir_texto, pedir_monto, pedir_opcion, imprimir_tabla, pausar, pedir_entero


CLASIFICACIONES = ["Imponible", "Tributable", "Adicional HE", "Adicional Valor Dia/Hora", "Horas Extras",
                   "No Imponible"]
CLASES = ["Fijo", "Variable", "Valor Diario", "Semana Corrida", "Porcentaje"]
BASES_CALCULO = ["Sueldo Base", "Sueldo Imponible", "Ninguna"]


def listar_haberes_descuentos(tipo=None):
    if tipo:
        return fetch_all("SELECT * FROM haber_descuento WHERE tipo = ? ORDER BY codigo", (tipo,))
    return fetch_all("SELECT * FROM haber_descuento ORDER BY codigo")


def obtener_haber_descuento(codigo):
    return fetch_one("SELECT * FROM haber_descuento WHERE codigo = ?", (codigo,))


def crear_haber_descuento(data):
    return insert("haber_descuento", data)


def actualizar_haber_descuento(codigo, data):
    return update("haber_descuento", data, "codigo = ?", (codigo,))


def eliminar_haber_descuento(codigo):
    return delete("haber_descuento", "codigo = ?", (codigo,))


def _pedir_datos_haber_descuento():
    data = {}
    data["nombre"] = pedir_texto("Nombre")
    data["tipo"] = pedir_opcion("Tipo", ["Haber", "Descuento"])
    data["clasificacion"] = pedir_opcion("Clasificación", CLASIFICACIONES)
    data["clase"] = pedir_opcion("Clase", CLASES)
    if data["clase"] == "Porcentaje":
        data["porcentaje"] = pedir_monto("Porcentaje")
        data["base_calculo"] = pedir_opcion("Base de Cálculo", ["Sueldo Base", "Sueldo Imponible"])
        data["monto"] = 0
    else:
        data["monto"] = pedir_monto("Monto en pesos")
        data["porcentaje"] = 0
        data["base_calculo"] = "Ninguna"
    return data


def menu_crear_haber_descuento():
    titulo("Nuevo Haber/Descuento")
    data = _pedir_datos_haber_descuento()
    codigo = crear_haber_descuento(data)
    print(f"Registro creado con código: {codigo}")
    pausar()


def menu_listar_haberes_descuentos():
    titulo("Listado de Haberes y Descuentos")
    imprimir_tabla(listar_haberes_descuentos())
    pausar()


def menu_editar_haber_descuento():
    titulo("Editar Haber/Descuento")
    imprimir_tabla(listar_haberes_descuentos())
    codigo = pedir_entero("Código a editar")
    if not obtener_haber_descuento(codigo):
        print("Registro no encontrado.")
        pausar()
        return
    data = _pedir_datos_haber_descuento()
    actualizar_haber_descuento(codigo, data)
    print("Registro actualizado.")
    pausar()


def menu_eliminar_haber_descuento():
    titulo("Eliminar Haber/Descuento")
    imprimir_tabla(listar_haberes_descuentos())
    codigo = pedir_entero("Código a eliminar")
    eliminar_haber_descuento(codigo)
    print("Registro eliminado.")
    pausar()


def calcular_monto_haber_descuento(item, sueldo_base, sueldo_imponible):
    """Calcula el monto en pesos de un haber/descuento según su clase."""
    if item["clase"] == "Porcentaje":
        base = sueldo_base if item["base_calculo"] == "Sueldo Base" else sueldo_imponible
        return round(base * item["porcentaje"] / 100.0)
    return item["monto"]
