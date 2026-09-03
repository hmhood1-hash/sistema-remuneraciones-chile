# -*- coding: utf-8 -*-
"""Ventanas de gestión de Parámetros, Factores Mensuales y Tablas editables."""
import tkinter as tk
from tkinter import ttk

from modules import parametros as mod_parametros
from ui.estilos import COLOR_FONDO
from ui.utils import centrar_ventana, mostrar_info, mostrar_error

CAMPOS_PARAMETROS = [
    ("sueldo_minimo", "Sueldo Mínimo"),
    ("sueldo_minimo_menor_18_mayor_65", "Sueldo Mínimo Menor 18 / Mayor 65"),
    ("tope_gratificacion_mensual", "Tope Gratificación Mensual"),
    ("tope_imponible_afp_uf", "Tope Imponible AFP (UF)"),
    ("tope_imponible_regimen_antiguo_uf", "Tope Imponible Régimen Antiguo (UF)"),
    ("tope_afc_uf", "Tope AFC (UF)"),
    ("tope_apv_mensual_uf", "Tope APV Mensual (UF)"),
    ("tope_apv_anual_uf", "Tope APV Anual (UF)"),
    ("tope_deposito_convenido_anual_uf", "Tope Depósito Convenido Anual (UF)"),
    ("utm", "UTM"),
    ("uf_afp_isapre", "UF AFP/Isapre"),
    ("uf_regimen_antiguo", "UF Régimen Antiguo"),
    ("aporte_patronal_pct", "Aporte Patronal %"),
    ("aporte_adicional_pct", "Aporte Adicional %"),
    ("factor_sss_pct", "Factor SSS %"),
    ("factor_empart_pct", "Factor Empart %"),
    ("ccaf_pct", "CCAF %"),
    ("salud_pct", "Salud %"),
    ("afp_empleador_pct", "AFP Empleador %"),
    ("sis_empleador_pct", "SIS Empleador %"),
    ("expectativa_vida_pct", "Expectativa de Vida %"),
    ("rentabilidad_protegida_pct", "Rentabilidad Protegida %"),
    ("afc_trabajador_indefinido_pct", "AFC Trabajador Indefinido %"),
    ("afc_empleador_indefinido_pct", "AFC Empleador Indefinido %"),
    ("afc_empleador_plazo_fijo_pct", "AFC Empleador Plazo Fijo %"),
    ("plazo_indefinido_11_anios_pct", "Plazo Indefinido 11 años o más %"),
    ("afc_casa_particular_pct", "AFC Casa Particular %"),
]

MESES = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
]


def abrir_ventana_parametros(maestro):
    ventana = tk.Toplevel(maestro)
    ventana.title("Parámetros del Sistema")
    ventana.geometry("620x640")
    ventana.configure(bg=COLOR_FONDO)
    ventana.transient(maestro)

    contenedor = ttk.Frame(ventana)
    contenedor.pack(fill=tk.BOTH, expand=True)

    canvas = tk.Canvas(contenedor, bg=COLOR_FONDO, highlightthickness=0)
    scrollbar = ttk.Scrollbar(contenedor, orient=tk.VERTICAL, command=canvas.yview)
    marco_scroll = ttk.Frame(canvas, padding=12)

    marco_scroll.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=marco_scroll, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    parametros = mod_parametros.obtener_parametros() or {}
    variables = {}
    for fila, (campo, etiqueta) in enumerate(CAMPOS_PARAMETROS):
        ttk.Label(marco_scroll, text=etiqueta + ":").grid(row=fila, column=0, sticky=tk.W, padx=4, pady=2)
        variable = tk.StringVar(value=str(parametros.get(campo, 0)))
        ttk.Entry(marco_scroll, textvariable=variable, width=20).grid(
            row=fila, column=1, sticky=tk.W, padx=4, pady=2
        )
        variables[campo] = variable

    def guardar():
        datos = {}
        for campo, etiqueta in CAMPOS_PARAMETROS:
            try:
                datos[campo] = float(variables[campo].get())
            except ValueError:
                mostrar_error("Dato inválido", "El campo '{}' debe ser numérico.".format(etiqueta))
                return
        mod_parametros.actualizar_parametros(datos)
        mostrar_info("Parámetros guardados", "Los parámetros se actualizaron correctamente.")

    barra_botones = ttk.Frame(ventana, padding=8)
    barra_botones.pack(fill=tk.X)
    ttk.Button(barra_botones, text="Guardar", style="Acento.TButton", command=guardar).pack(
        side=tk.LEFT, padx=4
    )
    ttk.Button(barra_botones, text="Cerrar", command=ventana.destroy).pack(side=tk.LEFT, padx=4)

    centrar_ventana(ventana, 620, 640)
    return ventana


