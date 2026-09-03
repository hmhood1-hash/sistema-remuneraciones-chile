# -*- coding: utf-8 -*-
"""Construcción de los menús desplegables de la ventana principal."""
import tkinter as tk

from modules import empresa as mod_empresa
from modules import previsional as mod_previsional
from modules import haberes as mod_haberes
from modules import parametros as mod_parametros

from ui.dialogs import VentanaCRUD
from ui import ventanas_empresa
from ui import ventanas_trabajador
from ui import ventanas_parametros
from ui import ventanas_liquidacion
from ui import ventanas_contrato
from ui import ventanas_vacaciones
from ui import ventanas_informes
from ui import ventanas_procesos
from ui.utils import mostrar_info


def _crud_afp(maestro):
    campos = [
        {"nombre": "codigo_afp", "etiqueta": "Código", "requerido": True},
        {"nombre": "nombre", "etiqueta": "Nombre AFP", "requerido": True},
        {"nombre": "factor_cotizacion", "etiqueta": "Factor Cotización (%)", "tipo": "numero"},
        {"nombre": "sistema_previsional", "etiqueta": "Sistema Previsional", "tipo": "combo",
         "opciones": ["Nuevo", "Antiguo"]},
    ]
    funciones = {
        "listar": mod_previsional.listar_afp,
        "crear": mod_previsional.crear_afp,
        "actualizar": mod_previsional.actualizar_afp,
        "eliminar": mod_previsional.eliminar_afp,
    }
    VentanaCRUD(maestro, "AFP - Instituciones Previsionales", list(f["nombre"] for f in campos),
                campos, funciones, id_campo="codigo_afp")


def _crud_simple(maestro, titulo, campo_codigo, etiqueta_codigo, funciones):
    campos = [
        {"nombre": campo_codigo, "etiqueta": etiqueta_codigo, "requerido": True},
        {"nombre": "nombre", "etiqueta": "Nombre", "requerido": True},
    ]
    VentanaCRUD(maestro, titulo, [campo_codigo, "nombre"], campos, funciones, id_campo=campo_codigo)


def _crud_isapre(maestro):
    _crud_simple(maestro, "Isapres", "codigo_isapre", "Código", {
        "listar": mod_previsional.listar_isapres,
        "crear": mod_previsional.crear_isapre,
        "actualizar": mod_previsional.actualizar_isapre,
        "eliminar": mod_previsional.eliminar_isapre,
    })


def _crud_ccaf(maestro):
    _crud_simple(maestro, "CCAF", "codigo_ccaf", "Código", {
        "listar": mod_previsional.listar_ccaf,
        "crear": mod_previsional.crear_ccaf,
        "actualizar": mod_previsional.actualizar_ccaf,
        "eliminar": mod_previsional.eliminar_ccaf,
    })


def _crud_mutual(maestro):
    _crud_simple(maestro, "Mutuales", "codigo_mutual", "Código", {
        "listar": mod_previsional.listar_mutuales,
        "crear": mod_previsional.crear_mutual,
        "actualizar": mod_previsional.actualizar_mutual,
        "eliminar": mod_previsional.eliminar_mutual,
    })


def _crud_ahorro(maestro):
    _crud_simple(maestro, "Ahorro Previsional", "codigo_ahorro", "Código", {
        "listar": mod_previsional.listar_ahorros_previsionales,
        "crear": mod_previsional.crear_ahorro_previsional,
        "actualizar": mod_previsional.actualizar_ahorro_previsional,
        "eliminar": mod_previsional.eliminar_ahorro_previsional,
    })


def _crud_centro_costo(maestro):
    campos = [
        {"nombre": "codigo_centro_costo", "etiqueta": "Código", "requerido": True},
        {"nombre": "descripcion", "etiqueta": "Descripción", "requerido": True},
        {"nombre": "codigo_empresa", "etiqueta": "Código Empresa", "tipo": "numero"},
    ]
    funciones = {
        "listar": mod_empresa.listar_centros_costo,
        "crear": mod_empresa.crear_centro_costo,
        "actualizar": mod_empresa.actualizar_centro_costo,
        "eliminar": mod_empresa.eliminar_centro_costo,
    }
    VentanaCRUD(maestro, "Centros de Costo", ["codigo_centro_costo", "descripcion", "codigo_empresa"],
                campos, funciones, id_campo="codigo_centro_costo")


