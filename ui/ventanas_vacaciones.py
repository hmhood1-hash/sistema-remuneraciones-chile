# -*- coding: utf-8 -*-
"""Ventana de Control de Vacaciones."""
import tkinter as tk
from datetime import datetime
from tkinter import ttk

from modules import trabajador as mod_trabajador
from modules import vacaciones as mod_vacaciones

from ui.estilos import COLOR_FONDO
from ui.tablas import TablaInteractiva
from ui.utils import centrar_ventana, mostrar_info, mostrar_error


def _opciones_trabajadores():
    return [
        "{} - {} {}".format(t["codigo_empleado"], t["nombres"], t["apellido_paterno"])
        for t in mod_trabajador.listar_trabajadores()
    ]


def abrir_vacaciones(maestro):
    ventana = tk.Toplevel(maestro)
    ventana.title("Control de Vacaciones")
    ventana.geometry("760x560")
    ventana.configure(bg=COLOR_FONDO)
    ventana.transient(maestro)

    marco_seleccion = ttk.Frame(ventana, padding=8)
    marco_seleccion.pack(fill=tk.X)
    ttk.Label(marco_seleccion, text="Trabajador:").pack(side=tk.LEFT, padx=4)
    var_trabajador = tk.StringVar()
    combo = ttk.Combobox(marco_seleccion, textvariable=var_trabajador, values=_opciones_trabajadores(),
                          state="readonly", width=35)
    combo.pack(side=tk.LEFT, padx=4)

    etiqueta_resumen = ttk.Label(ventana, text="Seleccione un trabajador para ver su resumen de vacaciones.")
    etiqueta_resumen.pack(fill=tk.X, padx=8, pady=4)

    columnas = ["fecha_inicio", "fecha_termino", "dias_habiles", "observaciones"]
    tabla = TablaInteractiva(ventana, columnas)
    tabla.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

    def codigo_empleado_actual():
        if not var_trabajador.get():
            return None
        return int(var_trabajador.get().split(" - ")[0])

    def actualizar():
        codigo_empleado = codigo_empleado_actual()
        if not codigo_empleado:
            return
        trabajador = mod_trabajador.obtener_trabajador(codigo_empleado)
        dias_usados = mod_vacaciones.total_dias_usados(codigo_empleado)
        resumen = mod_vacaciones.calcular_dias_disponibles(
            trabajador.get("fecha_contrato") or datetime.now().strftime("%Y-%m-%d"),
            dias_usados=dias_usados,
        )
        etiqueta_resumen.configure(text=(
            "Años trabajados: {} | Días acumulados: {} | Días usados: {} | Días disponibles: {}"
        ).format(resumen["anios_trabajados"], resumen["dias_acumulados"], resumen["dias_usados"],
                 resumen["dias_disponibles"]))

        filas = mod_vacaciones.listar_vacaciones(codigo_empleado)
        for fila in filas:
            fila["_id"] = fila["id_vacacion"]
        tabla.cargar_datos(filas)

    combo.bind("<<ComboboxSelected>>", lambda e: actualizar())

    def registrar():
        codigo_empleado = codigo_empleado_actual()
        if not codigo_empleado:
            mostrar_error("Seleccione trabajador", "Debe seleccionar un trabajador.")
            return

        ventana_registro = tk.Toplevel(ventana)
        ventana_registro.title("Registrar Vacaciones")
        ventana_registro.configure(bg=COLOR_FONDO)
        marco = ttk.Frame(ventana_registro, padding=12)
        marco.pack(fill=tk.BOTH, expand=True)

        ttk.Label(marco, text="Fecha Inicio (YYYY-MM-DD):").grid(row=0, column=0, sticky=tk.W, padx=4, pady=4)
        var_inicio = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        ttk.Entry(marco, textvariable=var_inicio, width=20).grid(row=0, column=1, padx=4, pady=4)

        ttk.Label(marco, text="Fecha Término (YYYY-MM-DD):").grid(row=1, column=0, sticky=tk.W, padx=4, pady=4)
        var_termino = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        ttk.Entry(marco, textvariable=var_termino, width=20).grid(row=1, column=1, padx=4, pady=4)

        ttk.Label(marco, text="Días Hábiles:").grid(row=2, column=0, sticky=tk.W, padx=4, pady=4)
        var_dias = tk.StringVar(value="0")
        ttk.Entry(marco, textvariable=var_dias, width=10).grid(row=2, column=1, sticky=tk.W, padx=4, pady=4)

        ttk.Label(marco, text="Observaciones:").grid(row=3, column=0, sticky=tk.W, padx=4, pady=4)
        var_obs = tk.StringVar()
        ttk.Entry(marco, textvariable=var_obs, width=32).grid(row=3, column=1, padx=4, pady=4)

        def guardar():
            try:
                dias = float(var_dias.get() or 0)
            except ValueError:
                mostrar_error("Dato inválido", "Los días hábiles deben ser numéricos.")
                return
            mod_vacaciones.registrar_vacaciones({
                "codigo_empleado": codigo_empleado,
                "fecha_inicio": var_inicio.get(),
                "fecha_termino": var_termino.get(),
                "dias_habiles": dias,
                "dias_acumulados_antes": 0,
                "observaciones": var_obs.get(),
            })
            ventana_registro.destroy()
            actualizar()

        ttk.Button(marco, text="Guardar", style="Acento.TButton", command=guardar).grid(
            row=4, column=0, columnspan=2, pady=10
        )
        centrar_ventana(ventana_registro, 380, 220)

    barra_botones = ttk.Frame(ventana, padding=8)
    barra_botones.pack(fill=tk.X)
    ttk.Button(barra_botones, text="Registrar Vacaciones", style="Acento.TButton", command=registrar).pack(
        side=tk.LEFT, padx=4
    )
    ttk.Button(barra_botones, text="Cerrar", command=ventana.destroy).pack(side=tk.LEFT, padx=4)

    centrar_ventana(ventana, 760, 560)
    return ventana
