"""
Sistema Profesional de Remuneraciones - Chile
Interfaz Gráfica con tkinter
"""
import tkinter as tk
from tkinter import ttk
from database.init_db import init_database
from gui.main_window import VentanaPrincipal


def iniciar_aplicacion():
    """Inicia la aplicación con interfaz gráfica"""
    # Inicializar base de datos
    conn = init_database()
    conn.close()
    
    # Crear ventana raíz
    root = tk.Tk()
    root.title("Sistema de Remuneraciones - Chile")
    root.geometry("1200x700")
    
    # Crear ventana principal
    app = VentanaPrincipal(root)
    
    # Iniciar mainloop
    root.mainloop()


if __name__ == "__main__":
    iniciar_aplicacion()
