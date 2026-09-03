# -*- coding: utf-8 -*-
"""Ventana de gestión de Empresas (datos maestros)."""
import tkinter as tk
from tkinter import ttk

from modules import empresa as mod_empresa
from ui.estilos import COLOR_FONDO
from ui.tablas import TablaInteractiva
from ui.dialogs import FormularioModal
from ui.utils import centrar_ventana, mostrar_info, confirmar

CAMPOS_EMPRESA = [
    {"nombre": "rut", "etiqueta": "RUT", "requerido": True},
    {"nombre": "razon_social", "etiqueta": "Razón Social", "requerido": True},
    {"nombre": "calle", "etiqueta": "Calle"},
    {"nombre": "numero", "etiqueta": "Número"},
    {"nombre": "depto", "etiqueta": "Depto."},
    {"nombre": "poblacion_villa", "etiqueta": "Población/Villa"},
    {"nombre": "comuna", "etiqueta": "Comuna"},
    {"nombre": "ciudad", "etiqueta": "Ciudad"},
    {"nombre": "region", "etiqueta": "Región"},
    {"nombre": "correo", "etiqueta": "Correo"},
    {"nombre": "fono", "etiqueta": "Fono"},
    {"nombre": "giro_comercial", "etiqueta": "Giro Comercial"},
    {"nombre": "codigo_actividad_economica", "etiqueta": "Código Actividad Económica"},
    {"nombre": "rep_legal_rut", "etiqueta": "RUT Rep. Legal"},
    {"nombre": "rep_legal_nombres", "etiqueta": "Nombres Rep. Legal"},
    {"nombre": "rep_legal_apellido_paterno", "etiqueta": "Apellido Paterno Rep. Legal"},
    {"nombre": "rep_legal_apellido_materno", "etiqueta": "Apellido Materno Rep. Legal"},
]

COLUMNAS = ["codigo_empresa", "rut", "razon_social", "comuna", "region", "fono"]


def abrir_ventana_empresa(maestro):
    ventana = tk.Toplevel(maestro)
    ventana.title("Empresa - Datos Maestros")
    ventana.geometry("820x480")
    ventana.configure(bg=COLOR_FONDO)
    ventana.transient(maestro)

    barra = ttk.Frame(ventana, padding=8)
    barra.pack(fill=tk.X)
    ttk.Button(barra, text="Nueva Empresa", style="Acento.TButton",
               command=lambda: _nueva(ventana, tabla)).pack(side=tk.LEFT, padx=4)
    ttk.Button(barra, text="Editar", command=lambda: _editar(ventana, tabla)).pack(side=tk.LEFT, padx=4)
    ttk.Button(barra, text="Eliminar", command=lambda: _eliminar(tabla)).pack(side=tk.LEFT, padx=4)

    tabla = TablaInteractiva(ventana, COLUMNAS)
    tabla.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
    _cargar(tabla)

    centrar_ventana(ventana)
    return ventana


def _cargar(tabla):
    filas = mod_empresa.listar_empresas()
    for fila in filas:
        fila["_id"] = fila["codigo_empresa"]
    tabla.cargar_datos(filas)


def _nueva(maestro, tabla):
    def guardar(datos):
        mod_empresa.crear_empresa(datos)
        _cargar(tabla)

    FormularioModal(maestro, "Nueva Empresa", CAMPOS_EMPRESA, al_guardar=guardar)


def _editar(maestro, tabla):
    seleccion = tabla.obtener_seleccion()
    if not seleccion:
        mostrar_info("Seleccione una empresa", "Debe seleccionar una empresa para editar.")
        return

    def guardar(datos):
        mod_empresa.actualizar_empresa(seleccion["codigo_empresa"], datos)
        _cargar(tabla)

    FormularioModal(maestro, "Editar Empresa", CAMPOS_EMPRESA, valores_iniciales=seleccion,
                     al_guardar=guardar)


def _eliminar(tabla):
    seleccion = tabla.obtener_seleccion()
    if not seleccion:
        mostrar_info("Seleccione una empresa", "Debe seleccionar una empresa para eliminar.")
        return
    if confirmar("Confirmar eliminación", "¿Eliminar la empresa seleccionada?"):
        mod_empresa.eliminar_empresa(seleccion["codigo_empresa"])
        _cargar(tabla)
