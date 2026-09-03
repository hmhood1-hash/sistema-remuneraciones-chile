"""
Menús principales del sistema de remuneraciones (interfaz de consola).
"""
from ui.utils import titulo, pausar

from modules import empresa, trabajador, previsional, parametros, haberes, contrato, finiquito, vacaciones
from modules import liquidacion, reportes


def _menu(opciones, encabezado):
    """
    opciones: lista de tuplas (etiqueta, función). La opción "0" (Volver/Salir) se agrega
    automáticamente por el llamador si corresponde.
    """
    while True:
        titulo(encabezado)
        for idx, (etiqueta, _) in enumerate(opciones):
            print(f"  {idx}. {etiqueta}")
        seleccion = input("\nSeleccione una opción: ").strip()
        if not seleccion.isdigit() or not (0 <= int(seleccion) < len(opciones)):
            print("Opción inválida.")
            pausar()
            continue
        seleccion = int(seleccion)
        etiqueta, funcion = opciones[seleccion]
        if funcion is None:  # Volver
            return
        funcion()


def menu_gestion_empresa():
    opciones = [
        ("Volver", None),
        ("Crear Empresa", empresa.menu_crear_empresa),
        ("Listar Empresas", empresa.menu_listar_empresas),
        ("Editar Empresa", empresa.menu_editar_empresa),
        ("Eliminar Empresa", empresa.menu_eliminar_empresa),
        ("Crear Sucursal", empresa.menu_crear_sucursal),
        ("Listar Sucursales", empresa.menu_listar_sucursales),
        ("Eliminar Sucursal", empresa.menu_eliminar_sucursal),
        ("Crear Centro de Costo", empresa.menu_crear_centro_costo),
        ("Listar Centros de Costo", empresa.menu_listar_centros_costo),
        ("Eliminar Centro de Costo", empresa.menu_eliminar_centro_costo),
    ]
    _menu(opciones, "Gestión de Empresa / Sucursales / Centros de Costo")


def menu_gestion_trabajador():
    opciones = [
        ("Volver", None),
        ("Crear Trabajador", trabajador.menu_crear_trabajador),
        ("Listar Trabajadores", trabajador.menu_listar_trabajadores),
        ("Editar Trabajador", trabajador.menu_editar_trabajador),
        ("Eliminar Trabajador", trabajador.menu_eliminar_trabajador),
        ("Datos Laborales", trabajador.menu_datos_laborales),
        ("Datos Previsionales", trabajador.menu_datos_previsionales),
        ("Cargas Familiares", trabajador.menu_cargas_familiares),
    ]
    _menu(opciones, "Gestión de Trabajadores")


def menu_instituciones_previsionales():
    opciones = [
        ("Volver", None),
        ("Crear AFP", previsional.menu_crear_afp),
        ("Listar AFP", previsional.menu_listar_afp),
        ("Editar AFP", previsional.menu_editar_afp),
        ("Eliminar AFP", previsional.menu_eliminar_afp),
        ("Crear Isapre", previsional.menu_crear_isapre),
        ("Listar Isapres", previsional.menu_listar_isapres),
        ("Eliminar Isapre", previsional.menu_eliminar_isapre),
        ("Crear CCAF", previsional.menu_crear_ccaf),
        ("Listar CCAF", previsional.menu_listar_ccaf),
        ("Eliminar CCAF", previsional.menu_eliminar_ccaf),
        ("Crear Mutual", previsional.menu_crear_mutual),
        ("Listar Mutuales", previsional.menu_listar_mutuales),
        ("Eliminar Mutual", previsional.menu_eliminar_mutual),
        ("Crear Institución APV", previsional.menu_crear_apv),
        ("Listar Instituciones APV", previsional.menu_listar_apv),
        ("Eliminar Institución APV", previsional.menu_eliminar_apv),
    ]
    _menu(opciones, "Instituciones Previsionales")


def menu_parametros():
    opciones = [
        ("Volver", None),
        ("Parámetros Generales del Año", parametros.menu_parametros),
        ("Factores de Actualización Mensuales (UTM/UF)", parametros.menu_factores_actualizacion),
        ("Listar Factores de Actualización", parametros.menu_listar_factores_actualizacion),
        ("Tramos de Cargas Familiares", parametros.menu_tramos_carga_familiar),
        ("Tabla de Impuesto Único (UTM)", parametros.menu_tabla_impuesto_unico),
        ("Tabla de Impuesto Único ($)", parametros.menu_tabla_impuesto_unico_pesos),
    ]
    _menu(opciones, "Parámetros y Factores")