def _crud_sucursales(maestro):
    campos = [
        {"nombre": "codigo_empresa", "etiqueta": "Código Empresa", "tipo": "numero", "requerido": True},
        {"nombre": "nombre", "etiqueta": "Nombre", "requerido": True},
        {"nombre": "direccion", "etiqueta": "Dirección"},
        {"nombre": "region", "etiqueta": "Región"},
        {"nombre": "ciudad", "etiqueta": "Ciudad"},
        {"nombre": "comuna", "etiqueta": "Comuna"},
        {"nombre": "fono", "etiqueta": "Fono"},
    ]
    funciones = {
        "listar": mod_empresa.listar_sucursales,
        "crear": mod_empresa.crear_sucursal,
        "actualizar": mod_empresa.actualizar_sucursal,
        "eliminar": mod_empresa.eliminar_sucursal,
    }
    VentanaCRUD(maestro, "Sucursales",
                ["codigo_sucursal", "codigo_empresa", "nombre", "ciudad", "comuna", "fono"],
                campos, funciones, id_campo="codigo_sucursal")


def _crud_tipos_contrato(maestro):
    _crud_simple(maestro, "Tipos de Contrato", "codigo", "Código", {
        "listar": mod_parametros.listar_tipos_contrato,
        "crear": lambda d: mod_parametros.crear_tipo_contrato(d["codigo"], d["nombre"]),
        "actualizar": lambda c, d: None,
        "eliminar": lambda c: None,
    })


def _crud_causales_finiquito(maestro):
    _crud_simple(maestro, "Causales de Finiquito", "codigo", "Código", {
        "listar": mod_parametros.listar_causales_finiquito,
        "crear": lambda d: mod_parametros.crear_causal_finiquito(d["codigo"], d["nombre"]),
        "actualizar": lambda c, d: None,
        "eliminar": lambda c: None,
    })


def _crud_haberes(maestro):
    campos = [
        {"nombre": "codigo", "etiqueta": "Código", "requerido": True},
        {"nombre": "nombre", "etiqueta": "Nombre", "requerido": True},
        {"nombre": "clasificacion", "etiqueta": "Clasificación", "tipo": "combo", "opciones": [
            "Imponible", "Tributable", "Adicional HE", "Adicional Valor Dia-Hora",
            "Horas Extras", "Descuento",
        ]},
        {"nombre": "clase", "etiqueta": "Clase", "tipo": "combo", "opciones": [
            "Fijo", "Variable", "Valor diario", "Semana corrida", "Porcentaje",
        ]},
        {"nombre": "monto", "etiqueta": "Monto ($)", "tipo": "numero"},
        {"nombre": "porcentaje", "etiqueta": "Porcentaje (%)", "tipo": "numero"},
        {"nombre": "base_porcentaje", "etiqueta": "Base % sobre", "tipo": "combo",
         "opciones": ["N/A", "Sueldo base", "Sueldo imponible"]},
    ]
    funciones = {
        "listar": mod_haberes.listar_haberes_descuentos,
        "crear": mod_haberes.crear_haber_descuento,
        "actualizar": mod_haberes.actualizar_haber_descuento,
        "eliminar": mod_haberes.eliminar_haber_descuento,
    }
    VentanaCRUD(maestro, "Haberes y Descuentos",
                ["codigo", "nombre", "clasificacion", "clase", "monto", "porcentaje"],
                campos, funciones, id_campo="codigo")


def _acerca_de(maestro):
    mostrar_info(
        "Acerca de",
        "Sistema Profesional de Remuneraciones Chile\n"
        "Gestión de nómina, liquidaciones e impuesto único.\n"
        "100% compatible con Windows 10/11.",
    )


