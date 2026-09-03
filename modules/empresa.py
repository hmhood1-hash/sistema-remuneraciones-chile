"""
Módulo de gestión de empresa, sucursales y centros de costo
"""
from database.models import fetch_all, fetch_one, insert, update, delete
from ui.utils import (
    titulo, pedir_texto, pedir_rut, pedir_entero, imprimir_tabla, pausar,
)


def menu_gestion_empresa():
    """
    Menú de gestión de empresa
    """
    opciones = {
        0: ("Volver", lambda: None),
        1: ("Crear Empresa", menu_crear_empresa),
        2: ("Listar Empresas", menu_listar_empresas),
        3: ("Modificar Empresa", menu_modificar_empresa),
        4: ("Gestión de Sucursales", menu_sucursales),
        5: ("Gestión de Centros de Costo", menu_centros_costo),
    }
    from ui.menus import _menu
    _menu(opciones, "Gestión de Empresa / Sucursales / Centros de Costo")


def menu_crear_empresa():
    """
    Crea una nueva empresa
    """
    titulo("Crear Nueva Empresa")
    
    data = _pedir_datos_empresa()
    
    try:
        codigo = insert('empresa', data)
        print(f"\n  ✓ Empresa creada con código {codigo}")
        pausar()
    except Exception as e:
        print(f"  ✗ Error: {str(e)}")
        pausar()


def _pedir_datos_empresa():
    """
    Pide los datos de una empresa
    """
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
    data["rep_legal_nombres"] = pedir_texto("Nombres Representante", obligatorio=False)
    data["rep_legal_ap_paterno"] = pedir_texto("Ap. Paterno Representante", obligatorio=False)
    data["rep_legal_ap_materno"] = pedir_texto("Ap. Materno Representante", obligatorio=False)
    
    return data


def menu_listar_empresas():
    """
    Lista todas las empresas
    """
    titulo("Listado de Empresas")
    
    empresas = fetch_all('empresa')
    
    if empresas:
        columnas = ['codigo', 'rut', 'razon_social', 'ciudad', 'region']
        imprimir_tabla(empresas, columnas)
    else:
        print("  * Sin empresas registradas")
    
    pausar()


def menu_modificar_empresa():
    """
    Modifica una empresa existente
    """
    titulo("Modificar Empresa")
    
    rut = pedir_rut("RUT de la empresa a modificar")
    empresa = fetch_one('empresa', {'rut': rut})
    
    if not empresa:
        print("  ✗ Empresa no encontrada")
        pausar()
        return
    
    print(f"  Empresa: {empresa['razon_social']}")
    
    data = {}
    data["razon_social"] = pedir_texto("Razón Social", default=empresa.get('razon_social', ''))
    data["ciudad"] = pedir_texto("Ciudad", obligatorio=False, default=empresa.get('ciudad', ''))
    data["region"] = pedir_texto("Región", obligatorio=False, default=empresa.get('region', ''))
    
    try:
        update('empresa', data, {'rut': rut})
        print("  ✓ Empresa actualizada")
        pausar()
    except Exception as e:
        print(f"  ✗ Error: {str(e)}")
        pausar()


def menu_sucursales():
    """
    Menú de gestión de sucursales
    """
    opciones = {
        0: ("Volver", lambda: None),
        1: ("Crear Sucursal", crear_sucursal),
        2: ("Listar Sucursales", listar_sucursales),
        3: ("Modificar Sucursal", modificar_sucursal),
        4: ("Eliminar Sucursal", eliminar_sucursal),
    }
    from ui.menus import _menu
    _menu(opciones, "Gestión de Sucursales")


def crear_sucursal():
    """
    Crea una nueva sucursal
    """
    titulo("Crear Sucursal")
    
    empresas = fetch_all('empresa')
    if not empresas:
        print("  ✗ No hay empresas registradas")
        pausar()
        return
    
    print("  Empresas disponibles:")
    for emp in empresas:
        print(f"    {emp['codigo']}: {emp['razon_social']}")
    
    empresa_codigo = pedir_entero("Código de Empresa")
    
    data = {
        'empresa_codigo': empresa_codigo,
        'nombre': pedir_texto("Nombre Sucursal"),
        'direccion': pedir_texto("Dirección", obligatorio=False),
        'region': pedir_texto("Región", obligatorio=False),
        'ciudad': pedir_texto("Ciudad", obligatorio=False),
        'comuna': pedir_texto("Comuna", obligatorio=False),
        'fono': pedir_texto("Fono", obligatorio=False),
    }
    
    try:
        codigo = insert('sucursal', data)
        print(f"  ✓ Sucursal creada con código {codigo}")
        pausar()
    except Exception as e:
        print(f"  ✗ Error: {str(e)}")
        pausar()


