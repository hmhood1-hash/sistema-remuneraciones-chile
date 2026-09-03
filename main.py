"""
Sistema Profesional de Remuneraciones - Chile
Punto de entrada principal. Inicializa la base de datos SQLite (si no existe)
y despliega el menú principal en consola.
"""
from database.init_db import init_database
from ui.menus import menu_principal


def main():
    conn = init_database()
    conn.close()
    print("\n" + "="*60)
    print("   BIENVENIDO AL SISTEMA DE REMUNERACIONES - CHILE")
    print("="*60)
    menu_principal()
    print("\nHasta pronto.")


if __name__ == "__main__":
    main()
