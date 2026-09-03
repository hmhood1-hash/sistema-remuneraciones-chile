# -*- coding: utf-8 -*-
"""Tema visual moderno y colores profesionales para la interfaz Windows."""
from tkinter import ttk

COLOR_PRIMARIO = "#1F3A5F"       # Azul corporativo oscuro
COLOR_SECUNDARIO = "#2E86AB"     # Azul medio
COLOR_ACENTO = "#F2A104"         # Naranjo de acento (botones destacados)
COLOR_FONDO = "#F4F6F8"          # Gris muy claro para fondos
COLOR_FONDO_TABLA = "#FFFFFF"
COLOR_TEXTO = "#1B1B1B"
COLOR_TEXTO_CLARO = "#FFFFFF"
COLOR_EXITO = "#2E7D32"
COLOR_ERROR = "#C62828"
COLOR_FILA_ALTERNA = "#E9EEF3"

FUENTE_BASE = ("Segoe UI", 10)
FUENTE_TITULO = ("Segoe UI", 14, "bold")
FUENTE_ENCABEZADO_TABLA = ("Segoe UI", 10, "bold")


def aplicar_tema(root):
    """Aplica un tema moderno (clam) con colores corporativos a la ventana raíz."""
    estilo = ttk.Style(root)
    try:
        estilo.theme_use("clam")
    except Exception:  # pragma: no cover - algunos entornos no tienen 'clam'
        pass

    root.configure(bg=COLOR_FONDO)

    estilo.configure("TFrame", background=COLOR_FONDO)
    estilo.configure("Encabezado.TFrame", background=COLOR_PRIMARIO)
    estilo.configure(
        "Encabezado.TLabel",
        background=COLOR_PRIMARIO,
        foreground=COLOR_TEXTO_CLARO,
        font=FUENTE_TITULO,
    )
    estilo.configure("TLabel", background=COLOR_FONDO, foreground=COLOR_TEXTO, font=FUENTE_BASE)
    estilo.configure("TButton", font=FUENTE_BASE, padding=6)
    estilo.configure(
        "Acento.TButton", background=COLOR_ACENTO, foreground=COLOR_TEXTO, font=FUENTE_BASE
    )
    estilo.map("Acento.TButton", background=[("active", COLOR_SECUNDARIO)])
    estilo.configure("TEntry", padding=4)
    estilo.configure("TCombobox", padding=4)
    estilo.configure(
        "Treeview",
        background=COLOR_FONDO_TABLA,
        fieldbackground=COLOR_FONDO_TABLA,
        rowheight=24,
        font=FUENTE_BASE,
    )
    estilo.configure("Treeview.Heading", font=FUENTE_ENCABEZADO_TABLA, background=COLOR_SECUNDARIO,
                      foreground=COLOR_TEXTO_CLARO)
    estilo.map("Treeview", background=[("selected", COLOR_SECUNDARIO)],
               foreground=[("selected", COLOR_TEXTO_CLARO)])
    estilo.configure("Barra.TFrame", background=COLOR_PRIMARIO)
    return estilo
