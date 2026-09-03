"""
Componentes reutilizables de interfaz gráfica: tablas, campos validados,
barra de estado y botones estandarizados.
"""
import tkinter as tk
from tkinter import ttk

from calculos.validaciones import validar_rut, validar_fecha, validar_monto
from gui.estilos import COLOR_ERROR, COLOR_BLANCO


class TablaDatos(ttk.Frame):
    """
    Tabla interactiva (Treeview) con scrollbars horizontal y vertical,
    pensada para mostrar listados de registros (empresas, trabajadores,
    liquidaciones, instituciones previsionales, etc.).
    """

    def __init__(self, parent, columnas, encabezados=None, anchos=None, **kwargs):
        super().__init__(parent, style="Tarjeta.TFrame", **kwargs)
        self.columnas = columnas
        encabezados = encabezados or {}
        anchos = anchos or {}

        self.tree = ttk.Treeview(
            self, columns=columnas, show="headings", style="Tabla.Treeview", selectmode="browse"
        )
        for col in columnas:
            self.tree.heading(col, text=encabezados.get(col, col.replace("_", " ").title()))
            self.tree.column(col, width=anchos.get(col, 120), anchor="w")

        scroll_y = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        scroll_x = ttk.Scrollbar(self, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def cargar_datos(self, registros):
        """
        Limpia y vuelve a cargar la tabla con una lista de diccionarios.
        """
        self.tree.delete(*self.tree.get_children())
        for registro in registros:
            valores = [registro.get(col, "") for col in self.columnas]
            self.tree.insert("", "end", values=valores)

    def fila_seleccionada(self):
        """
        Retorna los valores (tupla) de la fila seleccionada, o None.
        """
        seleccion = self.tree.selection()
        if not seleccion:
            return None
        return self.tree.item(seleccion[0], "values")

    def limpiar(self):
        self.tree.delete(*self.tree.get_children())


class CampoFormulario(ttk.Frame):
    """
    Campo de formulario con etiqueta, entrada y validación en tiempo real.
    Soporta tipos: texto, rut, fecha, monto, entero, opciones (combobox).
    """

    def __init__(self, parent, etiqueta, tipo="texto", obligatorio=True, valores=None, ancho=28, **kwargs):
        super().__init__(parent, style="Tarjeta.TFrame", **kwargs)
        self.tipo = tipo
        self.obligatorio = obligatorio

        texto_etiqueta = etiqueta + (" *" if obligatorio else "")
        self.label = ttk.Label(self, text=texto_etiqueta, style="Texto.TLabel")
        self.label.grid(row=0, column=0, sticky="w", padx=(0, 8), pady=4)

        self.var = tk.StringVar()

        if tipo == "opciones":
            self.widget = ttk.Combobox(self, textvariable=self.var, values=valores or [], width=ancho, state="readonly")
        else:
            self.widget = ttk.Entry(self, textvariable=self.var, width=ancho)

        self.widget.grid(row=0, column=1, sticky="w", pady=4)
        self.error_label = ttk.Label(self, text="", foreground=COLOR_ERROR, background=COLOR_BLANCO, font=("Segoe UI", 8))
        self.error_label.grid(row=1, column=1, sticky="w")

        if tipo != "opciones":
            self.widget.bind("<FocusOut>", lambda e: self.validar())

    def get(self):
        return self.var.get().strip()

    def set(self, valor):
        self.var.set("" if valor is None else str(valor))

    def validar(self):
        """
        Valida el contenido del campo según su tipo. Retorna True/False
        y muestra un mensaje de error bajo el campo si corresponde.
        """
        valor = self.get()

        if not valor:
            if self.obligatorio:
                self._mostrar_error("Campo obligatorio")
                return False
            self._limpiar_error()
            return True

        if self.tipo == "rut" and not validar_rut(valor):
            self._mostrar_error("RUT inválido")
            return False
        if self.tipo == "fecha" and not validar_fecha(valor):
            self._mostrar_error("Use formato DD-MM-YYYY")
            return False
        if self.tipo == "monto" and not validar_monto(valor):
            self._mostrar_error("Monto inválido")
            return False
        if self.tipo == "entero":
            try:
                int(valor)
            except ValueError:
                self._mostrar_error("Debe ser un número entero")
                return False

        self._limpiar_error()
        return True

    def _mostrar_error(self, mensaje):
        self.error_label.configure(text=mensaje)

    def _limpiar_error(self):
        self.error_label.configure(text="")


class BarraEstado(ttk.Frame):
    """
    Barra de estado inferior con mensaje de texto y barra de progreso
    para procesos largos.
    """

    def __init__(self, parent, **kwargs):
        super().__init__(parent, style="Estado.TFrame", **kwargs)
        self.mensaje = tk.StringVar(value="Listo")

        self.label = ttk.Label(self, textvariable=self.mensaje, style="Estado.TLabel")
        self.label.pack(side="left", padx=10, pady=4)

        self.progreso = ttk.Progressbar(self, mode="indeterminate", length=160)
        self.progreso.pack(side="right", padx=10, pady=4)

    def mostrar(self, texto):
        self.mensaje.set(texto)

    def iniciar_progreso(self):
        self.progreso.start(10)

    def detener_progreso(self):
        self.progreso.stop()


def crear_boton(parent, texto, comando, tipo="Primario", **kwargs):
    """
    Crea un botón ttk estilizado.

    Args:
        tipo: "Primario", "Secundario" o "Peligro"
    """
    return ttk.Button(parent, text=texto, command=comando, style=f"{tipo}.TButton", **kwargs)


def crear_boton_barra(parent, texto, icono, comando):
    """
    Crea un botón de barra de herramientas con un ícono (carácter unicode)
    y texto descriptivo.
    """
    return ttk.Button(parent, text=f"{icono}  {texto}", command=comando, style="Secundario.TButton")