def listar_sucursales():
    """
    Lista todas las sucursales
    """
    titulo("Listado de Sucursales")
    
    sucursales = fetch_all('sucursal')
    
    if sucursales:
        columnas = ['codigo', 'nombre', 'ciudad', 'region']
        imprimir_tabla(sucursales, columnas)
    else:
        print("  * Sin sucursales registradas")
    
    pausar()


def modificar_sucursal():
    """
    Modifica una sucursal
    """
    titulo("Modificar Sucursal")
    
    codigo = pedir_entero("Código de Sucursal a modificar")
    sucursal = fetch_one('sucursal', {'codigo': codigo})
    
    if not sucursal:
        print("  ✗ Sucursal no encontrada")
        pausar()
        return
    
    data = {
        'nombre': pedir_texto("Nombre", default=sucursal.get('nombre', '')),
        'ciudad': pedir_texto("Ciudad", obligatorio=False, default=sucursal.get('ciudad', '')),
    }
    
    try:
        update('sucursal', data, {'codigo': codigo})
        print("  ✓ Sucursal actualizada")
        pausar()
    except Exception as e:
        print(f"  ✗ Error: {str(e)}")
        pausar()


def eliminar_sucursal():
    """
    Elimina una sucursal
    """
    titulo("Eliminar Sucursal")
    
    codigo = pedir_entero("Código de Sucursal a eliminar")
    
    try:
        delete('sucursal', {'codigo': codigo})
        print("  ✓ Sucursal eliminada")
        pausar()
    except Exception as e:
        print(f"  ✗ Error: {str(e)}")
        pausar()


def menu_centros_costo():
    """
    Menú de gestión de centros de costo
    """
    opciones = {
        0: ("Volver", lambda: None),
        1: ("Crear Centro de Costo", crear_centro_costo),
        2: ("Listar Centros de Costo", listar_centros_costo),
        3: ("Modificar Centro de Costo", modificar_centro_costo),
        4: ("Eliminar Centro de Costo", eliminar_centro_costo),
    }
    from ui.menus import _menu
    _menu(opciones, "Gestión de Centros de Costo")


def crear_centro_costo():
    """
    Crea un nuevo centro de costo
    """
    titulo("Crear Centro de Costo")
    
    empresas = fetch_all('empresa')
    if not empresas:
        print("  ✗ No hay empresas registradas")
        pausar()
        return
    
    print("  Empresas disponibles:")
    for emp in empresas:
        print(f"    {emp['codigo']}: {emp['razon_social']}")
    
    data = {
        'empresa_codigo': pedir_entero("Código de Empresa"),
        'descripcion': pedir_texto("Descripción"),
    }
    
    try:
        codigo = insert('centro_costo', data)
        print(f"  ✓ Centro de Costo creado con código {codigo}")
        pausar()
    except Exception as e:
        print(f"  ✗ Error: {str(e)}")
        pausar()


def listar_centros_costo():
    """
    Lista todos los centros de costo
    """
    titulo("Listado de Centros de Costo")
    
    centros = fetch_all('centro_costo')
    
    if centros:
        columnas = ['codigo', 'descripcion', 'empresa_codigo']
        imprimir_tabla(centros, columnas)
    else:
        print("  * Sin centros de costo registrados")
    
    pausar()


def modificar_centro_costo():
    """
    Modifica un centro de costo
    """
    titulo("Modificar Centro de Costo")
    
    codigo = pedir_entero("Código de Centro de Costo a modificar")
    centro = fetch_one('centro_costo', {'codigo': codigo})
    
    if not centro:
        print("  ✗ Centro de Costo no encontrado")
        pausar()
        return
    
    data = {
        'descripcion': pedir_texto("Descripción", default=centro.get('descripcion', ''))
    }
    
    try:
        update('centro_costo', data, {'codigo': codigo})
        print("  ✓ Centro de Costo actualizado")
        pausar()
    except Exception as e:
        print(f"  ✗ Error: {str(e)}")
        pausar()


def eliminar_centro_costo():
    """
    Elimina un centro de costo
    """
    titulo("Eliminar Centro de Costo")
    
    codigo = pedir_entero("Código de Centro de Costo a eliminar")
    
    try:
        delete('centro_costo', {'codigo': codigo})
        print("  ✓ Centro de Costo eliminado")
        pausar()
    except Exception as e:
        print(f"  ✗ Error: {str(e)}")
        pausar()
