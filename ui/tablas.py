# -*- coding: utf-8 -*-
"""Tabla interactiva genérica (Treeview) con búsqueda y filtros."""
import tkinter as tk
from tkinter import ttk

from ui.estilos import COLOR_FONDO


class TablaInteractiva(ttk.Frame):
    """Widget de tabla con encabezados, scrollbars y filtro de búsqueda en vivo."""

    def __init__(self, maestro, columnas, titulos=None, ancho_columnas=None,
                 al_seleccionar=None, al_doble_click=None, **kwargs):
        super().__init__(maestro, **kwargs)
        self.columnas = columnas
        self.titulos = titulos or {c: c.replace("_", " ").title() for c in columnas}
        self.ancho_columnas = ancho_columnas or {}
        self.al_seleccionar = al_seleccionar
        self.al_doble_click = al_doble_click
        self.datos_completos = []

        self._construir_barra_busqueda()
        self._construir_tabla()

    def _construir_barra_busqueda(self):
        barra = ttk.Frame(self)
        barra.pack(fill=tk.X, padx=4, pady=(4, 0))
        ttk.Label(barra, text="Buscar:").pack(side=tk.LEFT, padx=(0, 4))
        self.variable_busqueda = tk.StringVar()
        self.variable_busqueda.trace_add("write", lambda *_: self._filtrar())
        entrada = ttk.Entry(barra, textvariable=self.variable_busqueda, width=40)
        entrada.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def _construir_tabla(self):
        contenedor = ttk.Frame(self)
        contenedor.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        self.tabla = ttk.Treeview(contenedor, columns=self.columnas, show="headings", selectmode="browse")
        for columna in self.columnas:
            self.tabla.heading(columna, text=self.titulos.get(columna, columna),
                                command=lambda c=columna: self._ordenar_por(c, False))
            self.tabla.column(columna, width=self.ancho_columnas.get(columna, 120), anchor=tk.W)

        scroll_y = ttk.Scrollbar(contenedor, orient=tk.VERTICAL, command=self.tabla.yview)
        scroll_x = ttk.Scrollbar(contenedor, orient=tk.HORIZONTAL, command=self.tabla.xview)
        self.tabla.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        self.tabla.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")
        contenedor.rowconfigure(0, weight=1)
        contenedor.columnconfigure(0, weight=1)

        self.tabla.tag_configure("par", background=COLOR_FONDO)

        if self.al_seleccionar:
            self.tabla.bind("<<TreeviewSelect>>", lambda e: self.al_seleccionar(self.obtener_seleccion()))
        if self.al_doble_click:
            self.tabla.bind("<Double-1>", lambda e: self.al_doble_click(self.obtener_seleccion()))

    def cargar_datos(self, filas):
        """``filas`` es una lista de dicts. Cada dict debe tener las llaves de ``columnas``."""
        self.datos_completos = filas
        self._refrescar(filas)

    def _refrescar(self, filas):
        self.tabla.delete(*self.tabla.get_children())
        for indice, fila in enumerate(filas):
            valores = [fila.get(columna, "") for columna in self.columnas]
            etiqueta = "par" if indice % 2 == 0 else ""
            self.tabla.insert("", tk.END, iid=str(fila.get("_id", indice)), values=valores, tags=(etiqueta,))

    def _filtrar(self):
        texto = self.variable_busqueda.get().strip().lower()
        if not texto:
            self._refrescar(self.datos_completos)
            return
        filtradas = [
            fila for fila in self.datos_completos
            if any(texto in str(fila.get(columna, "")).lower() for columna in self.columnas)
        ]
        self._refrescar(filtradas)

    def _ordenar_por(self, columna, invertir):
        try:
            self.datos_completos.sort(key=lambda f: f.get(columna) or "", reverse=invertir)
        except TypeError:
            self.datos_completos.sort(key=lambda f: str(f.get(columna) or ""), reverse=invertir)
        self._refrescar(self.datos_completos)
        self.tabla.heading(columna, command=lambda: self._ordenar_por(columna, not invertir))

    def obtener_seleccion(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            return None
        iid = seleccion[0]
        for fila in self.datos_completos:
            if str(fila.get("_id")) == iid:
                return fila
        return None
