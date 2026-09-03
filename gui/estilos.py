"""
Estilos y temas profesionales para la GUI
"""
import tkinter as tk
from tkinter import font

# Colores suaves y profesionales
COLORES = {
    'fondo_principal': '#f0f2f5',      # Gris claro
    'fondo_secundario': '#ffffff',      # Blanco
    'texto_principal': '#1c1e21',       # Gris oscuro
    'texto_secundario': '#65676b',      # Gris medio
    'azul_primario': '#0a66c2',         # Azul profesional
    'azul_hover': '#054399',            # Azul oscuro
    'verde_exito': '#31a24c',           # Verde suave
    'rojo_error': '#d62828',            # Rojo suave
    'borde': '#e4e6eb',                 # Borde gris claro
    'sidebar': '#e7f3ff',               # Azul muy claro
}

# Fuentes
FUENTES = {
    'titulo': ('Segoe UI', 16, 'bold'),
    'subtitulo': ('Segoe UI', 12, 'bold'),
    'normal': ('Segoe UI', 10),
    'pequeño': ('Segoe UI', 9),
    'mono': ('Courier New', 10),
}

def aplicar_estilo_boton(boton, estilo='primario'):
    """
    Aplica estilo a un botón
    """
    if estilo == 'primario':
        boton.config(
            bg=COLORES['azul_primario'],
            fg='white',
            font=FUENTES['normal'],
            relief=tk.FLAT,
            cursor='hand2',
            padx=20,
            pady=10,
            activebackground=COLORES['azul_hover'],
            activeforeground='white'
        )
    elif estilo == 'secundario':
        boton.config(
            bg=COLORES['fondo_secundario'],
            fg=COLORES['azul_primario'],
            font=FUENTES['normal'],
            relief=tk.SOLID,
            borderwidth=1,
            cursor='hand2',
            padx=20,
            pady=10,
            activebackground=COLORES['sidebar'],
            activeforeground=COLORES['azul_primario']
        )
    elif estilo == 'exito':
        boton.config(
            bg=COLORES['verde_exito'],
            fg='white',
            font=FUENTES['normal'],
            relief=tk.FLAT,
            cursor='hand2',
            padx=20,
            pady=10
        )
    elif estilo == 'peligro':
        boton.config(
            bg=COLORES['rojo_error'],
            fg='white',
            font=FUENTES['normal'],
            relief=tk.FLAT,
            cursor='hand2',
            padx=20,
            pady=10
        )

def aplicar_estilo_entrada(entrada):
    """
    Aplica estilo a un campo de entrada
    """
    entrada.config(
        bg=COLORES['fondo_secundario'],
        fg=COLORES['texto_principal'],
        font=FUENTES['normal'],
        relief=tk.SOLID,
        borderwidth=1,
        insertbackground=COLORES['azul_primario']
    )
