# -*- coding: utf-8 -*-
"""Ventanas de Liquidación Individual, Liquidaciones por Empresa y Pago Anticipos."""
import os
import tkinter as tk
from datetime import datetime
from tkinter import ttk, filedialog

from modules import empresa as mod_empresa
from modules import trabajador as mod_trabajador
from modules import liquidacion as mod_liquidacion
from reportes import generador_excel, generador_pdf

from ui.estilos import COLOR_FONDO
from ui.tablas import TablaInteractiva
from ui.dialogs import FormularioModal
from ui.utils import centrar_ventana, mostrar_info, mostrar_error, formatear_pesos

MESES_NOMBRE = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
]


def _lista_empresas_opciones():
    return ["{} - {}".format(e["codigo_empresa"], e["razon_social"]) for e in mod_empresa.listar_empresas()]


def _lista_trabajadores_opciones(codigo_empresa=None):
    trabajadores = mod_trabajador.listar_trabajadores(codigo_empresa)
    return [
        "{} - {} {}".format(t["codigo_empleado"], t["nombres"], t["apellido_paterno"])
        for t in trabajadores
    ]


def abrir_liquidacion_individual(maestro):
    ventana = tk.Toplevel(maestro)
    ventana.title("Liquidación Individual")
    ventana.geometry("560x560")
    ventana.configure(bg=COLOR_FONDO)
    ventana.transient(maestro)

    marco_seleccion = ttk.Frame(ventana, padding=10)
    marco_seleccion.pack(fill=tk.X)

    ttk.Label(marco_seleccion, text="Trabajador:").grid(row=0, column=0, sticky=tk.W, padx=4, pady=4)
    var_trabajador = tk.StringVar()
    combo_trabajador = ttk.Combobox(marco_seleccion, textvariable=var_trabajador,
                                     values=_lista_trabajadores_opciones(), state="readonly", width=35)
    combo_trabajador.grid(row=0, column=1, padx=4, pady=4)

    ttk.Label(marco_seleccion, text="Mes:").grid(row=1, column=0, sticky=tk.W, padx=4, pady=4)
    var_mes = tk.StringVar(value=MESES_NOMBRE[datetime.now().month - 1])
    ttk.Combobox(marco_seleccion, textvariable=var_mes, values=MESES_NOMBRE, state="readonly",
                 width=15).grid(row=1, column=1, sticky=tk.W, padx=4, pady=4)

    ttk.Label(marco_seleccion, text="Año:").grid(row=2, column=0, sticky=tk.W, padx=4, pady=4)
    var_anio = tk.StringVar(value=str(datetime.now().year))
    ttk.Entry(marco_seleccion, textvariable=var_anio, width=10).grid(row=2, column=1, sticky=tk.W, padx=4, pady=4)

    marco_resultado = ttk.Frame(ventana, padding=10)
    marco_resultado.pack(fill=tk.BOTH, expand=True)

    texto_resultado = tk.Text(marco_resultado, height=20, width=60, state="disabled")
    texto_resultado.pack(fill=tk.BOTH, expand=True)

    resultado_actual = {"liquidacion": None, "trabajador": None}

    def calcular():
        if not var_trabajador.get():
            mostrar_error("Seleccione trabajador", "Debe seleccionar un trabajador.")
            return
        codigo_empleado = int(var_trabajador.get().split(" - ")[0])
        mes = MESES_NOMBRE.index(var_mes.get()) + 1
        try:
            anio = int(var_anio.get())
            liquidacion = mod_liquidacion.calcular_liquidacion(codigo_empleado, anio, mes)
        except Exception as error:  # noqa: BLE001
            mostrar_error("Error de cálculo", str(error))
            return

        trabajador = mod_trabajador.obtener_trabajador(codigo_empleado)
        resultado_actual["liquidacion"] = liquidacion
        resultado_actual["trabajador"] = trabajador

        texto_resultado.configure(state="normal")
        texto_resultado.delete("1.0", tk.END)
        lineas = [
            "LIQUIDACIÓN DE SUELDO - {} {}".format(trabajador["nombres"], trabajador["apellido_paterno"]),
            "RUT: {}    Período: {}/{}".format(trabajador["rut"], mes, anio),
            "-" * 55,
            "Sueldo Base: {}".format(formatear_pesos(liquidacion["sueldo_base"])),
            "Total Haberes Imponibles: {}".format(formatear_pesos(liquidacion["total_haberes_imponibles"])),
            "Total Haberes No Imponibles: {}".format(formatear_pesos(liquidacion["total_haberes_no_imponibles"])),
            "TOTAL INGRESO BRUTO: {}".format(formatear_pesos(liquidacion["total_ingreso_bruto"])),
            "",
            "Descuento AFP: {}".format(formatear_pesos(liquidacion["monto_afp"])),
            "Descuento Salud: {}".format(formatear_pesos(liquidacion["monto_salud"])),
            "Descuento Seguro Cesantía: {}".format(formatear_pesos(liquidacion["monto_seguro_cesantia"])),
            "Total Descuentos Previsionales: {}".format(
                formatear_pesos(liquidacion["total_descuentos_previsionales"])
            ),
            "",
            "Base Tributable: {}".format(formatear_pesos(liquidacion["base_tributable"])),
            "Impuesto Único: {}".format(formatear_pesos(liquidacion["impuesto_unico"])),
            "",
            "TOTAL DESCUENTOS: {}".format(formatear_pesos(liquidacion["total_descuentos"])),
            "SUELDO LÍQUIDO: {}".format(formatear_pesos(liquidacion["sueldo_liquido"])),
            "-" * 55,
            "Aportes Patronales: {}".format(formatear_pesos(liquidacion["total_aportes_patronales"])),
            "COSTO TOTAL EMPRESA: {}".format(formatear_pesos(liquidacion["costo_total_empresa"])),
        ]
        texto_resultado.insert(tk.END, "\n".join(lineas))
        texto_resultado.configure(state="disabled")

    def guardar():
        if not resultado_actual["liquidacion"]:
            mostrar_error("Sin cálculo", "Primero debe calcular la liquidación.")
            return
        mod_liquidacion.guardar_liquidacion(resultado_actual["liquidacion"])
        mostrar_info("Liquidación guardada", "La liquidación se guardó correctamente en la base de datos.")

    def exportar_excel():
        if not resultado_actual["liquidacion"]:
            mostrar_error("Sin cálculo", "Primero debe calcular la liquidación.")
            return
        ruta = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                             filetypes=[("Excel", "*.xlsx")])
        if ruta:
            generador_excel.exportar_liquidacion_individual(
                resultado_actual["liquidacion"], resultado_actual["trabajador"], ruta
            )
            mostrar_info("Exportado", "Liquidación exportada a: {}".format(ruta))

    def exportar_pdf():
        if not resultado_actual["liquidacion"]:
            mostrar_error("Sin cálculo", "Primero debe calcular la liquidación.")
            return
        ruta = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf")])
        if ruta:
            trabajador = resultado_actual["trabajador"]
            empresa = mod_empresa.obtener_empresa(trabajador["codigo_empresa"])
            generador_pdf.exportar_liquidacion_individual_pdf(
                resultado_actual["liquidacion"], trabajador, empresa, ruta
            )
            mostrar_info("Exportado", "Liquidación exportada a: {}".format(ruta))

    barra_botones = ttk.Frame(ventana, padding=8)
    barra_botones.pack(fill=tk.X)
    ttk.Button(barra_botones, text="Calcular", style="Acento.TButton", command=calcular).pack(
        side=tk.LEFT, padx=4
    )
    ttk.Button(barra_botones, text="Guardar", command=guardar).pack(side=tk.LEFT, padx=4)
    ttk.Button(barra_botones, text="Exportar Excel", command=exportar_excel).pack(side=tk.LEFT, padx=4)
    ttk.Button(barra_botones, text="Exportar PDF", command=exportar_pdf).pack(side=tk.LEFT, padx=4)
    ttk.Button(barra_botones, text="Cerrar", command=ventana.destroy).pack(side=tk.LEFT, padx=4)

    centrar_ventana(ventana, 560, 560)
    return ventana