def abrir_ventana_factores(maestro):
    ventana = tk.Toplevel(maestro)
    ventana.title("Factores Mensuales (UTM / UF)")
    ventana.geometry("520x480")
    ventana.configure(bg=COLOR_FONDO)
    ventana.transient(maestro)

    marco_anio = ttk.Frame(ventana, padding=8)
    marco_anio.pack(fill=tk.X)
    ttk.Label(marco_anio, text="Año:").pack(side=tk.LEFT, padx=4)
    from datetime import datetime
    var_anio = tk.StringVar(value=str(datetime.now().year))
    ttk.Entry(marco_anio, textvariable=var_anio, width=8).pack(side=tk.LEFT, padx=4)

    marco_tabla = ttk.Frame(ventana, padding=8)
    marco_tabla.pack(fill=tk.BOTH, expand=True)

    ttk.Label(marco_tabla, text="Mes").grid(row=0, column=0, padx=4, pady=4)
    ttk.Label(marco_tabla, text="Factor").grid(row=0, column=1, padx=4, pady=4)
    ttk.Label(marco_tabla, text="UTM").grid(row=0, column=2, padx=4, pady=4)
    ttk.Label(marco_tabla, text="UF").grid(row=0, column=3, padx=4, pady=4)

    variables_meses = []

    def cargar():
        anio = int(var_anio.get())
        factores_guardados = {f["mes"]: f for f in mod_parametros.listar_factores_anio(anio)}
        for indice, nombre_mes in enumerate(MESES):
            mes = indice + 1
            datos_mes = factores_guardados.get(mes, {"factor": 1, "utm": 0, "uf": 0})
            if len(variables_meses) <= indice:
                ttk.Label(marco_tabla, text=nombre_mes).grid(row=mes, column=0, sticky=tk.W, padx=4, pady=2)
                v_factor = tk.StringVar()
                v_utm = tk.StringVar()
                v_uf = tk.StringVar()
                ttk.Entry(marco_tabla, textvariable=v_factor, width=8).grid(row=mes, column=1, padx=4, pady=2)
                ttk.Entry(marco_tabla, textvariable=v_utm, width=10).grid(row=mes, column=2, padx=4, pady=2)
                ttk.Entry(marco_tabla, textvariable=v_uf, width=10).grid(row=mes, column=3, padx=4, pady=2)
                variables_meses.append((v_factor, v_utm, v_uf))
            v_factor, v_utm, v_uf = variables_meses[indice]
            v_factor.set(str(datos_mes.get("factor", 1)))
            v_utm.set(str(datos_mes.get("utm", 0)))
            v_uf.set(str(datos_mes.get("uf", 0)))

    def guardar():
        try:
            anio = int(var_anio.get())
        except ValueError:
            mostrar_error("Año inválido", "Ingrese un año válido.")
            return
        for indice, (v_factor, v_utm, v_uf) in enumerate(variables_meses):
            mes = indice + 1
            try:
                mod_parametros.guardar_factor_mensual(
                    anio, mes, float(v_factor.get() or 1), float(v_utm.get() or 0), float(v_uf.get() or 0)
                )
            except ValueError:
                mostrar_error("Dato inválido", "Revise los valores del mes {}.".format(MESES[indice]))
                return
        mostrar_info("Factores guardados", "Los factores mensuales se guardaron correctamente.")

    cargar()
    var_anio.trace_add("write", lambda *_: cargar())

    barra_botones = ttk.Frame(ventana, padding=8)
    barra_botones.pack(fill=tk.X)
    ttk.Button(barra_botones, text="Guardar", style="Acento.TButton", command=guardar).pack(
        side=tk.LEFT, padx=4
    )
    ttk.Button(barra_botones, text="Cerrar", command=ventana.destroy).pack(side=tk.LEFT, padx=4)

    centrar_ventana(ventana, 520, 480)
    return ventana


