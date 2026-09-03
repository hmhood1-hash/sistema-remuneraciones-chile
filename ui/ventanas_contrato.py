# -*- coding: utf-8 -*-
"""Ventanas de gestión de Contratos y Finiquitos."""
import tkinter as tk
from datetime import datetime
from tkinter import ttk

from modules import trabajador as mod_trabajador
from modules import contrato as mod_contrato
from modules import finiquito as mod_finiquito
from modules import parametros as mod_parametros

from ui.estilos import COLOR_FONDO
from ui.tablas import TablaInteractiva
from ui.utils import centrar_ventana, mostrar_info, mostrar_error


def _opciones_trabajadores():
    return [
        "{} - {} {}".format(t["codigo_empleado"], t["nombres"], t["apellido_paterno"])
        for t in mod_trabajador.listar_trabajadores()
    ]


def abrir_contrato(maestro):
    ventana = tk.Toplevel(maestro)
    ventana.title("Contrato de Trabajo")
    ventana.geometry("640x560")
    ventana.configure(bg=COLOR_FONDO)
    ventana.transient(maestro)

    marco = ttk.Frame(ventana, padding=12)
    marco.pack(fill=tk.BOTH, expand=True)

    tipos_contrato = [t["codigo"] for t in mod_parametros.listar_tipos_contrato()]

    ttk.Label(marco, text="Trabajador:").grid(row=0, column=0, sticky=tk.W, padx=4, pady=4)
    var_trabajador = tk.StringVar()
    ttk.Combobox(marco, textvariable=var_trabajador, values=_opciones_trabajadores(),
                 state="readonly", width=35).grid(row=0, column=1, padx=4, pady=4)

    campos = [
        ("nacionalidad", "Nacionalidad"),
        ("labor_ejecutar", "Labor a Ejecutar"),
        ("establecimiento", "Establecimiento"),
        ("horarios", "Horarios"),
        ("duracion_contrato", "Duración del Contrato"),
    ]
    variables = {}
    for fila, (nombre, etiqueta) in enumerate(campos, start=1):
        ttk.Label(marco, text=etiqueta + ":").grid(row=fila, column=0, sticky=tk.W, padx=4, pady=4)
        variable = tk.StringVar()
        ttk.Entry(marco, textvariable=variable, width=32).grid(row=fila, column=1, padx=4, pady=4)
        variables[nombre] = variable

    fila_actual = len(campos) + 1
    ttk.Label(marco, text="Tipo de Contrato:").grid(row=fila_actual, column=0, sticky=tk.W, padx=4, pady=4)
    var_tipo_contrato = tk.StringVar()
    ttk.Combobox(marco, textvariable=var_tipo_contrato, values=tipos_contrato, state="readonly",
                 width=32).grid(row=fila_actual, column=1, padx=4, pady=4)

    fila_actual += 1
    ttk.Label(marco, text="Pago:").grid(row=fila_actual, column=0, sticky=tk.W, padx=4, pady=4)
    var_pago = tk.StringVar(value="Mensual")
    ttk.Combobox(marco, textvariable=var_pago, values=["Mensual", "Quincenal", "Diario"], state="readonly",
                 width=32).grid(row=fila_actual, column=1, padx=4, pady=4)

    campos_montos = [
        ("sueldo_base", "Sueldo Base"),
        ("movilizacion", "Movilización"),
        ("colacion", "Colación"),
        ("gratificacion", "Gratificación"),
        ("remuneracion_adicional", "Remuneración Adicional"),
    ]
    variables_montos = {}
    for indice, (nombre, etiqueta) in enumerate(campos_montos):
        fila_actual += 1
        ttk.Label(marco, text=etiqueta + " ($):").grid(row=fila_actual, column=0, sticky=tk.W, padx=4, pady=4)
        variable = tk.StringVar(value="0")
        ttk.Entry(marco, textvariable=variable, width=32).grid(row=fila_actual, column=1, padx=4, pady=4)
        variables_montos[nombre] = variable

    def guardar():
        if not var_trabajador.get():
            mostrar_error("Trabajador requerido", "Debe seleccionar un trabajador.")
            return
        codigo_empleado = int(var_trabajador.get().split(" - ")[0])
        datos = {"codigo_empleado": codigo_empleado, "codigo_tipo_contrato": var_tipo_contrato.get(),
                 "pago": var_pago.get()}
        for nombre in variables:
            datos[nombre] = variables[nombre].get()
        for nombre in variables_montos:
            try:
                datos[nombre] = float(variables_montos[nombre].get() or 0)
            except ValueError:
                mostrar_error("Dato inválido", "Los montos deben ser numéricos.")
                return
        mod_contrato.crear_contrato(datos)
        mostrar_info("Contrato guardado", "El contrato se guardó correctamente.")

    barra_botones = ttk.Frame(ventana, padding=8)
    barra_botones.pack(fill=tk.X)
    ttk.Button(barra_botones, text="Guardar", style="Acento.TButton", command=guardar).pack(side=tk.LEFT, padx=4)
    ttk.Button(barra_botones, text="Cerrar", command=ventana.destroy).pack(side=tk.LEFT, padx=4)

    centrar_ventana(ventana, 640, 560)
    return ventana