def construir_menu(root):
    """Construye la barra de menús desplegable de la ventana principal."""
    barra = tk.Menu(root)

    # 1. Datos Base
    menu_datos = tk.Menu(barra, tearoff=0)
    menu_datos.add_command(label="Empresa", command=lambda: ventanas_empresa.abrir_ventana_empresa(root))
    menu_datos.add_command(label="Sucursales", command=lambda: _crud_sucursales(root))
    menu_datos.add_command(label="Centros de Costo", command=lambda: _crud_centro_costo(root))
    menu_datos.add_separator()
    menu_datos.add_command(
        label="Trabajadores", command=lambda: ventanas_trabajador.abrir_ventana_trabajadores(root)
    )
    barra.add_cascade(label="Datos Base", menu=menu_datos)

    # 2. Instituciones Previsionales
    menu_previsional = tk.Menu(barra, tearoff=0)
    menu_previsional.add_command(label="AFP", command=lambda: _crud_afp(root))
    menu_previsional.add_command(label="Isapres", command=lambda: _crud_isapre(root))
    menu_previsional.add_command(label="CCAF", command=lambda: _crud_ccaf(root))
    menu_previsional.add_command(label="Mutuales", command=lambda: _crud_mutual(root))
    menu_previsional.add_command(label="Ahorro Previsional", command=lambda: _crud_ahorro(root))
    barra.add_cascade(label="Instituciones Previsionales", menu=menu_previsional)

    # 3. Haberes y Descuentos
    barra.add_command(label="Haberes y Descuentos", command=lambda: _crud_haberes(root))

    # 4. Parámetros
    menu_parametros = tk.Menu(barra, tearoff=0)
    menu_parametros.add_command(
        label="Parámetros Generales",
        command=lambda: ventanas_parametros.abrir_ventana_parametros(root),
    )
    menu_parametros.add_command(
        label="Factores Mensuales (UTM / UF)",
        command=lambda: ventanas_parametros.abrir_ventana_factores(root),
    )
    menu_parametros.add_command(
        label="Cargas Familiares (Tramos)",
        command=lambda: ventanas_parametros.abrir_ventana_tramos_carga(root),
    )
    menu_parametros.add_command(
        label="Impuesto Único (Tabla)",
        command=lambda: ventanas_parametros.abrir_ventana_impuesto_unico(root),
    )
    menu_parametros.add_separator()
    menu_parametros.add_command(label="Tipos de Contrato", command=lambda: _crud_tipos_contrato(root))
    menu_parametros.add_command(label="Causales de Finiquito", command=lambda: _crud_causales_finiquito(root))
    barra.add_cascade(label="Parámetros", menu=menu_parametros)

    # 5. Liquidaciones
    menu_liquidaciones = tk.Menu(barra, tearoff=0)
    menu_liquidaciones.add_command(
        label="Liquidación Individual",
        command=lambda: ventanas_liquidacion.abrir_liquidacion_individual(root),
    )
    menu_liquidaciones.add_command(
        label="Liquidaciones por Empresa",
        command=lambda: ventanas_liquidacion.abrir_liquidaciones_empresa(root),
    )
    menu_liquidaciones.add_command(
        label="Pago Anticipos", command=lambda: ventanas_liquidacion.abrir_anticipos(root)
    )
    barra.add_cascade(label="Liquidaciones", menu=menu_liquidaciones)

    # 6. Contratos y Finiquitos
    menu_contratos = tk.Menu(barra, tearoff=0)
    menu_contratos.add_command(label="Contrato", command=lambda: ventanas_contrato.abrir_contrato(root))
    menu_contratos.add_command(label="Finiquito", command=lambda: ventanas_contrato.abrir_finiquito(root))
    barra.add_cascade(label="Contratos y Finiquitos", menu=menu_contratos)

    # 7. Vacaciones
    barra.add_command(
        label="Control de Vacaciones", command=lambda: ventanas_vacaciones.abrir_vacaciones(root)
    )

    # 8. Informes
    menu_informes = tk.Menu(barra, tearoff=0)
    menu_informes.add_command(
        label="Libro de Remuneraciones", command=lambda: ventanas_informes.libro_remuneraciones(root)
    )
    menu_informes.add_command(
        label="Detalle Pago Imposiciones", command=lambda: ventanas_informes.detalle_imposiciones(root)
    )
    menu_informes.add_command(
        label="Detalle de Anticipos", command=lambda: ventanas_informes.detalle_anticipos(root)
    )
    menu_informes.add_command(
        label="Ficha del Trabajador", command=lambda: ventanas_informes.ficha_trabajador(root)
    )
    menu_informes.add_command(
        label="Informe de Vacaciones", command=lambda: ventanas_informes.informe_vacaciones(root)
    )
    menu_informes.add_command(
        label="Certificado Tributario de Remuneraciones",
        command=lambda: ventanas_informes.certificado_tributario(root),
    )
    barra.add_cascade(label="Informes", menu=menu_informes)

    # 9. Procesos
    menu_procesos = tk.Menu(barra, tearoff=0)
    menu_procesos.add_command(
        label="Centralización Mensual", command=lambda: ventanas_procesos.centralizacion_mensual(root)
    )
    menu_procesos.add_command(
        label="Actualizar Base de Datos", command=lambda: ventanas_procesos.actualizar_bd(root)
    )
    menu_procesos.add_command(
        label="Respaldo de Base de Datos", command=lambda: ventanas_procesos.respaldar_bd(root)
    )
    barra.add_cascade(label="Procesos", menu=menu_procesos)

    # 10. Ayuda
    menu_ayuda = tk.Menu(barra, tearoff=0)
    menu_ayuda.add_command(label="Acerca de", command=lambda: _acerca_de(root))
    barra.add_cascade(label="Ayuda", menu=menu_ayuda)

    root.config(menu=barra)
    return barra