def abrir_liquidaciones_empresa(maestro):
    ventana = tk.Toplevel(maestro)
    ventana.title("Liquidaciones por Empresa")
    ventana.geometry("820x520")
    ventana.configure(bg=COLOR_FONDO)
    ventana.transient(maestro)

    marco_filtro = ttk.Frame(ventana, padding=8)
    marco_filtro.pack(fill=tk.X)
    ttk.Label(marco_filtro, text="Empresa:").pack(side=tk.LEFT, padx=4)
    var_empresa = tk.StringVar()
    ttk.Combobox(marco_filtro, textvariable=var_empresa, values=_lista_empresas_opciones(),
                 state="readonly", width=30).pack(side=tk.LEFT, padx=4)
    ttk.Label(marco_filtro, text="Año:").pack(side=tk.LEFT, padx=4)
    var_anio = tk.StringVar(value=str(datetime.now().year))
    ttk.Entry(marco_filtro, textvariable=var_anio, width=8).pack(side=tk.LEFT, padx=4)
    ttk.Label(marco_filtro, text="Mes:").pack(side=tk.LEFT, padx=4)
    var_mes = tk.StringVar(value=str(datetime.now().month))
    ttk.Entry(marco_filtro, textvariable=var_mes, width=5).pack(side=tk.LEFT, padx=4)

    columnas = ["codigo_empleado", "anio", "mes", "sueldo_base", "total_ingreso_bruto",
                "total_descuentos", "sueldo_liquido", "costo_total_empresa"]
    tabla = TablaInteractiva(ventana, columnas)
    tabla.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

    def buscar():
        codigo_empresa = int(var_empresa.get().split(" - ")[0]) if var_empresa.get() else None
        anio = int(var_anio.get()) if var_anio.get() else None
        mes = int(var_mes.get()) if var_mes.get() else None
        filas = mod_liquidacion.listar_liquidaciones(codigo_empresa, anio, mes)
        for fila in filas:
            fila["_id"] = fila["id_liquidacion"]
        tabla.cargar_datos(filas)

    def exportar():
        ruta = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel", "*.xlsx")])
        if ruta:
            generador_excel.exportar_libro_remuneraciones(tabla.datos_completos, ruta)
            mostrar_info("Exportado", "Libro de remuneraciones exportado a: {}".format(ruta))

    barra_botones = ttk.Frame(ventana, padding=8)
    barra_botones.pack(fill=tk.X)
    ttk.Button(barra_botones, text="Buscar", style="Acento.TButton", command=buscar).pack(side=tk.LEFT, padx=4)
    ttk.Button(barra_botones, text="Exportar a Excel", command=exportar).pack(side=tk.LEFT, padx=4)
    ttk.Button(barra_botones, text="Cerrar", command=ventana.destroy).pack(side=tk.LEFT, padx=4)

    buscar()
    centrar_ventana(ventana, 820, 520)
    return ventana