def menu_haberes_descuentos():
    opciones = [
        ("Volver", None),
        ("Crear Haber/Descuento", haberes.menu_crear_haber_descuento),
        ("Listar Haberes/Descuentos", haberes.menu_listar_haberes_descuentos),
        ("Editar Haber/Descuento", haberes.menu_editar_haber_descuento),
        ("Eliminar Haber/Descuento", haberes.menu_eliminar_haber_descuento),
    ]
    _menu(opciones, "Haberes y Descuentos")


def menu_contratos_finiquitos():
    opciones = [
        ("Volver", None),
        ("Crear Tipo de Contrato", contrato.menu_crear_tipo_contrato),
        ("Listar Tipos de Contrato", contrato.menu_listar_tipos_contrato),
        ("Eliminar Tipo de Contrato", contrato.menu_eliminar_tipo_contrato),
        ("Crear Contrato", contrato.menu_crear_contrato),
        ("Listar Contratos", contrato.menu_listar_contratos),
        ("Eliminar Contrato", contrato.menu_eliminar_contrato),
        ("Crear Causal de Finiquito", contrato.menu_crear_causal_finiquito),
        ("Listar Causales de Finiquito", contrato.menu_listar_causales_finiquito),
        ("Eliminar Causal de Finiquito", contrato.menu_eliminar_causal_finiquito),
        ("Registrar Finiquito", finiquito.menu_crear_finiquito),
        ("Listar Finiquitos", finiquito.menu_listar_finiquitos),
        ("Eliminar Finiquito", finiquito.menu_eliminar_finiquito),
    ]
    _menu(opciones, "Contratos y Finiquitos")


def menu_vacaciones():
    opciones = [
        ("Volver", None),
        ("Registrar Vacaciones", vacaciones.menu_registrar_vacaciones),
        ("Listar Vacaciones", vacaciones.menu_listar_vacaciones),
        ("Eliminar Registro de Vacaciones", vacaciones.menu_eliminar_vacaciones),
    ]
    _menu(opciones, "Control de Vacaciones")


def menu_liquidaciones():
    opciones = [
        ("Volver", None),
        ("Calcular Liquidación Individual", liquidacion.menu_calcular_liquidacion),
        ("Ver Liquidación Guardada", liquidacion.menu_ver_liquidacion),
        ("Calcular Liquidaciones por Empresa", liquidacion.menu_calcular_liquidaciones_empresa),
    ]
    _menu(opciones, "Liquidaciones de Sueldo")


def menu_informes():
    opciones = [
        ("Volver", None),
        ("Libro de Remuneraciones", reportes.menu_libro_remuneraciones),
        ("Detalle de Pago de Imposiciones", reportes.menu_detalle_pago_imposiciones),
        ("Detalle de Anticipos", reportes.menu_detalle_anticipos),
        ("Ficha del Trabajador", reportes.menu_ficha_trabajador),
        ("Informe de Vacaciones", reportes.menu_informe_vacaciones),
        ("Certificado Tributario de Remuneraciones", reportes.menu_certificado_tributario),
    ]
    _menu(opciones, "Informes y Reportes")


def menu_procesos():
    from modules import procesos
    opciones = [
        ("Volver", None),
        ("Centralización Mensual", procesos.menu_centralizacion_mensual),
        ("Actualiza Base de Datos", procesos.menu_actualiza_base_datos),
    ]
    _menu(opciones, "Procesos")


def menu_principal():
    opciones = [
        ("Salir", None),
        ("Gestión de Empresa / Sucursales / Centros de Costo", menu_gestion_empresa),
        ("Gestión de Trabajadores", menu_gestion_trabajador),
        ("Instituciones Previsionales", menu_instituciones_previsionales),
        ("Parámetros y Factores", menu_parametros),
        ("Haberes y Descuentos", menu_haberes_descuentos),
        ("Contratos y Finiquitos", menu_contratos_finiquitos),
        ("Control de Vacaciones", menu_vacaciones),
        ("Liquidaciones de Sueldo", menu_liquidaciones),
        ("Informes y Reportes", menu_informes),
        ("Procesos", menu_procesos),
    ]
    _menu(opciones, "SISTEMA DE REMUNERACIONES - CHILE")
