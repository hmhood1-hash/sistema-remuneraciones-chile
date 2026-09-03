"""
Tema visual y colores profesionales para la interfaz gráfica.
"""
import tkinter as tk
from tkinter import ttk

# Paleta de colores (azul corporativo / gris)
COLOR_PRIMARIO = "#1a5276"        # Azul oscuro (encabezados, menú)
COLOR_PRIMARIO_CLARO = "#2874a6"  # Azul medio (botones)
COLOR_PRIMARIO_HOVER = "#21618c"  # Azul hover
COLOR_SECUNDARIO = "#eaeded"      # Gris claro (fondo panel)
COLOR_FONDO = "#f4f6f7"           # Fondo general
COLOR_BLANCO = "#ffffff"
COLOR_TEXTO = "#1c2833"
COLOR_TEXTO_CLARO = "#ffffff"
COLOR_EXITO = "#1e8449"
COLOR_ERROR = "#b03a2e"
COLOR_ADVERTENCIA = "#ca6f1e"
COLOR_BORDE = "#ccd1d1"

FUENTE_BASE = ("Segoe UI", 10)
FUENTE_TITULO = ("Segoe UI", 14, "bold")
FUENTE_SUBTITULO = ("Segoe UI", 11, "bold")
FUENTE_TABLA = ("Segoe UI", 9)
FUENTE_TABLA_ENCABEZADO = ("Segoe UI", 9, "bold")


def aplicar_estilo(root):
    """
    Configura el tema ttk profesional para toda la aplicación.

    Args:
        root: instancia de tk.Tk sobre la que se aplica el estilo.
    """
    root.configure(bg=COLOR_FONDO)

    estilo = ttk.Style(root)
    try:
        estilo.theme_use("clam")
    except tk.TclError:
        pass

    estilo.configure(".", font=FUENTE_BASE, background=COLOR_FONDO)

    # Botones
    estilo.configure(
        "Primario.TButton",
        background=COLOR_PRIMARIO_CLARO,
        foreground=COLOR_TEXTO_CLARO,
        padding=(12, 6),
        font=FUENTE_BASE,
        borderwidth=0,
    )
    estilo.map(
        "Primario.TButton",
        background=[("active", COLOR_PRIMARIO_HOVER), ("disabled", COLOR_BORDE)],
    )

    estilo.configure(
        "Secundario.TButton",
        background=COLOR_SECUNDARIO,
        foreground=COLOR_TEXTO,
        padding=(12, 6),
        font=FUENTE_BASE,
        borderwidth=1,
    )
    estilo.map("Secundario.TButton", background=[("active", "#d5dbdb")])

    estilo.configure(
        "Peligro.TButton",
        background=COLOR_ERROR,
        foreground=COLOR_TEXTO_CLARO,
        padding=(12, 6),
        font=FUENTE_BASE,
        borderwidth=0,
    )
    estilo.map("Peligro.TButton", background=[("active", "#922b21")])

    # Barra lateral
    estilo.configure("Sidebar.TFrame", background=COLOR_PRIMARIO)
    estilo.configure(
        "Sidebar.TButton",
        background=COLOR_PRIMARIO,
        foreground=COLOR_TEXTO_CLARO,
        anchor="w",
        padding=(16, 10),
        font=FUENTE_BASE,
        borderwidth=0,
    )
    estilo.map(
        "Sidebar.TButton",
        background=[("active", COLOR_PRIMARIO_HOVER)],
        foreground=[("active", COLOR_TEXTO_CLARO)],
    )

    # Contenedores
    estilo.configure("Contenido.TFrame", background=COLOR_FONDO)
    estilo.configure("Tarjeta.TFrame", background=COLOR_BLANCO, relief="flat")
    estilo.configure("Titulo.TLabel", background=COLOR_FONDO, foreground=COLOR_PRIMARIO, font=FUENTE_TITULO)
    estilo.configure("Subtitulo.TLabel", background=COLOR_BLANCO, foreground=COLOR_TEXTO, font=FUENTE_SUBTITULO)
    estilo.configure("Texto.TLabel", background=COLOR_BLANCO, foreground=COLOR_TEXTO, font=FUENTE_BASE)
    estilo.configure("TextoFondo.TLabel", background=COLOR_FONDO, foreground=COLOR_TEXTO, font=FUENTE_BASE)

    # Tabla (Treeview)
    estilo.configure(
        "Tabla.Treeview",
        background=COLOR_BLANCO,
        fieldbackground=COLOR_BLANCO,
        foreground=COLOR_TEXTO,
        rowheight=26,
        font=FUENTE_TABLA,
        borderwidth=1,
    )
    estilo.configure(
        "Tabla.Treeview.Heading",
        background=COLOR_PRIMARIO,
        foreground=COLOR_TEXTO_CLARO,
        font=FUENTE_TABLA_ENCABEZADO,
        relief="flat",
    )
    estilo.map("Tabla.Treeview.Heading", background=[("active", COLOR_PRIMARIO_HOVER)])
    estilo.map("Tabla.Treeview", background=[("selected", COLOR_PRIMARIO_CLARO)], foreground=[("selected", COLOR_TEXTO_CLARO)])

    # Barra de estado
    estilo.configure("Estado.TFrame", background=COLOR_SECUNDARIO)
    estilo.configure("Estado.TLabel", background=COLOR_SECUNDARIO, foreground=COLOR_TEXTO, font=("Segoe UI", 9))

    # Barra de herramientas
    estilo.configure("Toolbar.TFrame", background=COLOR_BLANCO)

    # Entradas / Combobox
    estilo.configure("TEntry", padding=4)
    estilo.configure("TCombobox", padding=4)

    return estilo
