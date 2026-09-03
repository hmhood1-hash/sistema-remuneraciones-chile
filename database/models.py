"""
Capa de acceso a datos (DAO) genérica y utilidades comunes para todas las tablas
del sistema de remuneraciones.
"""
from database.init_db import get_connection


def row_to_dict(row):
    if row is None:
        return None
    return dict(row)


def rows_to_list(rows):
    return [dict(r) for r in rows]


def fetch_all(query, params=(), db_path=None):
    conn = get_connection(db_path) if db_path else get_connection()
    try:
        cur = conn.execute(query, params)
        return rows_to_list(cur.fetchall())
    finally:
        conn.close()


def fetch_one(query, params=(), db_path=None):
    conn = get_connection(db_path) if db_path else get_connection()
    try:
        cur = conn.execute(query, params)
        return row_to_dict(cur.fetchone())
    finally:
        conn.close()


def execute(query, params=(), db_path=None):
    """Ejecuta un INSERT/UPDATE/DELETE y retorna el lastrowid."""
    conn = get_connection(db_path) if db_path else get_connection()
    try:
        cur = conn.execute(query, params)
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()


def insert(table, data, db_path=None):
    """Inserta un registro (dict columna->valor) en `table` y retorna el id generado."""
    columns = ", ".join(data.keys())
    placeholders = ", ".join(["?"] * len(data))
    query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
    return execute(query, tuple(data.values()), db_path)


def update(table, data, where, where_params, db_path=None):
    """Actualiza registros de `table` con `data` (dict) usando cláusula `where`."""
    set_clause = ", ".join(f"{col} = ?" for col in data.keys())
    query = f"UPDATE {table} SET {set_clause} WHERE {where}"
    return execute(query, tuple(data.values()) + tuple(where_params), db_path)


def delete(table, where, where_params, db_path=None):
    query = f"DELETE FROM {table} WHERE {where}"
    return execute(query, tuple(where_params), db_path)
