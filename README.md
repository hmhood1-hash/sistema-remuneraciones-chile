# Sistema Profesional de Remuneraciones - Chile

Sistema profesional de remuneraciones para Chile, desarrollado en **Python** con
base de datos **SQLite** e interfaz gráfica **tkinter**, optimizado para
**Windows 10/11 (32 y 64 bits)**.

## Características principales

- Interfaz gráfica moderna con menús desplegables, ventanas modales, tablas
  interactivas con búsqueda/filtro y barra de herramientas.
- Base de datos SQLite creada y respaldada automáticamente en
  `%LOCALAPPDATA%\SistemaRemuneraciones` (equivalente a
  `C:\Users\<usuario>\AppData\Local\SistemaRemuneraciones` en Windows).
- Gestión completa de Empresas, Sucursales, Centros de Costo, Trabajadores,
  Cargas Familiares, Instituciones Previsionales (AFP, Isapres, CCAF,
  Mutuales, Ahorro Previsional), Haberes y Descuentos, Contratos y Finiquitos,
  Vacaciones.
- Parámetros y factores 100% editables: sueldo mínimo, topes, UTM/UF
  mensuales, porcentajes de aportes, tramos de cargas familiares y tabla de
  Impuesto Único.
- Cálculo profesional de liquidaciones de sueldo: ingreso bruto, descuentos
  previsionales (AFP, salud, seguro de cesantía), impuesto único progresivo
  (tabla editable) y aportes patronales, con costo total para la empresa.
- Informes exportables a **Excel** (openpyxl) y **PDF** (reportlab): libro de
  remuneraciones, detalle de imposiciones, detalle de anticipos, ficha del
  trabajador, informe de vacaciones, liquidación individual y certificado
  tributario.
- Procesos de centralización mensual, actualización de la base de datos y
  respaldo automático.

## Requisitos

- Windows 10/11 (32 o 64 bits) o Linux/Mac para desarrollo.
- Python 3.9 o superior (con soporte de `tkinter`, incluido por defecto en el
  instalador oficial de Python para Windows).

## Instalación (Windows)

```
git clone https://github.com/hmhood1-hash/sistema-remuneraciones-chile.git
cd sistema-remuneraciones-chile
pip install -r requirements.txt
python main.py
```

Al ejecutar `main.py` por primera vez, el sistema crea automáticamente la
base de datos SQLite y sus tablas en `%LOCALAPPDATA%\SistemaRemuneraciones`,
junto con datos base (AFP, Isapres, CCAF, tabla de Impuesto Único, etc.).

## Estructura del proyecto

```
sistema-remuneraciones-chile/
├── main.py                 # Punto de entrada (menú principal)
├── requirements.txt
├── database/                # Esquema y conexión SQLite
├── calculos/                 # Impuesto único, previsiones, aportes, validaciones
├── modules/                  # Lógica de negocio (CRUD y procesos)
├── ui/                       # Interfaz gráfica tkinter (menús, diálogos, tablas)
├── reportes/                 # Exportación a Excel y PDF
└── tests/                    # Pruebas de los módulos de cálculo
```

## Generar ejecutable (.exe) con PyInstaller (opcional)

```
pip install pyinstaller
pyinstaller --onefile --windowed --name SistemaRemuneraciones main.py
```

El ejecutable resultante se genera en la carpeta `dist/` y no requiere tener
Python instalado para ejecutarse en otro equipo Windows.

## Ejecutar las pruebas

```
python -m unittest discover tests
```
