"""
Modelo de datos y funciones de acceso a la base de datos SQLite.
"""
import sqlite3
from database.init_db import DB_PATH


def get_connection():
    """Obtiene conexión a la base de datos."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def fetch_all(tabla, filtro=None):
    """Obtiene todos los registros de una tabla.
    Args:
        tabla: Nombre de la tabla
        filtro: Diccionario con condiciones WHERE {columna: valor}
    """
    conn = get_connection()
    cursor = conn.cursor()
    query = f"SELECT * FROM {tabla}"
    params = []
    if filtro:
        conditions = " AND ".join([f"{k}=?" for k in filtro.keys()])
        query += f" WHERE {conditions}"
        params = list(filtro.values())
    cursor.execute(query, params)
    resultados = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return resultados


def fetch_one(tabla, filtro):
    """Obtiene un registro de una tabla.
    Args:
        tabla: Nombre de la tabla
        filtro: Diccionario con condiciones WHERE {columna: valor}
    """
    conn = get_connection()
    cursor = conn.cursor()
    conditions = " AND ".join([f"{k}=?" for k in filtro.keys()])
    query = f"SELECT * FROM {tabla} WHERE {conditions}"
    cursor.execute(query, list(filtro.values()))
    resultado = cursor.fetchone()
    conn.close()
    return dict(resultado) if resultado else None


def insert(tabla, datos):
    """Inserta un registro en una tabla.
    Args:
        tabla: Nombre de la tabla
        datos: Diccionario {columna: valor}
    Returns:
        ID del registro insertado o valor de clave primaria
    """
    conn = get_connection()
    cursor = conn.cursor()
    columnas = list(datos.keys())
    placeholders = ",".join(["?" for _ in columnas])
    query = f"INSERT INTO {tabla} ({','.join(columnas)}) VALUES ({placeholders})"
    cursor.execute(query, list(datos.values()))
    conn.commit()
    ultimo_id = cursor.lastrowid
    conn.close()
    return ultimo_id


def update(tabla, datos, filtro):
    """Actualiza registros en una tabla.
    Args:
        tabla: Nombre de la tabla
        datos: Diccionario {columna: valor} a actualizar
        filtro: Diccionario {columna: valor} con condiciones WHERE
    """
    conn = get_connection()
    cursor = conn.cursor()
    set_clause = ",".join([f"{k}=?" for k in datos.keys()])
    where_clause = " AND ".join([f"{k}=?" for k in filtro.keys()])
    query = f"UPDATE {tabla} SET {set_clause} WHERE {where_clause}"
    values = list(datos.values()) + list(filtro.values())
    cursor.execute(query, values)
    conn.commit()
    conn.close()


def delete(tabla, filtro):
    """Elimina registros de una tabla.
    Args:
        tabla: Nombre de la tabla
        filtro: Diccionario {columna: valor} con condiciones WHERE
    """
    conn = get_connection()
    cursor = conn.cursor()
    where_clause = " AND ".join([f"{k}=?" for k in filtro.keys()])
    query = f"DELETE FROM {tabla} WHERE {where_clause}"
    cursor.execute(query, list(filtro.values()))
    conn.commit()
    conn.close()
