# -*- coding: utf-8 -*-
"""Ventana principal del Sistema de Remuneraciones Chile."""
import tkinter as tk
from tkinter import ttk

from ui.estilos import aplicar_tema, COLOR_PRIMARIO, COLOR_TEXTO_CLARO
from ui.menus import construir_menu
from ui.utils import centrar_ventana


class VentanaPrincipal(tk.Tk):
    """Ventana raíz de la aplicación: encabezado, menús y barra de estado."""

    def __init__(self):
        super().__init__()
        self.title("Sistema Profesional de Remuneraciones - Chile")
        self.geometry("1000x650")
        self.minsize(800, 500)

        aplicar_tema(self)
        self._construir_encabezado()
        construir_menu(self)
        self._construir_barra_estado()

        centrar_ventana(self, 1000, 650)

    def _construir_encabezado(self):
        encabezado = ttk.Frame(self, style="Encabezado.TFrame", padding=16)
        encabezado.pack(fill=tk.X)
        ttk.Label(
            encabezado, text="Sistema Profesional de Remuneraciones - Chile",
            style="Encabezado.TLabel",
        ).pack(side=tk.LEFT)

        contenido = ttk.Frame(self, padding=20)
        contenido.pack(fill=tk.BOTH, expand=True)
        ttk.Label(
            contenido,
            text=(
                "Utilice el menú superior para gestionar empresas, trabajadores,\n"
                "instituciones previsionales, parámetros, liquidaciones, contratos,\n"
                "finiquitos, vacaciones e informes."
            ),
            justify=tk.LEFT,
        ).pack(anchor=tk.NW)

    def _construir_barra_estado(self):
        barra = ttk.Frame(self, style="Barra.TFrame", padding=4)
        barra.pack(fill=tk.X, side=tk.BOTTOM)
        tk.Label(barra, text="Listo.", bg=COLOR_PRIMARIO, fg=COLOR_TEXTO_CLARO).pack(side=tk.LEFT, padx=8)


def iniciar_aplicacion():
    app = VentanaPrincipal()
    app.mainloop()