def abrir_finiquito(maestro):
    ventana = tk.Toplevel(maestro)
    ventana.title("Finiquito")
    ventana.geometry("620x460")
    ventana.configure(bg=COLOR_FONDO)
    ventana.transient(maestro)

    marco = ttk.Frame(ventana, padding=12)
    marco.pack(fill=tk.BOTH, expand=True)

    causales = [c["codigo"] for c in mod_parametros.listar_causales_finiquito()]

    ttk.Label(marco, text="Trabajador:").grid(row=0, column=0, sticky=tk.W, padx=4, pady=4)
    var_trabajador = tk.StringVar()
    ttk.Combobox(marco, textvariable=var_trabajador, values=_opciones_trabajadores(), state="readonly",
                 width=35).grid(row=0, column=1, padx=4, pady=4)

    ttk.Label(marco, text="Fecha Inicio (YYYY-MM-DD):").grid(row=1, column=0, sticky=tk.W, padx=4, pady=4)
    var_fecha_inicio = tk.StringVar()
    ttk.Entry(marco, textvariable=var_fecha_inicio, width=20).grid(row=1, column=1, sticky=tk.W, padx=4, pady=4)

    ttk.Label(marco, text="Fecha Término (YYYY-MM-DD):").grid(row=2, column=0, sticky=tk.W, padx=4, pady=4)
    var_fecha_termino = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
    ttk.Entry(marco, textvariable=var_fecha_termino, width=20).grid(row=2, column=1, sticky=tk.W, padx=4, pady=4)

    ttk.Label(marco, text="Cargo:").grid(row=3, column=0, sticky=tk.W, padx=4, pady=4)
    var_cargo = tk.StringVar()
    ttk.Entry(marco, textvariable=var_cargo, width=32).grid(row=3, column=1, padx=4, pady=4)

    ttk.Label(marco, text="Causal de Despido:").grid(row=4, column=0, sticky=tk.W, padx=4, pady=4)
    var_causal = tk.StringVar()
    ttk.Combobox(marco, textvariable=var_causal, values=causales, state="readonly", width=32).grid(
        row=4, column=1, padx=4, pady=4
    )

    ttk.Label(marco, text="Días Vacaciones Pendientes:").grid(row=5, column=0, sticky=tk.W, padx=4, pady=4)
    var_dias_vacaciones = tk.StringVar(value="0")
    ttk.Entry(marco, textvariable=var_dias_vacaciones, width=10).grid(row=5, column=1, sticky=tk.W, padx=4, pady=4)

    texto_resultado = tk.Text(marco, height=10, width=60, state="disabled")
    texto_resultado.grid(row=6, column=0, columnspan=2, pady=12)

    resultado_actual = {}

    def calcular():
        if not var_trabajador.get():
            mostrar_error("Trabajador requerido", "Debe seleccionar un trabajador.")
            return
        codigo_empleado = int(var_trabajador.get().split(" - ")[0])
        trabajador = mod_trabajador.obtener_trabajador(codigo_empleado)
        try:
            dias_vacaciones = float(var_dias_vacaciones.get() or 0)
            resultado = mod_finiquito.calcular_finiquito(
                trabajador["sueldo_base"] or 0, var_fecha_inicio.get() or trabajador.get("fecha_contrato"),
                var_fecha_termino.get(), var_causal.get(), dias_vacaciones,
            )
        except Exception as error:  # noqa: BLE001
            mostrar_error("Error de cálculo", str(error))
            return

        resultado_actual["datos"] = {
            "codigo_empleado": codigo_empleado,
            "fecha_inicio": var_fecha_inicio.get() or trabajador.get("fecha_contrato"),
            "fecha_termino": var_fecha_termino.get(),
            "cargo": var_cargo.get(),
            "codigo_causal": var_causal.get(),
        }
        resultado_actual["monto_total"] = resultado["monto_total"]

        texto_resultado.configure(state="normal")
        texto_resultado.delete("1.0", tk.END)
        texto_resultado.insert(tk.END, "\n".join([
            "Años de Servicio: {}".format(resultado["anios_servicio"]),
            "Indemnización Años de Servicio: {:,.0f}".format(resultado["indemnizacion_anos_servicio"]),
            "Indemnización Aviso Previo: {:,.0f}".format(resultado["indemnizacion_aviso_previo"]),
            "Vacaciones Proporcionales: {:,.0f}".format(resultado["vacaciones_proporcionales"]),
            "MONTO TOTAL FINIQUITO: {:,.0f}".format(resultado["monto_total"]),
        ]))
        texto_resultado.configure(state="disabled")

    def guardar():
        if "datos" not in resultado_actual:
            mostrar_error("Sin cálculo", "Primero debe calcular el finiquito.")
            return
        mod_finiquito.crear_finiquito(resultado_actual["datos"], resultado_actual["monto_total"])
        mostrar_info("Finiquito guardado", "El finiquito se guardó correctamente.")

    barra_botones = ttk.Frame(ventana, padding=8)
    barra_botones.pack(fill=tk.X)
    ttk.Button(barra_botones, text="Calcular", style="Acento.TButton", command=calcular).pack(side=tk.LEFT, padx=4)
    ttk.Button(barra_botones, text="Guardar", command=guardar).pack(side=tk.LEFT, padx=4)
    ttk.Button(barra_botones, text="Cerrar", command=ventana.destroy).pack(side=tk.LEFT, padx=4)

    centrar_ventana(ventana, 620, 460)
    return ventana
