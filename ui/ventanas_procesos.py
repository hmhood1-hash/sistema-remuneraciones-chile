# -*- coding: utf-8 -*-
"""Ventanas de Procesos: Centralización Mensual y Actualización/Respaldo de la Base de Datos."""
import tkinter as tk
from datetime import datetime
from tkinter import ttk

from modules import empresa as mod_empresa
from modules import centralizacion as mod_centralizacion

from ui.estilos import COLOR_FONDO
from ui.utils import centrar_ventana, mostrar_info, mostrar_error


def centralizacion_mensual(maestro):
    ventana = tk.Toplevel(maestro)
    ventana.title("Centralización Mensual")
    ventana.geometry("480x320")
    ventana.configure(bg=COLOR_FONDO)
    ventana.transient(maestro)

    marco = ttk.Frame(ventana, padding=16)
    marco.pack(fill=tk.BOTH, expand=True)

    empresas = mod_empresa.listar_empresas()
    ttk.Label(marco, text="Empresa:").grid(row=0, column=0, sticky=tk.W, padx=4, pady=6)
    var_empresa = tk.StringVar()
    ttk.Combobox(marco, textvariable=var_empresa,
                 values=["{} - {}".format(e["codigo_empresa"], e["razon_social"]) for e in empresas],
                 state="readonly", width=30).grid(row=0, column=1, padx=4, pady=6)

    ttk.Label(marco, text="Año:").grid(row=1, column=0, sticky=tk.W, padx=4, pady=6)
    var_anio = tk.StringVar(value=str(datetime.now().year))
    ttk.Entry(marco, textvariable=var_anio, width=10).grid(row=1, column=1, sticky=tk.W, padx=4, pady=6)

    ttk.Label(marco, text="Mes:").grid(row=2, column=0, sticky=tk.W, padx=4, pady=6)
    var_mes = tk.StringVar(value=str(datetime.now().month))
    ttk.Entry(marco, textvariable=var_mes, width=10).grid(row=2, column=1, sticky=tk.W, padx=4, pady=6)

    texto_resultado = tk.Text(marco, height=6, width=50, state="disabled")
    texto_resultado.grid(row=3, column=0, columnspan=2, pady=12)

    def ejecutar():
        if not var_empresa.get():
            mostrar_error("Empresa requerida", "Debe seleccionar una empresa.")
            return
        codigo_empresa = int(var_empresa.get().split(" - ")[0])
        try:
            anio = int(var_anio.get())
            mes = int(var_mes.get())
        except ValueError:
            mostrar_error("Dato inválido", "Año y mes deben ser numéricos.")
            return

        resultado = mod_centralizacion.centralizacion_mensual(codigo_empresa, anio, mes)
        texto_resultado.configure(state="normal")
        texto_resultado.delete("1.0", tk.END)
        texto_resultado.insert(tk.END, "\n".join([
            "Trabajadores procesados: {}".format(resultado["total_trabajadores"]),
            "Liquidaciones generadas: {}".format(resultado["total_generadas"]),
            "Errores: {}".format(len(resultado["errores"])),
        ]))
        texto_resultado.configure(state="disabled")
        mostrar_info("Centralización completada", "Se generaron {} liquidaciones.".format(
            resultado["total_generadas"]
        ))

    barra = ttk.Frame(ventana, padding=8)
    barra.pack(fill=tk.X)
    ttk.Button(barra, text="Ejecutar Centralización", style="Acento.TButton", command=ejecutar).pack(
        side=tk.LEFT, padx=4
    )
    ttk.Button(barra, text="Cerrar", command=ventana.destroy).pack(side=tk.LEFT, padx=4)

    centrar_ventana(ventana, 480, 320)
    return ventana


def actualizar_bd(maestro):
    ruta = mod_centralizacion.actualizar_base_datos()
    mostrar_info("Base de Datos Actualizada", "La estructura de la base de datos se actualizó en:\n{}".format(ruta))


def respaldar_bd(maestro):
    try:
        ruta = mod_centralizacion.respaldar_base_datos()
        mostrar_info("Respaldo generado", "Se generó un respaldo de la base de datos en:\n{}".format(ruta))
    except Exception as error:  # noqa: BLE001
        mostrar_error("Error al respaldar", str(error))
