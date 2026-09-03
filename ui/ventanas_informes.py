# -*- coding: utf-8 -*-
"""Ventanas de Informes y Reportes exportables."""
import tkinter as tk
from datetime import datetime
from tkinter import ttk, filedialog

from modules import empresa as mod_empresa
from modules import trabajador as mod_trabajador
from modules import liquidacion as mod_liquidacion
from modules import vacaciones as mod_vacaciones
from reportes import generador_excel, generador_pdf

from ui.estilos import COLOR_FONDO
from ui.tablas import TablaInteractiva
from ui.utils import centrar_ventana, mostrar_info, mostrar_error


def _ventana_base(maestro, titulo, ancho=820, alto=520):
    ventana = tk.Toplevel(maestro)
    ventana.title(titulo)
    ventana.geometry("{}x{}".format(ancho, alto))
    ventana.configure(bg=COLOR_FONDO)
    ventana.transient(maestro)
    return ventana


def libro_remuneraciones(maestro):
    ventana = _ventana_base(maestro, "Libro de Remuneraciones")

    marco_filtro = ttk.Frame(ventana, padding=8)
    marco_filtro.pack(fill=tk.X)
    ttk.Label(marco_filtro, text="Empresa:").pack(side=tk.LEFT, padx=4)
    empresas = mod_empresa.listar_empresas()
    var_empresa = tk.StringVar()
    ttk.Combobox(marco_filtro, textvariable=var_empresa,
                 values=["{} - {}".format(e["codigo_empresa"], e["razon_social"]) for e in empresas],
                 state="readonly", width=30).pack(side=tk.LEFT, padx=4)
    ttk.Label(marco_filtro, text="Año:").pack(side=tk.LEFT, padx=4)
    var_anio = tk.StringVar(value=str(datetime.now().year))
    ttk.Entry(marco_filtro, textvariable=var_anio, width=8).pack(side=tk.LEFT, padx=4)
    ttk.Label(marco_filtro, text="Mes:").pack(side=tk.LEFT, padx=4)
    var_mes = tk.StringVar(value=str(datetime.now().month))
    ttk.Entry(marco_filtro, textvariable=var_mes, width=5).pack(side=tk.LEFT, padx=4)

    columnas = ["codigo_empleado", "anio", "mes", "sueldo_base", "total_ingreso_bruto",
                "total_descuentos_previsionales", "impuesto_unico", "sueldo_liquido", "costo_total_empresa"]
    tabla = TablaInteractiva(ventana, columnas)
    tabla.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

    def buscar():
        codigo_empresa = int(var_empresa.get().split(" - ")[0]) if var_empresa.get() else None
        filas = mod_liquidacion.listar_liquidaciones(
            codigo_empresa, int(var_anio.get()) if var_anio.get() else None,
            int(var_mes.get()) if var_mes.get() else None,
        )
        for fila in filas:
            fila["_id"] = fila["id_liquidacion"]
        tabla.cargar_datos(filas)

    def exportar_excel():
        ruta = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel", "*.xlsx")])
        if ruta:
            generador_excel.exportar_libro_remuneraciones(tabla.datos_completos, ruta)
            mostrar_info("Exportado", "Libro exportado a: {}".format(ruta))

    def exportar_pdf():
        ruta = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf")])
        if ruta:
            encabezados = ["Empleado", "Año", "Mes", "Bruto", "Previsión", "Impuesto", "Líquido", "Costo Empresa"]
            filas = [
                [f["codigo_empleado"], f["anio"], f["mes"], f["total_ingreso_bruto"],
                 f["total_descuentos_previsionales"], f["impuesto_unico"], f["sueldo_liquido"],
                 f["costo_total_empresa"]]
                for f in tabla.datos_completos
            ]
            generador_pdf.exportar_tabla_generica_pdf("Libro de Remuneraciones", encabezados, filas, ruta)
            mostrar_info("Exportado", "Libro exportado a: {}".format(ruta))

    barra = ttk.Frame(ventana, padding=8)
    barra.pack(fill=tk.X)
    ttk.Button(barra, text="Buscar", style="Acento.TButton", command=buscar).pack(side=tk.LEFT, padx=4)
    ttk.Button(barra, text="Exportar Excel", command=exportar_excel).pack(side=tk.LEFT, padx=4)
    ttk.Button(barra, text="Exportar PDF", command=exportar_pdf).pack(side=tk.LEFT, padx=4)
    ttk.Button(barra, text="Cerrar", command=ventana.destroy).pack(side=tk.LEFT, padx=4)

    buscar()
    centrar_ventana(ventana, 820, 520)
    return ventana


