# -*- coding: utf-8 -*-
"""Funciones auxiliares reutilizables para la interfaz gráfica."""
from tkinter import messagebox


def centrar_ventana(ventana, ancho=None, alto=None):
    """Centra una ventana (Tk o Toplevel) respecto de la pantalla."""
    ventana.update_idletasks()
    ancho = ancho or ventana.winfo_width()
    alto = alto or ventana.winfo_height()
    x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana.winfo_screenheight() // 2) - (alto // 2)
    ventana.geometry("{}x{}+{}+{}".format(ancho, alto, x, y))


def mostrar_info(titulo, mensaje):
    messagebox.showinfo(titulo, mensaje)


def mostrar_error(titulo, mensaje):
    messagebox.showerror(titulo, mensaje)


def mostrar_advertencia(titulo, mensaje):
    messagebox.showwarning(titulo, mensaje)


def confirmar(titulo, mensaje):
    return messagebox.askyesno(titulo, mensaje)


def a_float(valor, por_defecto=0.0):
    try:
        return float(str(valor).replace(".", "").replace(",", ".")) if "," in str(valor) else float(valor)
    except (TypeError, ValueError):
        return por_defecto


def formatear_pesos(monto):
    """Formatea un monto en pesos chilenos: ``$ 1.234.567``."""
    try:
        return "$ {:,.0f}".format(float(monto)).replace(",", ".")
    except (TypeError, ValueError):
        return "$ 0"
