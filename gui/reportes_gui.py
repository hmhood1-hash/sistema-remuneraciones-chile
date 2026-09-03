"""
Interfaz gráfica de Informes y Reportes: filtros por período/empresa,
tablas de resultados y exportación a CSV (compatible con Excel).
"""
import csv
import os
import tkinter as tk
from tkinter import ttk, filedialog

from database.models import fetch_all, fetch_one
from gui.widgets import TablaDatos, crear_boton, CampoFormulario
from gui.dialogs import mostrar_error, mostrar_exito, mostrar_info


class PanelReportes(ttk.Frame):
    """
    Panel de reportes con selección de tipo de informe, filtros por
    año/mes/empresa y tabla de resultados exportable a CSV.
    """

    REPORTES = [
        "Libro de Remuneraciones",
        "Detalle Pago de Imposiciones",
        "Resumen Empresa",
    ]

    def __init__(self, parent, barra_estado, **kwargs):
        super().__init__(parent, style="Contenido.TFrame", **kwargs)
        self.barra_estado = barra_estado
        self._columnas_actuales = []
        self._datos_actuales = []

        filtros = ttk.Frame(self, style="Tarjeta.TFrame", padding=12)
        filtros.pack(fill="x", pady=(0, 10))

        self.campo_reporte = CampoFormulario(filtros, "Tipo de Reporte", tipo="opciones", obligatorio=True, valores=self.REPORTES)
        self.campo_empresa = CampoFormulario(filtros, "Código Empresa", tipo="entero", obligatorio=False)
        self.campo_anio = CampoFormulario(filtros, "Año", tipo="entero", obligatorio=True)
        self.campo_mes = CampoFormulario(filtros, "Mes (1-12)", tipo="entero", obligatorio=False)

        self.campo_reporte.grid(row=0, column=0, padx=6, sticky="w")
        self.campo_empresa.grid(row=0, column=1, padx=6, sticky="w")
        self.campo_anio.grid(row=0, column=2, padx=6, sticky="w")
        self.campo_mes.grid(row=0, column=3, padx=6, sticky="w")

        botones = ttk.Frame(self, style="Contenido.TFrame")
        botones.pack(fill="x", pady=(0, 8))
        crear_boton(botones, "Generar Reporte", self._generar_reporte).pack(side="left", padx=4)
        crear_boton(botones, "Exportar a CSV/Excel", self._exportar_csv, tipo="Secundario").pack(side="left", padx=4)

        self.marco_tabla = ttk.Frame(self, style="Contenido.TFrame")
        self.marco_tabla.pack(fill="both", expand=True)
        self.tabla = None

        self.totales_label = ttk.Label(self, text="", style="TextoFondo.TLabel")
        self.totales_label.pack(anchor="w", pady=(8, 0))

    def _mostrar_tabla(self, columnas, registros, encabezados=None):
        if self.tabla is not None:
            self.tabla.destroy()
        self.tabla = TablaDatos(self.marco_tabla, columnas, encabezados=encabezados)
        self.tabla.pack(fill="both", expand=True)
        self.tabla.cargar_datos(registros)
        self._columnas_actuales = columnas
        self._datos_actuales = registros

    def _generar_reporte(self):
        if not self.campo_reporte.validar() or not self.campo_anio.validar():
            mostrar_error("Datos inválidos", "Seleccione el tipo de reporte e ingrese el año.")
            return

        reporte = self.campo_reporte.get()
        anio = int(self.campo_anio.get())
        mes = int(self.campo_mes.get()) if self.campo_mes.get() else None
        empresa_codigo = int(self.campo_empresa.get()) if self.campo_empresa.get() else None

        try:
            if reporte == "Libro de Remuneraciones":
                self._reporte_libro_remuneraciones(anio, mes)
            elif reporte == "Detalle Pago de Imposiciones":
                self._reporte_detalle_imposiciones(anio, mes)
            elif reporte == "Resumen Empresa":
                self._reporte_resumen_empresa(anio, mes, empresa_codigo)
            self.barra_estado.mostrar(f"Reporte '{reporte}' generado")
        except Exception as e:
            mostrar_error("Error al generar reporte", str(e))

    def _filtro_periodo(self, anio, mes):
        filtro = {"anio": anio}
        if mes:
            filtro["mes"] = mes
        return filtro

    def _reporte_libro_remuneraciones(self, anio, mes):
        liquidaciones = fetch_all("liquidacion", self._filtro_periodo(anio, mes))
        columnas = ["trabajador_rut", "anio", "mes", "sueldo_base", "total_haberes", "total_descuentos", "sueldo_liquido"]
        self._mostrar_tabla(columnas, liquidaciones)
        total_haberes = sum(l["total_haberes"] for l in liquidaciones)
        total_descuentos = sum(l["total_descuentos"] for l in liquidaciones)
        total_liquido = sum(l["sueldo_liquido"] for l in liquidaciones)
        self.totales_label.configure(
            text=f"Total Haberes: ${total_haberes:,.0f}   |   Total Descuentos: ${total_descuentos:,.0f}   |   Total Líquido: ${total_liquido:,.0f}"
        )

    def _reporte_detalle_imposiciones(self, anio, mes):
        liquidaciones = fetch_all("liquidacion", self._filtro_periodo(anio, mes))
        columnas = ["trabajador_rut", "anio", "mes", "monto_afp", "monto_salud", "monto_afc", "impuesto_unico"]
        self._mostrar_tabla(columnas, liquidaciones)
        total_afp = sum(l["monto_afp"] for l in liquidaciones)
        total_salud = sum(l["monto_salud"] for l in liquidaciones)
        total_impuesto = sum(l["impuesto_unico"] for l in liquidaciones)
        self.totales_label.configure(
            text=f"Total AFP: ${total_afp:,.0f}   |   Total Salud: ${total_salud:,.0f}   |   Total Impuesto: ${total_impuesto:,.0f}"
        )

    def _reporte_resumen_empresa(self, anio, mes, empresa_codigo):
        filtro = self._filtro_periodo(anio, mes)
        if empresa_codigo:
            filtro["empresa_codigo"] = empresa_codigo
        liquidaciones = fetch_all("liquidacion", filtro)
        columnas = ["trabajador_rut", "empresa_codigo", "anio", "mes", "sueldo_liquido"]
        self._mostrar_tabla(columnas, liquidaciones)
        self.totales_label.configure(
            text=f"Número de Trabajadores: {len(liquidaciones)}   |   Total Líquido: ${sum(l['sueldo_liquido'] for l in liquidaciones):,.0f}"
        )

    def _exportar_csv(self):
        if not self._datos_actuales:
            mostrar_error("Sin datos", "Genere un reporte antes de exportar.")
            return

        ruta = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("Archivo CSV (Excel)", "*.csv")],
            title="Guardar Reporte",
        )
        if not ruta:
            return

        try:
            with open(ruta, "w", newline="", encoding="utf-8-sig") as archivo:
                escritor = csv.DictWriter(archivo, fieldnames=self._columnas_actuales)
                escritor.writeheader()
                for fila in self._datos_actuales:
                    escritor.writerow({col: fila.get(col, "") for col in self._columnas_actuales})
            mostrar_exito("Exportación Exitosa", f"El reporte fue exportado a:\n{os.path.abspath(ruta)}")
        except Exception as e:
            mostrar_error("Error al exportar", str(e))
