"""
Widgets personalizados reutilizables
"""
import tkinter as tk
from tkinter import ttk
from gui.estilos import COLORES, FUENTES, aplicar_estilo_entrada

class TablaDatos(ttk.Frame):
    """
    Tabla interactiva con scroll
    """
    def __init__(self, parent, columnas, datos=None):
        super().__init__(parent)
        self.columnas = columnas
        self.datos = datos or []
        
        # Crear Treeview
        self.tree = ttk.Treeview(
            self,
            columns=columnas,
            height=15,
            show='headings'
        )
        
        # Configurar columnas
        for col in columnas:
            self.tree.column(col, width=150, anchor='w')
            self.tree.heading(col, text=col)
        
        # Scrollbars
        vsb = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        hsb = ttk.Scrollbar(self, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscroll=vsb.set, xscroll=hsb.set)
        
        # Grid layout
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        
        # Cargar datos
        self.cargar_datos(datos)
    
    def cargar_datos(self, datos):
        """
        Carga datos en la tabla
        """
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Agregar datos
        if datos:
            for fila in datos:
                valores = [fila.get(col, '') if isinstance(fila, dict) else fila[self.columnas.index(col)] 
                          for col in self.columnas]
                self.tree.insert('', 'end', values=valores)
    
    def obtener_seleccion(self):
        """
        Obtiene la fila seleccionada
        """
        seleccion = self.tree.selection()
        if seleccion:
            item = seleccion[0]
            valores = self.tree.item(item)['values']
            return {col: val for col, val in zip(self.columnas, valores)}
        return None


class CampoFormulario(ttk.Frame):
    """
    Campo de formulario con etiqueta y validación
    """
    def __init__(self, parent, etiqueta, tipo='texto', obligatorio=False):
        super().__init__(parent)
        self.tipo = tipo
        self.obligatorio = obligatorio
        self.valor = tk.StringVar()
        
        # Etiqueta
        lbl = ttk.Label(self, text=etiqueta, font=FUENTES['normal'])
        lbl.pack(anchor='w', pady=(5, 2))
        
        # Campo de entrada
        self.entrada = ttk.Entry(self, textvariable=self.valor)
        self.entrada.pack(fill='x', padx=0, pady=(0, 5))
        aplicar_estilo_entrada(self.entrada)
        
        # Etiqueta de error
        self.lbl_error = ttk.Label(self, text='', foreground=COLORES['rojo_error'])
        self.lbl_error.pack(anchor='w')
    
    def obtener_valor(self):
        """
        Obtiene el valor del campo
        """
        return self.valor.get().strip()
    
    def establecer_valor(self, valor):
        """
        Establece el valor del campo
        """
        self.valor.set(str(valor))
    
    def validar(self):
        """
        Valida el campo
        """
        if self.obligatorio and not self.obtener_valor():
            self.lbl_error.config(text='Este campo es obligatorio')
            return False
        
        self.lbl_error.config(text='')
        return True


class BarraEstado(ttk.Frame):
    """
    Barra de estado con progreso
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.config(relief='sunken', height=30)
        
        # Etiqueta de estado
        self.lbl_estado = ttk.Label(self, text='Listo')
        self.lbl_estado.pack(side='left', padx=10, pady=5)
        
        # Barra de progreso
        self.progreso = ttk.Progressbar(self, mode='indeterminate')
        self.progreso.pack(side='right', padx=10, pady=5, fill='x', expand=True)
    
    def actualizar_estado(self, mensaje):
        """
        Actualiza el mensaje de estado
        """
        self.lbl_estado.config(text=mensaje)
        self.update_idletasks()
    
    def iniciar_progreso(self):
        """
        Inicia la barra de progreso
        """
        self.progreso.start()
    
    def detener_progreso(self):
        """
        Detiene la barra de progreso
        """
        self.progreso.stop()