def abrir_ventana_tramos_carga(maestro):
    ventana = tk.Toplevel(maestro)
    ventana.title("Cargas Familiares - Tramos")
    ventana.geometry("560x300")
    ventana.configure(bg=COLOR_FONDO)
    ventana.transient(maestro)

    marco = ttk.Frame(ventana, padding=12)
    marco.pack(fill=tk.BOTH, expand=True)

    for columna, titulo in enumerate(["Tramo", "Desde", "Hasta", "Valor"]):
        ttk.Label(marco, text=titulo, font=("Segoe UI", 10, "bold")).grid(row=0, column=columna, padx=4, pady=4)

    tramos = mod_parametros.listar_tramos_carga_familiar()
    variables = []
    for fila, tramo in enumerate(tramos, start=1):
        ttk.Label(marco, text="Tramo {}".format(tramo["tramo"])).grid(row=fila, column=0, padx=4, pady=2)
        v_desde = tk.StringVar(value=str(tramo["desde"]))
        v_hasta = tk.StringVar(value=str(tramo["hasta"]) if tramo["hasta"] is not None else "")
        v_valor = tk.StringVar(value=str(tramo["valor"]))
        ttk.Entry(marco, textvariable=v_desde, width=12).grid(row=fila, column=1, padx=4, pady=2)
        ttk.Entry(marco, textvariable=v_hasta, width=12).grid(row=fila, column=2, padx=4, pady=2)
        ttk.Entry(marco, textvariable=v_valor, width=12).grid(row=fila, column=3, padx=4, pady=2)
        variables.append((tramo["tramo"], v_desde, v_hasta, v_valor))

    def guardar():
        for numero_tramo, v_desde, v_hasta, v_valor in variables:
            try:
                datos = {
                    "desde": float(v_desde.get() or 0),
                    "hasta": float(v_hasta.get()) if v_hasta.get() else None,
                    "valor": float(v_valor.get() or 0),
                }
            except ValueError:
                mostrar_error("Dato inválido", "Revise los valores del tramo {}.".format(numero_tramo))
                return
            mod_parametros.actualizar_tramo_carga_familiar(numero_tramo, datos)
        mostrar_info("Tramos guardados", "Los tramos de carga familiar se actualizaron correctamente.")

    barra_botones = ttk.Frame(ventana, padding=8)
    barra_botones.pack(fill=tk.X)
    ttk.Button(barra_botones, text="Guardar", style="Acento.TButton", command=guardar).pack(
        side=tk.LEFT, padx=4
    )
    ttk.Button(barra_botones, text="Cerrar", command=ventana.destroy).pack(side=tk.LEFT, padx=4)

    centrar_ventana(ventana, 560, 300)
    return ventana


def abrir_ventana_impuesto_unico(maestro):
    ventana = tk.Toplevel(maestro)
    ventana.title("Impuesto Único - Tabla Progresiva (en UTM)")
    ventana.geometry("620x420")
    ventana.configure(bg=COLOR_FONDO)
    ventana.transient(maestro)

    marco = ttk.Frame(ventana, padding=12)
    marco.pack(fill=tk.BOTH, expand=True)

    for columna, titulo in enumerate(["Tramo", "Desde (UTM)", "Hasta (UTM)", "Factor", "Rebaja (UTM)"]):
        ttk.Label(marco, text=titulo, font=("Segoe UI", 10, "bold")).grid(row=0, column=columna, padx=4, pady=4)

    tramos = mod_parametros.listar_tramos_impuesto_unico()
    variables = []
    for fila, tramo in enumerate(tramos, start=1):
        ttk.Label(marco, text=str(tramo["tramo"])).grid(row=fila, column=0, padx=4, pady=2)
        v_desde = tk.StringVar(value=str(tramo["desde_utm"]))
        v_hasta = tk.StringVar(value=str(tramo["hasta_utm"]) if tramo["hasta_utm"] is not None else "")
        v_factor = tk.StringVar(value=str(tramo["factor"]))
        v_rebaja = tk.StringVar(value=str(tramo["rebaja_utm"]))
        ttk.Entry(marco, textvariable=v_desde, width=12).grid(row=fila, column=1, padx=4, pady=2)
        ttk.Entry(marco, textvariable=v_hasta, width=12).grid(row=fila, column=2, padx=4, pady=2)
        ttk.Entry(marco, textvariable=v_factor, width=10).grid(row=fila, column=3, padx=4, pady=2)
        ttk.Entry(marco, textvariable=v_rebaja, width=10).grid(row=fila, column=4, padx=4, pady=2)
        variables.append((tramo["tramo"], v_desde, v_hasta, v_factor, v_rebaja))

    def guardar():
        for numero_tramo, v_desde, v_hasta, v_factor, v_rebaja in variables:
            try:
                datos = {
                    "desde_utm": float(v_desde.get() or 0),
                    "hasta_utm": float(v_hasta.get()) if v_hasta.get() else None,
                    "factor": float(v_factor.get() or 0),
                    "rebaja_utm": float(v_rebaja.get() or 0),
                }
            except ValueError:
                mostrar_error("Dato inválido", "Revise los valores del tramo {}.".format(numero_tramo))
                return
            mod_parametros.actualizar_tramo_impuesto_unico(numero_tramo, datos)
        mostrar_info("Tabla actualizada", "La tabla de impuesto único se actualizó correctamente.")

    barra_botones = ttk.Frame(ventana, padding=8)
    barra_botones.pack(fill=tk.X)
    ttk.Button(barra_botones, text="Guardar", style="Acento.TButton", command=guardar).pack(
        side=tk.LEFT, padx=4
    )
    ttk.Button(barra_botones, text="Cerrar", command=ventana.destroy).pack(side=tk.LEFT, padx=4)

    centrar_ventana(ventana, 620, 420)
    return ventana
