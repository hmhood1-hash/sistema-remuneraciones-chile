# -*- coding: utf-8 -*-
"""
Gestión de la ruta y conexión a la base de datos SQLite.

Compatible con Windows (guarda la base de datos en
``%LOCALAPPDATA%\\SistemaRemuneraciones``) y con otros sistemas operativos
(usa una carpeta equivalente dentro del directorio del usuario), para poder
ejecutar y probar el sistema también en entornos de desarrollo Linux/Mac.
"""
import os
import sqlite3
from contextlib import contextmanager

APP_FOLDER_NAME = "SistemaRemuneraciones"
DB_FILE_NAME = "remuneraciones.db"


def obtener_directorio_datos():
    """Devuelve (y crea si no existe) la carpeta donde se guarda la BD.

    En Windows utiliza ``%LOCALAPPDATA%`` (equivalente a
    ``C:\\Users\\<usuario>\\AppData\\Local``). En otros sistemas operativos
    usa ``~/.local/share`` como alternativa razonable.
    """
    local_app_data = os.environ.get("LOCALAPPDATA")
    if local_app_data:
        base_dir = local_app_data
    elif os.name == "nt":
        base_dir = os.path.expanduser(os.path.join("~", "AppData", "Local"))
    else:
        base_dir = os.environ.get(
            "XDG_DATA_HOME", os.path.expanduser(os.path.join("~", ".local", "share"))
        )

    directorio = os.path.join(base_dir, APP_FOLDER_NAME)
    os.makedirs(directorio, exist_ok=True)
    return directorio


def obtener_ruta_base_datos():
    """Devuelve la ruta completa (compatible con el SO) del archivo SQLite."""
    return os.path.join(obtener_directorio_datos(), DB_FILE_NAME)


def obtener_conexion(ruta_bd=None):
    """Crea una conexión SQLite con soporte de claves foráneas y UTF-8."""
    ruta = ruta_bd or obtener_ruta_base_datos()
    conexion = sqlite3.connect(ruta)
    conexion.execute("PRAGMA foreign_keys = ON")
    conexion.row_factory = sqlite3.Row
    return conexion


@contextmanager
def conexion_bd(ruta_bd=None):
    """Context manager que entrega una conexión y hace commit/close al salir."""
    conexion = obtener_conexion(ruta_bd)
    try:
        yield conexion
        conexion.commit()
    except Exception:
        conexion.rollback()
        raise
    finally:
        conexion.close()