def detalle_imposiciones(maestro):
    ventana = _ventana_base(maestro, "Detalle Pago de Imposiciones")
    columnas = ["codigo_empleado", "anio", "mes", "monto_afp", "monto_salud", "monto_seguro_cesantia",
                "total_descuentos_previsionales"]
    tabla = TablaInteractiva(ventana, columnas)
    tabla.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

    filas = mod_liquidacion.listar_liquidaciones()
    for fila in filas:
        fila["_id"] = fila["id_liquidacion"]
    tabla.cargar_datos(filas)

    def exportar():
        ruta = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel", "*.xlsx")])
        if ruta:
            encabezados = ["Código Empleado", "Año", "Mes", "AFP", "Salud", "Seguro Cesantía", "Total"]
            filas_export = [
                [f["codigo_empleado"], f["anio"], f["mes"], f["monto_afp"], f["monto_salud"],
                 f["monto_seguro_cesantia"], f["total_descuentos_previsionales"]]
                for f in tabla.datos_completos
            ]
            generador_excel.exportar_tabla_generica("Detalle Imposiciones", encabezados, filas_export, ruta)
            mostrar_info("Exportado", "Detalle exportado a: {}".format(ruta))

    barra = ttk.Frame(ventana, padding=8)
    barra.pack(fill=tk.X)
    ttk.Button(barra, text="Exportar Excel", style="Acento.TButton", command=exportar).pack(side=tk.LEFT, padx=4)
    ttk.Button(barra, text="Cerrar", command=ventana.destroy).pack(side=tk.LEFT, padx=4)
    centrar_ventana(ventana)
    return ventana


def detalle_anticipos(maestro):
    ventana = _ventana_base(maestro, "Detalle de Anticipos")
    columnas = ["codigo_empleado", "anio", "mes", "fecha_pago", "monto", "observaciones"]
    tabla = TablaInteractiva(ventana, columnas)
    tabla.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

    filas = mod_liquidacion.listar_anticipos()
    for fila in filas:
        fila["_id"] = fila["id_anticipo"]
    tabla.cargar_datos(filas)

    def exportar():
        ruta = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel", "*.xlsx")])
        if ruta:
            generador_excel.exportar_tabla_generica("Detalle Anticipos", columnas, [
                [f.get(c, "") for c in columnas] for f in tabla.datos_completos
            ], ruta)
            mostrar_info("Exportado", "Detalle exportado a: {}".format(ruta))

    barra = ttk.Frame(ventana, padding=8)
    barra.pack(fill=tk.X)
    ttk.Button(barra, text="Exportar Excel", style="Acento.TButton", command=exportar).pack(side=tk.LEFT, padx=4)
    ttk.Button(barra, text="Cerrar", command=ventana.destroy).pack(side=tk.LEFT, padx=4)
    centrar_ventana(ventana)
    return ventana


def ficha_trabajador(maestro):
    ventana = _ventana_base(maestro, "Ficha del Trabajador", 500, 400)
    marco = ttk.Frame(ventana, padding=8)
    marco.pack(fill=tk.X)
    ttk.Label(marco, text="Trabajador:").pack(side=tk.LEFT, padx=4)
    trabajadores = mod_trabajador.listar_trabajadores()
    var_trabajador = tk.StringVar()
    ttk.Combobox(
        marco, textvariable=var_trabajador,
        values=["{} - {} {}".format(t["codigo_empleado"], t["nombres"], t["apellido_paterno"]) for t in trabajadores],
        state="readonly", width=30,
    ).pack(side=tk.LEFT, padx=4)

    texto = tk.Text(ventana, height=18, width=60, state="disabled")
    texto.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

    trabajador_actual = {}

    def mostrar():
        if not var_trabajador.get():
            return
        codigo_empleado = int(var_trabajador.get().split(" - ")[0])
        trabajador = mod_trabajador.obtener_trabajador(codigo_empleado)
        trabajador_actual["datos"] = trabajador
        texto.configure(state="normal")
        texto.delete("1.0", tk.END)
        for campo, valor in trabajador.items():
            texto.insert(tk.END, "{}: {}\n".format(campo, valor))
        texto.configure(state="disabled")

    def exportar():
        if "datos" not in trabajador_actual:
            mostrar_error("Sin datos", "Primero seleccione un trabajador.")
            return
        ruta = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel", "*.xlsx")])
        if ruta:
            generador_excel.exportar_ficha_trabajador(trabajador_actual["datos"], ruta)
            mostrar_info("Exportado", "Ficha exportada a: {}".format(ruta))

    barra = ttk.Frame(ventana, padding=8)
    barra.pack(fill=tk.X)
    ttk.Button(barra, text="Ver Ficha", style="Acento.TButton", command=mostrar).pack(side=tk.LEFT, padx=4)
    ttk.Button(barra, text="Exportar Excel", command=exportar).pack(side=tk.LEFT, padx=4)
    ttk.Button(barra, text="Cerrar", command=ventana.destroy).pack(side=tk.LEFT, padx=4)
    centrar_ventana(ventana, 500, 400)
    return ventana


