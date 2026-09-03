"""
Módulo de gestión de Empresa, Sucursales y Centros de Costo.
"""
from database.models import fetch_all, fetch_one, insert, update, delete
from ui.utils import (
    titulo, pedir_texto, pedir_rut, pedir_entero, imprimir_tabla, pausar,
)


# ---------- Empresa ----------

def listar_empresas():
    return fetch_all("SELECT * FROM empresa ORDER BY codigo")


def obtener_empresa(codigo):
    return fetch_one("SELECT * FROM empresa WHERE codigo = ?", (codigo,))


def crear_empresa(data):
    return insert("empresa", data)


def actualizar_empresa(codigo, data):
    return update("empresa", data, "codigo = ?", (codigo,))


def eliminar_empresa(codigo):
    return delete("empresa", "codigo = ?", (codigo,))


def _pedir_datos_empresa():
    data = {}
    data["rut"] = pedir_rut("RUT Empresa")
    data["razon_social"] = pedir_texto("Razón Social")
    data["calle"] = pedir_texto("Calle", obligatorio=False)
    data["numero"] = pedir_texto("Número", obligatorio=False)
    data["depto"] = pedir_texto("Depto", obligatorio=False)
    data["poblacion_villa"] = pedir_texto("Población/Villa", obligatorio=False)
    data["comuna"] = pedir_texto("Comuna", obligatorio=False)
    data["ciudad"] = pedir_texto("Ciudad", obligatorio=False)
    data["region"] = pedir_texto("Región", obligatorio=False)
    data["correo"] = pedir_texto("Correo", obligatorio=False)
    data["fono"] = pedir_texto("Fono", obligatorio=False)
    data["giro_comercial"] = pedir_texto("Giro Comercial", obligatorio=False)
    data["codigo_actividad_economica"] = pedir_texto("Código Actividad Económica", obligatorio=False)
    data["rep_legal_rut"] = pedir_rut("RUT Representante Legal")
    data["rep_legal_nombres"] = pedir_texto("Nombres Rep. Legal", obligatorio=False)
    data["rep_legal_ap_paterno"] = pedir_texto("Apellido Paterno Rep. Legal", obligatorio=False)
    data["rep_legal_ap_materno"] = pedir_texto("Apellido Materno Rep. Legal", obligatorio=False)
    return data


def menu_crear_empresa():
    titulo("Nueva Empresa")
    data = _pedir_datos_empresa()
    codigo = crear_empresa(data)
    print(f"Empresa creada con código: {codigo}")
    pausar()


def menu_listar_empresas():
    titulo("Listado de Empresas")
    imprimir_tabla(listar_empresas())
    pausar()


def menu_editar_empresa():
    titulo("Editar Empresa")
    imprimir_tabla(listar_empresas())
    codigo = pedir_entero("Código de empresa a editar")
    empresa = obtener_empresa(codigo)
    if not empresa:
        print("Empresa no encontrada.")
        pausar()
        return
    print("Ingrese los nuevos datos (los campos son obligatorios salvo indicación):")
    data = _pedir_datos_empresa()
    actualizar_empresa(codigo, data)
    print("Empresa actualizada.")
    pausar()


def menu_eliminar_empresa():
    titulo("Eliminar Empresa")
    imprimir_tabla(listar_empresas())
    codigo = pedir_entero("Código de empresa a eliminar")
    eliminar_empresa(codigo)
    print("Empresa eliminada.")
    pausar()


# ---------- Sucursales ----------

def listar_sucursales(empresa_codigo=None):
    if empresa_codigo:
        return fetch_all("SELECT * FROM sucursal WHERE empresa_codigo = ? ORDER BY codigo", (empresa_codigo,))
    return fetch_all("SELECT * FROM sucursal ORDER BY codigo")


def crear_sucursal(data):
    return insert("sucursal", data)


def menu_crear_sucursal():
    titulo("Nueva Sucursal")
    imprimir_tabla(listar_empresas())
    empresa_codigo = pedir_entero("Código de empresa")
    data = {
        "empresa_codigo": empresa_codigo,
        "nombre": pedir_texto("Nombre"),
        "direccion": pedir_texto("Dirección", obligatorio=False),
        "region": pedir_texto("Región", obligatorio=False),
        "ciudad": pedir_texto("Ciudad", obligatorio=False),
        "comuna": pedir_texto("Comuna", obligatorio=False),
        "fono": pedir_texto("Fono", obligatorio=False),
    }
    codigo = crear_sucursal(data)
    print(f"Sucursal creada con código: {codigo}")
    pausar()


def menu_listar_sucursales():
    titulo("Listado de Sucursales")
    imprimir_tabla(listar_sucursales())
    pausar()


def menu_eliminar_sucursal():
    titulo("Eliminar Sucursal")
    imprimir_tabla(listar_sucursales())
    codigo = pedir_entero("Código de sucursal a eliminar")
    delete("sucursal", "codigo = ?", (codigo,))
    print("Sucursal eliminada.")
    pausar()


# ---------- Centros de Costo ----------

def listar_centros_costo(empresa_codigo=None):
    if empresa_codigo:
        return fetch_all("SELECT * FROM centro_costo WHERE empresa_codigo = ? ORDER BY codigo", (empresa_codigo,))
    return fetch_all("SELECT * FROM centro_costo ORDER BY codigo")


def crear_centro_costo(data):
    return insert("centro_costo", data)


def menu_crear_centro_costo():
    titulo("Nuevo Centro de Costo")
    imprimir_tabla(listar_empresas())
    empresa_codigo = pedir_entero("Código de empresa")
    data = {
        "empresa_codigo": empresa_codigo,
        "descripcion": pedir_texto("Descripción"),
    }
    codigo = crear_centro_costo(data)
    print(f"Centro de costo creado con código: {codigo}")
    pausar()


def menu_listar_centros_costo():
    titulo("Listado de Centros de Costo")
    imprimir_tabla(listar_centros_costo())
    pausar()


def menu_eliminar_centro_costo():
    titulo("Eliminar Centro de Costo")
    imprimir_tabla(listar_centros_costo())
    codigo = pedir_entero("Código de centro de costo a eliminar")
    delete("centro_costo", "codigo = ?", (codigo,))
    print("Centro de costo eliminado.")
    pausar()
