"""
Módulo de reportes con interfaz gráfica
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from gui.estilos import COLORES, FUENTES, aplicar_estilo_boton
from gui.widgets import TablaDatos
from database.models import fetch_all
import csv


class PanelReportes(ttk.Frame):
    """
    Panel de reportes y exportación
    """
    def __init__(self, parent):
        super().__init__(parent)
        
        # Título
        lbl_titulo = ttk.Label(
            self,
            text='Reportes y Exportación',
            font=FUENTES['titulo']
        )
        lbl_titulo.pack(pady=10)
        
        # Frame filtros
        frame_filtros = ttk.LabelFrame(self, text='Filtros')
        frame_filtros.pack(fill='x', pady=10, padx=10)
        
        ttk.Label(frame_filtros, text='Tipo Reporte:').pack(side='left', padx=5, pady=5)
        self.combo_tipo = ttk.Combobox(
            frame_filtros,
            values=['Liquidaciones', 'Trabajadores', 'Empresas'],
            state='readonly'
        )
        self.combo_tipo.pack(side='left', padx=5, pady=5, fill='x', expand=True)
        
        btn_generar = tk.Button(
            frame_filtros,
            text='Generar',
            command=self._generar_reporte
        )
        aplicar_estilo_boton(btn_generar, 'primario')
        btn_generar.pack(side='left', padx=5, pady=5)
        
        btn_exportar = tk.Button(
            frame_filtros,
            text='Exportar CSV',
            command=self._exportar_csv
        )
        aplicar_estilo_boton(btn_exportar, 'exito')
        btn_exportar.pack(side='left', padx=5, pady=5)
        
        # Frame resultados
        self.frame_resultados = ttk.Frame(self)
        self.frame_resultados.pack(fill='both', expand=True, pady=10, padx=10)
    
    def _generar_reporte(self):
        """
        Genera un reporte
        """
        tipo = self.combo_tipo.get()
        if not tipo:
            messagebox.showwarning('Advertencia', 'Seleccione un tipo de reporte')
            return
        
        # Limpiar frame
        for widget in self.frame_resultados.winfo_children():
            widget.destroy()
        
        if tipo == 'Liquidaciones':
            liquidaciones = fetch_all('liquidacion')
            if liquidaciones:
                columnas = ['trabajador_rut', 'anio', 'mes', 'sueldo_base', 'sueldo_liquido']
                tabla = TablaDatos(self.frame_resultados, columnas, liquidaciones)
                tabla.pack(fill='both', expand=True)
                self.datos_actuales = liquidaciones
            else:
                ttk.Label(self.frame_resultados, text='Sin liquidaciones').pack()
        
        elif tipo == 'Trabajadores':
            trabajadores = fetch_all('trabajador')
            if trabajadores:
                columnas = ['rut', 'nombre', 'ap_paterno', 'correo']
                tabla = TablaDatos(self.frame_resultados, columnas, trabajadores)
                tabla.pack(fill='both', expand=True)
                self.datos_actuales = trabajadores
            else:
                ttk.Label(self.frame_resultados, text='Sin trabajadores').pack()
        
        elif tipo == 'Empresas':
            empresas = fetch_all('empresa')
            if empresas:
                columnas = ['codigo', 'rut', 'razon_social', 'ciudad']
                tabla = TablaDatos(self.frame_resultados, columnas, empresas)
                tabla.pack(fill='both', expand=True)
                self.datos_actuales = empresas
            else:
                ttk.Label(self.frame_resultados, text='Sin empresas').pack()
    
    def _exportar_csv(self):
        """
        Exporta datos a CSV
        """
        if not hasattr(self, 'datos_actuales'):
            messagebox.showwarning('Advertencia', 'Genere un reporte primero')
            return
        
        archivo = filedialog.asksaveasfilename(
            defaultextension='.csv',
            filetypes=[('CSV files', '*.csv'), ('All files', '*.*')]
        )
        
        if archivo:
            try:
                with open(archivo, 'w', newline='', encoding='utf-8') as f:
                    if self.datos_actuales:
                        writer = csv.DictWriter(f, fieldnames=self.datos_actuales[0].keys())
                        writer.writeheader()
                        writer.writerows(self.datos_actuales)
                messagebox.showinfo('Éxito', f'Exportado a {archivo}')
            except Exception as e:
                messagebox.showerror('Error', str(e))