def informe_vacaciones(maestro):
    ventana = _ventana_base(maestro, "Informe de Vacaciones")
    columnas = ["codigo_empleado", "fecha_inicio", "fecha_termino", "dias_habiles", "observaciones"]
    tabla = TablaInteractiva(ventana, columnas)
    tabla.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

    filas = mod_vacaciones.listar_vacaciones()
    for fila in filas:
        fila["_id"] = fila["id_vacacion"]
    tabla.cargar_datos(filas)

    def exportar():
        ruta = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel", "*.xlsx")])
        if ruta:
            generador_excel.exportar_tabla_generica("Informe Vacaciones", columnas, [
                [f.get(c, "") for c in columnas] for f in tabla.datos_completos
            ], ruta)
            mostrar_info("Exportado", "Informe exportado a: {}".format(ruta))

    barra = ttk.Frame(ventana, padding=8)
    barra.pack(fill=tk.X)
    ttk.Button(barra, text="Exportar Excel", style="Acento.TButton", command=exportar).pack(side=tk.LEFT, padx=4)
    ttk.Button(barra, text="Cerrar", command=ventana.destroy).pack(side=tk.LEFT, padx=4)
    centrar_ventana(ventana)
    return ventana


def certificado_tributario(maestro):
    ventana = _ventana_base(maestro, "Certificado Tributario de Remuneraciones", 520, 420)
    marco = ttk.Frame(ventana, padding=8)
    marco.pack(fill=tk.X)
    ttk.Label(marco, text="Trabajador:").pack(side=tk.LEFT, padx=4)
    trabajadores = mod_trabajador.listar_trabajadores()
    var_trabajador = tk.StringVar()
    ttk.Combobox(
        marco, textvariable=var_trabajador,
        values=["{} - {} {}".format(t["codigo_empleado"], t["nombres"], t["apellido_paterno"]) for t in trabajadores],
        state="readonly", width=30,
    ).pack(side=tk.LEFT, padx=4)
    ttk.Label(marco, text="Año:").pack(side=tk.LEFT, padx=4)
    var_anio = tk.StringVar(value=str(datetime.now().year))
    ttk.Entry(marco, textvariable=var_anio, width=8).pack(side=tk.LEFT, padx=4)

    texto = tk.Text(ventana, height=18, width=60, state="disabled")
    texto.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

    datos_actuales = {}

    def generar():
        if not var_trabajador.get():
            return
        codigo_empleado = int(var_trabajador.get().split(" - ")[0])
        anio = int(var_anio.get())
        liquidaciones = [
            liquidacion for liquidacion in mod_liquidacion.listar_liquidaciones(anio=anio)
            if liquidacion["codigo_empleado"] == codigo_empleado
        ]
        total_bruto = sum(l["total_ingreso_bruto"] for l in liquidaciones)
        total_impuesto = sum(l["impuesto_unico"] for l in liquidaciones)
        total_previsional = sum(l["total_descuentos_previsionales"] for l in liquidaciones)
        datos_actuales["filas"] = liquidaciones
        datos_actuales["encabezados"] = ["Año", "Mes", "Bruto", "Previsional", "Impuesto Único"]
        datos_actuales["tabla"] = [[l["anio"], l["mes"], l["total_ingreso_bruto"],
                                     l["total_descuentos_previsionales"], l["impuesto_unico"]] for l in liquidaciones]

        texto.configure(state="normal")
        texto.delete("1.0", tk.END)
        texto.insert(tk.END, "CERTIFICADO TRIBUTARIO DE REMUNERACIONES - AÑO {}\n\n".format(anio))
        texto.insert(tk.END, "Total Renta Bruta: {:,.0f}\n".format(total_bruto))
        texto.insert(tk.END, "Total Descuentos Previsionales: {:,.0f}\n".format(total_previsional))
        texto.insert(tk.END, "Total Impuesto Único Retenido: {:,.0f}\n".format(total_impuesto))
        texto.configure(state="disabled")

    def exportar():
        if "tabla" not in datos_actuales:
            mostrar_error("Sin datos", "Primero genere el certificado.")
            return
        ruta = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf")])
        if ruta:
            generador_pdf.exportar_tabla_generica_pdf(
                "Certificado Tributario de Remuneraciones", datos_actuales["encabezados"],
                datos_actuales["tabla"], ruta,
            )
            mostrar_info("Exportado", "Certificado exportado a: {}".format(ruta))

    barra = ttk.Frame(ventana, padding=8)
    barra.pack(fill=tk.X)
    ttk.Button(barra, text="Generar", style="Acento.TButton", command=generar).pack(side=tk.LEFT, padx=4)
    ttk.Button(barra, text="Exportar PDF", command=exportar).pack(side=tk.LEFT, padx=4)
    ttk.Button(barra, text="Cerrar", command=ventana.destroy).pack(side=tk.LEFT, padx=4)
    centrar_ventana(ventana, 520, 420)
    return ventana
