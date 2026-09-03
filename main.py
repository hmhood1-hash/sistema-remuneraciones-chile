"""
Sistema Profesional de Remuneraciones - Chile
Punto de entrada principal con interfaz gráfica tkinter
Versión: 1.0 - Windows Compatible
"""
import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Agregar carpeta raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def crear_gui_fallback(root):
    """
    GUI simple de fallback si hay problemas con imports
    """
    root.title("Sistema de Remuneraciones - Chile")
    root.geometry("900x600")
    root.config(bg="#f0f2f5")
    
    # Frame principal
    frame_main = tk.Frame(root, bg="#f0f2f5")
    frame_main.pack(fill='both', expand=True, padx=20, pady=20)
    
    # Título
    titulo = tk.Label(
        frame_main,
        text="SISTEMA DE REMUNERACIONES - CHILE",
        font=("Segoe UI", 18, "bold"),
        bg="#f0f2f5",
        fg="#0a66c2"
    )
    titulo.pack(pady=20)
    
    # Mensaje
    msg = tk.Label(
        frame_main,
        text="Error: No se pudo cargar la interfaz gráfica.\nVerifique que tenga todas las dependencias instaladas.",
        font=("Segoe UI", 11),
        bg="#f0f2f5",
        fg="#d62828",
        justify='center'
    )
    msg.pack(pady=20)
    
    # Botones
    frame_botones = tk.Frame(frame_main, bg="#f0f2f5")
    frame_botones.pack(pady=20)
    
    btn_reintentar = tk.Button(
        frame_botones,
        text="Reintentar",
        bg="#0a66c2",
        fg="white",
        font=("Segoe UI", 11),
        padx=20,
        pady=10,
        relief='flat',
        cursor='hand2',
        command=lambda: reiniciar_app(root)
    )
    btn_reintentar.pack(side='left', padx=5)
    
    btn_salir = tk.Button(
        frame_botones,
        text="Salir",
        bg="#d62828",
        fg="white",
        font=("Segoe UI", 11),
        padx=20,
        pady=10,
        relief='flat',
        cursor='hand2',
        command=root.quit
    )
    btn_salir.pack(side='left', padx=5)


def reiniciar_app(root):
    """Reinicia la aplicación"""
    root.destroy()
    iniciar_aplicacion()


def iniciar_aplicacion():
    """
    Inicia la aplicación con interfaz gráfica profesional
    """
    try:
        # Crear ventana raíz
        root = tk.Tk()
        root.title("Sistema de Remuneraciones - Chile")
        root.geometry("1200x700")
        root.config(bg="#f0f2f5")
        
        # Icono (si existe)
        try:
            icon_path = os.path.join(os.path.dirname(__file__), "assets", "icon.ico")
            if os.path.exists(icon_path):
                root.iconbitmap(icon_path)
        except:
            pass
        
        # Intentar cargar la base de datos
        try:
            from database.init_db import init_database
            conn = init_database()
            conn.close()
        except Exception as e:
            print(f"Advertencia: Error al inicializar BD: {e}")
            # Continuar de todas formas
        
        # Intentar cargar la ventana principal
        try:
            from gui.main_window import VentanaPrincipal
            app = VentanaPrincipal(root)
        except ImportError as e:
            print(f"Error de importación: {e}")
            crear_gui_fallback(root)
        except Exception as e:
            print(f"Error: {e}")
            messagebox.showerror("Error", f"Error al inicializar la GUI:\n{str(e)}")
            crear_gui_fallback(root)
        
        # Centrar ventana en pantalla
        root.update_idletasks()
        ancho = root.winfo_width()
        alto = root.winfo_height()
        x = (root.winfo_screenwidth() // 2) - (ancho // 2)
        y = (root.winfo_screenheight() // 2) - (alto // 2)
        root.geometry(f"+{x}+{y}")
        
        # Iniciar mainloop
        root.mainloop()
        
    except Exception as e:
        print(f"Error crítico: {e}")
        # Crear ventana de error mínima
        root = tk.Tk()
        root.title("Error")
        root.geometry("400x200")
        
        lbl_error = tk.Label(
            root,
            text=f"Error crítico:\n{str(e)}",
            font=("Arial", 11),
            fg="red"
        )
        lbl_error.pack(padx=20, pady=20)
        
        btn_ok = tk.Button(root, text="OK", command=root.quit, padx=20, pady=10)
        btn_ok.pack(pady=10)
        
        root.mainloop()


if __name__ == "__main__":
    try:
        iniciar_aplicacion()
    except KeyboardInterrupt:
        print("\nAplicación cerrada por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"Error no controlado: {e}")
        sys.exit(1)
