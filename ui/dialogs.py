# -*- coding: utf-8 -*-
"""Ventanas modales (formularios) y ventana CRUD genérica reutilizable."""
import tkinter as tk
from tkinter import ttk

from ui.estilos import COLOR_FONDO
from ui.tablas import TablaInteractiva
from ui.utils import centrar_ventana, mostrar_error, mostrar_info, confirmar


class FormularioModal(tk.Toplevel):
    """Ventana modal genérica para crear/editar un registro según ``campos``.

    Cada elemento de ``campos`` es un dict:
        nombre: llave del dato (clave del diccionario resultante)
        etiqueta: texto mostrado al usuario
        tipo: "texto" | "numero" | "combo" | "fecha" (por defecto "texto")
        opciones: lista de valores válidos si tipo == "combo"
        solo_lectura: si True, el campo no se puede editar (p.ej. código autogenerado)
    """

    def __init__(self, maestro, titulo, campos, valores_iniciales=None, al_guardar=None):
        super().__init__(maestro)
        self.title(titulo)
        self.configure(bg=COLOR_FONDO)
        self.resizable(False, False)
        self.transient(maestro)
        self.grab_set()

        self.campos = campos
        self.al_guardar = al_guardar
        self.variables = {}
        valores_iniciales = valores_iniciales or {}

        contenedor = ttk.Frame(self, padding=16)
        contenedor.pack(fill=tk.BOTH, expand=True)

        for fila, campo in enumerate(campos):
            ttk.Label(contenedor, text=campo["etiqueta"] + ":").grid(
                row=fila, column=0, sticky=tk.W, padx=4, pady=4
            )
            valor_inicial = valores_iniciales.get(campo["nombre"], campo.get("valor_defecto", ""))
            tipo = campo.get("tipo", "texto")

            if tipo == "combo":
                variable = tk.StringVar(value=str(valor_inicial) if valor_inicial is not None else "")
                widget = ttk.Combobox(
                    contenedor, textvariable=variable, values=campo.get("opciones", []),
                    state="readonly" if not campo.get("editable_combo") else "normal", width=30,
                )
            else:
                variable = tk.StringVar(value=str(valor_inicial) if valor_inicial is not None else "")
                widget = ttk.Entry(contenedor, textvariable=variable, width=32)
                if campo.get("solo_lectura"):
                    widget.configure(state="readonly")

            widget.grid(row=fila, column=1, sticky=tk.W, padx=4, pady=4)
            self.variables[campo["nombre"]] = variable

        botones = ttk.Frame(contenedor)
        botones.grid(row=len(campos), column=0, columnspan=2, pady=(12, 0))
        ttk.Button(botones, text="Guardar", style="Acento.TButton", command=self._guardar).pack(
            side=tk.LEFT, padx=4
        )
        ttk.Button(botones, text="Cancelar", command=self.destroy).pack(side=tk.LEFT, padx=4)

        centrar_ventana(self)

    def _guardar(self):
        datos = {}
        for campo in self.campos:
            nombre = campo["nombre"]
            valor = self.variables[nombre].get()
            if campo.get("tipo") == "numero":
                try:
                    valor = float(valor) if valor not in ("", None) else 0.0
                except ValueError:
                    mostrar_error("Dato inválido", "El campo '{}' debe ser numérico.".format(campo["etiqueta"]))
                    return
            if campo.get("requerido") and not str(valor).strip():
                mostrar_error("Dato requerido", "El campo '{}' es obligatorio.".format(campo["etiqueta"]))
                return
            datos[nombre] = valor

        if self.al_guardar:
            try:
                self.al_guardar(datos)
            except Exception as error:  # noqa: BLE001
                mostrar_error("Error al guardar", str(error))
                return
        self.destroy()


class VentanaCRUD(tk.Toplevel):
    """Ventana con tabla + botones Nuevo/Editar/Eliminar para un catálogo simple."""

    def __init__(self, maestro, titulo, columnas, campos_formulario, funciones,
                 titulos_columnas=None, id_campo="_id"):
        super().__init__(maestro)
        self.title(titulo)
        self.geometry("720x480")
        self.configure(bg=COLOR_FONDO)
        self.transient(maestro)

        self.columnas = columnas
        self.campos_formulario = campos_formulario
        self.funciones = funciones
        self.id_campo = id_campo

        barra = ttk.Frame(self, padding=8)
        barra.pack(fill=tk.X)
        ttk.Button(barra, text="Nuevo", style="Acento.TButton", command=self._nuevo).pack(side=tk.LEFT, padx=4)
        ttk.Button(barra, text="Editar", command=self._editar).pack(side=tk.LEFT, padx=4)
        ttk.Button(barra, text="Eliminar", command=self._eliminar).pack(side=tk.LEFT, padx=4)
        ttk.Button(barra, text="Actualizar Lista", command=self._cargar).pack(side=tk.LEFT, padx=4)

        self.tabla = TablaInteractiva(self, columnas, titulos=titulos_columnas)
        self.tabla.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        self._cargar()
        centrar_ventana(self)

    def _cargar(self):
        filas = self.funciones["listar"]()
        for fila in filas:
            fila["_id"] = fila.get(self.id_campo)
        self.tabla.cargar_datos(filas)

    def _nuevo(self):
        def guardar(datos):
            self.funciones["crear"](datos)
            self._cargar()

        FormularioModal(self, "Nuevo registro", self.campos_formulario, al_guardar=guardar)

    def _editar(self):
        seleccion = self.tabla.obtener_seleccion()
        if not seleccion:
            mostrar_info("Seleccione un registro", "Debe seleccionar un registro para editar.")
            return

        def guardar(datos):
            self.funciones["actualizar"](seleccion[self.id_campo], datos)
            self._cargar()

        FormularioModal(self, "Editar registro", self.campos_formulario, valores_iniciales=seleccion,
                         al_guardar=guardar)

    def _eliminar(self):
        seleccion = self.tabla.obtener_seleccion()
        if not seleccion:
            mostrar_info("Seleccione un registro", "Debe seleccionar un registro para eliminar.")
            return
        if confirmar("Confirmar eliminación", "¿Está seguro de eliminar el registro seleccionado?"):
            self.funciones["eliminar"](seleccion[self.id_campo])
            self._cargar()