def abrir_anticipos(maestro):
    ventana = tk.Toplevel(maestro)
    ventana.title("Pago de Anticipos")
    ventana.geometry("700x480")
    ventana.configure(bg=COLOR_FONDO)
    ventana.transient(maestro)

    columnas = ["codigo_empleado", "anio", "mes", "fecha_pago", "monto", "observaciones"]
    tabla = TablaInteractiva(ventana, columnas)
    tabla.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

    def cargar():
        filas = mod_liquidacion.listar_anticipos()
        for fila in filas:
            fila["_id"] = fila["id_anticipo"]
        tabla.cargar_datos(filas)

    def nuevo():
        campos = [
            {"nombre": "codigo_empleado", "etiqueta": "Código Empleado", "tipo": "numero", "requerido": True},
            {"nombre": "anio", "etiqueta": "Año", "tipo": "numero", "requerido": True,
             "valor_defecto": datetime.now().year},
            {"nombre": "mes", "etiqueta": "Mes", "tipo": "numero", "requerido": True,
             "valor_defecto": datetime.now().month},
            {"nombre": "fecha_pago", "etiqueta": "Fecha de Pago (YYYY-MM-DD)",
             "valor_defecto": datetime.now().strftime("%Y-%m-%d")},
            {"nombre": "monto", "etiqueta": "Monto ($)", "tipo": "numero", "requerido": True},
            {"nombre": "observaciones", "etiqueta": "Observaciones"},
        ]

        def guardar(datos):
            datos["codigo_empleado"] = int(datos["codigo_empleado"])
            datos["anio"] = int(datos["anio"])
            datos["mes"] = int(datos["mes"])
            mod_liquidacion.registrar_anticipo(datos)
            cargar()

        FormularioModal(ventana, "Nuevo Anticipo", campos, al_guardar=guardar)

    def eliminar():
        seleccion = tabla.obtener_seleccion()
        if not seleccion:
            mostrar_error("Seleccione un registro", "Debe seleccionar un anticipo para eliminar.")
            return
        mod_liquidacion.eliminar_anticipo(seleccion["id_anticipo"])
        cargar()

    barra_botones = ttk.Frame(ventana, padding=8)
    barra_botones.pack(fill=tk.X)
    ttk.Button(barra_botones, text="Nuevo Anticipo", style="Acento.TButton", command=nuevo).pack(
        side=tk.LEFT, padx=4
    )
    ttk.Button(barra_botones, text="Eliminar", command=eliminar).pack(side=tk.LEFT, padx=4)
    ttk.Button(barra_botones, text="Cerrar", command=ventana.destroy).pack(side=tk.LEFT, padx=4)

    cargar()
    centrar_ventana(ventana, 700, 480)
    return ventana
