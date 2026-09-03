"""
Sistema Profesional de Remuneraciones - Chile
Punto de entrada principal. Inicializa la base de datos SQLite (si no existe)
y despliega la interfaz gráfica (GUI) profesional con tkinter.
"""
from database.init_db import init_database
from gui.main_window import iniciar_aplicacion


def main():
    conn = init_database()
    conn.close()
    iniciar_aplicacion()


if __name__ == "__main__":
    main()
