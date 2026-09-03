# -*- coding: utf-8 -*-
"""
Sistema Profesional de Remuneraciones - Chile
Punto de entrada de la aplicación.

Ejecutar con: python main.py
Compatible con Windows 10/11 (32 y 64 bits) y con Linux/Mac para desarrollo.
"""
import sys
import io

# Asegura salida en UTF-8 para caracteres especiales (ñ, tildes) en consolas Windows.
if sys.stdout.encoding is None or sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")
    except Exception:  # pragma: no cover - algunos entornos no exponen 'buffer'
        pass

from database.init_db import inicializar_base_datos  # noqa: E402


def main():
    ruta_bd = inicializar_base_datos()
    print("Sistema Profesional de Remuneraciones - Chile")
    print("Base de datos lista en: {}".format(ruta_bd))

    from ui.main_window import iniciar_aplicacion
    iniciar_aplicacion()


if __name__ == "__main__":
    main()
