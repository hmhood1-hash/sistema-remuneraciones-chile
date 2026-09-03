"""
Ventana principal de la aplicación: menú superior, barra de herramientas,
panel lateral de navegación, área de contenido y barra de estado.
"""
import tkinter as tk
from tkinter import ttk

from database.models import fetch_all, fetch_one, insert, update, delete
from ui.utils import formatear_moneda
from calculos.validaciones import validar_rut

from modules.liquidacion import calcular_liquidacion, guardar_liquidacion

from gui.estilos import aplicar_estilo, COLOR_PRIMARIO, COLOR_TEXTO_CLARO, FUENTE_TITULO
from gui.widgets import TablaDatos, crear_boton, crear_boton_barra, BarraEstado
from gui.dialogs import (
    FormularioEmpresa,
    FormularioTrabajador,
    DialogoCargaFamiliar,
    DialogoSeleccionLiquidacion,
    DialogoResumenLiquidacion,
    mostrar_error,
    mostrar_exito,
    mostrar_info,
    pedir_confirmacion,
)
from gui.reportes_gui import PanelReportes


class VentanaPrincipal(tk.Tk):
    """
    Ventana principal del Sistema de Remuneraciones Chile.
    """

    def __init__(self):
        super().__init__()
        self.title("Sistema de Remuneraciones - Chile")
        self.geometry("1200x720")
        self.minsize(1000, 600)

        aplicar_estilo(self)

        self._crear_menu()
        self._crear_toolbar()
        self._crear_cuerpo()
        self._crear_barra_estado()

        self.mostrar_inicio()

    # ------------------------------------------------------------------
    # Estructura general
    # ------------------------------------------------------------------
    def _crear_menu(self):
        barra_menu = tk.Menu(self)

        menu_empresa = tk.Menu(barra_menu, tearoff=0)
        menu_empresa.add_command(label="Gestión de Empresa", command=self.mostrar_empresas)
        menu_empresa.add_separator()
        menu_empresa.add_command(label="Salir", command=self.destroy)
        barra_menu.add_cascade(label="Empresa", menu=menu_empresa)

        menu_trabajadores = tk.Menu(barra_menu, tearoff=0)
        menu_trabajadores.add_command(label="Gestión de Trabajadores", command=self.mostrar_trabajadores)
        barra_menu.add_cascade(label="Trabajadores", menu=menu_trabajadores)

        menu_liquidaciones = tk.Menu(barra_menu, tearoff=0)
        menu_liquidaciones.add_command(label="Liquidaciones de Sueldo", command=self.mostrar_liquidaciones)
        barra_menu.add_cascade(label="Liquidaciones", menu=menu_liquidaciones)

        menu_previsional = tk.Menu(barra_menu, tearoff=0)
        menu_previsional.add_command(label="Instituciones Previsionales", command=self.mostrar_previsional)
        barra_menu.add_cascade(label="Previsional", menu=menu_previsional)

        menu_reportes = tk.Menu(barra_menu, tearoff=0)
        menu_reportes.add_command(label="Informes y Reportes", command=self.mostrar_reportes)
        barra_menu.add_cascade(label="Reportes", menu=menu_reportes)

        menu_ayuda = tk.Menu(barra_menu, tearoff=0)
        menu_ayuda.add_command(label="Acerca de", command=self._acerca_de)
        barra_menu.add_cascade(label="Ayuda", menu=menu_ayuda)

        self.config(menu=barra_menu)

    def _crear_toolbar(self):
        self.toolbar = ttk.Frame(self, style="Toolbar.TFrame", padding=6)
        self.toolbar.pack(side="top", fill="x")

        crear_boton_barra(self.toolbar, "Inicio", "🏠", self.mostrar_inicio).pack(side="left", padx=3)
        crear_boton_barra(self.toolbar, "Empresas", "🏢", self.mostrar_empresas).pack(side="left", padx=3)
        crear_boton_barra(self.toolbar, "Trabajadores", "👤", self.mostrar_trabajadores).pack(side="left", padx=3)
        crear_boton_barra(self.toolbar, "Liquidaciones", "💵", self.mostrar_liquidaciones).pack(side="left", padx=3)
        crear_boton_barra(self.toolbar, "Previsional", "🏦", self.mostrar_previsional).pack(side="left", padx=3)
        crear_boton_barra(self.toolbar, "Reportes", "📊", self.mostrar_reportes).pack(side="left", padx=3)

    def _crear_cuerpo(self):
        cuerpo = ttk.Frame(self, style="Contenido.TFrame")
        cuerpo.pack(side="top", fill="both", expand=True)

        self.sidebar = ttk.Frame(cuerpo, style="Sidebar.TFrame", width=220)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Label(
            self.sidebar, text="MENÚ PRINCIPAL", bg=COLOR_PRIMARIO, fg=COLOR_TEXTO_CLARO,
            font=("Segoe UI", 11, "bold"), pady=16,
        ).pack(fill="x")

        opciones_sidebar = [
            ("🏠  Inicio", self.mostrar_inicio),
            ("🏢  Empresa", self.mostrar_empresas),
            ("👤  Trabajadores", self.mostrar_trabajadores),
            ("🏦  Previsional", self.mostrar_previsional),
            ("💵  Liquidaciones", self.mostrar_liquidaciones),
            ("📊  Reportes", self.mostrar_reportes),
        ]
        for texto, comando in opciones_sidebar:
            ttk.Button(self.sidebar, text=texto, command=comando, style="Sidebar.TButton").pack(fill="x")

        self.contenido = ttk.Frame(cuerpo, style="Contenido.TFrame", padding=16)
        self.contenido.pack(side="left", fill="both", expand=True)

    def _crear_barra_estado(self):
        self.barra_estado = BarraEstado(self)
        self.barra_estado.pack(side="bottom", fill="x")

    def _limpiar_contenido(self):
        for widget in self.contenido.winfo_children():
            widget.destroy()

    def _acerca_de(self):
        mostrar_info(
            "Acerca de",
            "Sistema de Remuneraciones - Chile\nInterfaz gráfica profesional (tkinter)\nCompatible con Windows 10/11",
        )

    # ------------------------------------------------------------------
    # Panel: Inicio
    # ------------------------------------------------------------------
    def mostrar_inicio(self):
        self._limpiar_contenido()
        self.barra_estado.mostrar("Inicio")

        ttk.Label(self.contenido, text="Bienvenido al Sistema de Remuneraciones - Chile", style="Titulo.TLabel").pack(
            anchor="w", pady=(0, 16)
        )
        tarjeta = ttk.Frame(self.contenido, style="Tarjeta.TFrame", padding=20)
        tarjeta.pack(fill="both", expand=True)
        ttk.Label(
            tarjeta,
            text=(
                "Use el menú superior, la barra de herramientas o el panel lateral\n"
                "para acceder a los módulos del sistema:\n\n"
                "• Gestión de Empresa\n"
                "• Gestión de Trabajadores\n"
                "• Instituciones Previsionales\n"
                "• Liquidaciones de Sueldo\n"
                "• Informes y Reportes"
            ),
            style="Subtitulo.TLabel",
            justify="left",
        ).pack(anchor="w")

    # ------------------------------------------------------------------
    # Panel: Empresa
    # ------------------------------------------------------------------
    def mostrar_empresas(self):
        self._limpiar_contenido()
        self.barra_estado.mostrar("Gestión de Empresa")

        ttk.Label(self.contenido, text="Gestión de Empresa", style="Titulo.TLabel").pack(anchor="w", pady=(0, 10))

        botones = ttk.Frame(self.contenido, style="Contenido.TFrame")
        botones.pack(fill="x", pady=(0, 8))
        crear_boton(botones, "Nuevo", lambda: self._crear_empresa()).pack(side="left", padx=4)
        crear_boton(botones, "Editar", lambda: self._editar_empresa(), tipo="Secundario").pack(side="left", padx=4)
        crear_boton(botones, "Eliminar", lambda: self._eliminar_empresa(), tipo="Peligro").pack(side="left", padx=4)
        crear_boton(botones, "Actualizar", lambda: self._cargar_empresas(), tipo="Secundario").pack(side="left", padx=4)

        columnas = ["codigo", "rut", "razon_social", "ciudad", "region"]
        self.tabla_empresas = TablaDatos(self.contenido, columnas)
        self.tabla_empresas.pack(fill="both", expand=True)

        self._cargar_empresas()

    def _cargar_empresas(self):
        self.tabla_empresas.cargar_datos(fetch_all("empresa"))
        self.barra_estado.mostrar("Empresas actualizadas")

    def _crear_empresa(self):
        dialogo = FormularioEmpresa(self)
        self.wait_window(dialogo)
        if dialogo.resultado:
            if not validar_rut(dialogo.resultado["rut"]):
                mostrar_error("RUT Inválido", "El RUT de la empresa no es válido.")
                return
            try:
                insert("empresa", dialogo.resultado)
                mostrar_exito("Empresa Creada", "La empresa fue creada exitosamente.")
                self._cargar_empresas()
            except Exception as e:
                mostrar_error("Error", str(e))

    def _editar_empresa(self):
        fila = self.tabla_empresas.fila_seleccionada()
        if not fila:
            mostrar_error("Sin selección", "Seleccione una empresa de la tabla.")
            return
        empresa = fetch_one("empresa", {"codigo": fila[0]})
        dialogo = FormularioEmpresa(self, empresa=empresa)
        self.wait_window(dialogo)
        if dialogo.resultado:
            datos = {k: v for k, v in dialogo.resultado.items() if k != "rut"}
            try:
                update("empresa", datos, {"codigo": empresa["codigo"]})
                mostrar_exito("Empresa Actualizada", "Los cambios fueron guardados.")
                self._cargar_empresas()
            except Exception as e:
                mostrar_error("Error", str(e))

    def _eliminar_empresa(self):
        fila = self.tabla_empresas.fila_seleccionada()
        if not fila:
            mostrar_error("Sin selección", "Seleccione una empresa de la tabla.")
            return
        if pedir_confirmacion("Confirmar", f"¿Eliminar la empresa '{fila[2]}'?"):
            try:
                delete("empresa", {"codigo": fila[0]})
                mostrar_exito("Empresa Eliminada", "La empresa fue eliminada.")
                self._cargar_empresas()
            except Exception as e:
                mostrar_error("Error", str(e))

    # ------------------------------------------------------------------
    # Panel: Trabajadores
    # ------------------------------------------------------------------
    def mostrar_trabajadores(self):
        self._limpiar_contenido()
        self.barra_estado.mostrar("Gestión de Trabajadores")

        ttk.Label(self.contenido, text="Gestión de Trabajadores", style="Titulo.TLabel").pack(anchor="w", pady=(0, 10))

        barra_busqueda = ttk.Frame(self.contenido, style="Contenido.TFrame")
        barra_busqueda.pack(fill="x", pady=(0, 8))
        ttk.Label(barra_busqueda, text="Buscar por RUT/Nombre:", style="TextoFondo.TLabel").pack(side="left", padx=(0, 6))
        self.busqueda_var = tk.StringVar()
        entrada_busqueda = ttk.Entry(barra_busqueda, textvariable=self.busqueda_var, width=30)
        entrada_busqueda.pack(side="left", padx=(0, 6))
        entrada_busqueda.bind("<KeyRelease>", lambda e: self._filtrar_trabajadores())

        botones = ttk.Frame(self.contenido, style="Contenido.TFrame")
        botones.pack(fill="x", pady=(0, 8))
        crear_boton(botones, "Nuevo", self._crear_trabajador).pack(side="left", padx=4)
        crear_boton(botones, "Cargas Familiares", self._agregar_carga_familiar, tipo="Secundario").pack(side="left", padx=4)
        crear_boton(botones, "Eliminar", self._eliminar_trabajador, tipo="Peligro").pack(side="left", padx=4)
        crear_boton(botones, "Actualizar", self._cargar_trabajadores, tipo="Secundario").pack(side="left", padx=4)

        columnas = ["rut", "nombre", "ap_paterno", "cargo"]
        self.tabla_trabajadores = TablaDatos(self.contenido, columnas)
        self.tabla_trabajadores.pack(fill="both", expand=True)

        self._cargar_trabajadores()

    def _obtener_trabajadores_con_cargo(self):
        trabajadores = fetch_all("trabajador")
        for t in trabajadores:
            datos_laborales = fetch_one("datos_laborales", {"trabajador_rut": t["rut"]})
            t["cargo"] = datos_laborales.get("cargo", "") if datos_laborales else ""
        return trabajadores

    def _cargar_trabajadores(self):
        self._trabajadores_cache = self._obtener_trabajadores_con_cargo()
        self.tabla_trabajadores.cargar_datos(self._trabajadores_cache)
        self.barra_estado.mostrar("Trabajadores actualizados")

    def _filtrar_trabajadores(self):
        texto = self.busqueda_var.get().strip().lower()
        datos = getattr(self, "_trabajadores_cache", None) or self._obtener_trabajadores_con_cargo()
        if not texto:
            filtrados = datos
        else:
            filtrados = [
                t for t in datos
                if texto in t["rut"].lower() or texto in (t.get("nombre") or "").lower()
            ]
        self.tabla_trabajadores.cargar_datos(filtrados)

    def _crear_trabajador(self):
        empresas = fetch_all("empresa")
        if not empresas:
            mostrar_error("Sin empresas", "Debe registrar al menos una empresa antes de crear un trabajador.")
            return

        dialogo = FormularioTrabajador(self, empresas)
        self.wait_window(dialogo)
        if not dialogo.resultado:
            return

        datos = dialogo.resultado
        rut = datos["rut"]
        if fetch_one("trabajador", {"rut": rut}):
            mostrar_error("Trabajador existente", "Ya existe un trabajador con ese RUT.")
            return

        try:
            trabajador_datos = {
                "rut": rut,
                "empresa_codigo": datos["empresa_codigo"],
                "nombre": datos["nombre"],
                "ap_paterno": datos["ap_paterno"],
                "ap_materno": datos["ap_materno"],
                "fecha_nacimiento": datos["fecha_nacimiento"],
                "sexo": datos["sexo"],
                "estado_civil": datos["estado_civil"],
                "comuna": datos["comuna"],
                "correo": datos["correo"],
                "fono": datos["fono"],
            }
            insert("trabajador", trabajador_datos)

            datos_laborales = {
                "trabajador_rut": rut,
                "sueldo_tipo": datos["sueldo_tipo"],
                "sueldo_base": float(datos["sueldo_base"]),
                "gratificacion_tipo": datos["gratificacion_tipo"],
                "horas_semanales": int(datos["horas_semanales"]),
                "dias_laborales_semana": int(datos["dias_laborales_semana"]),
                "fecha_contrato": datos["fecha_contrato"],
                "cargo": datos["cargo"],
                "aplica_sis": datos["aplica_sis"],
            }
            insert("datos_laborales", datos_laborales)

            datos_previsionales = {
                "trabajador_rut": rut,
                "afp_codigo": datos["afp_codigo"],
                "isapre_codigo": datos["isapre_codigo"],
                "modalidad_salud": datos["modalidad_salud"],
                "cotizacion_pactada": float(datos["cotizacion_pactada"]),
                "tipo_trabajador": datos["tipo_trabajador"],
            }
            insert("datos_previsionales", datos_previsionales)

            mostrar_exito("Trabajador Creado", f"El trabajador {datos['nombre']} fue creado exitosamente.")
            self._cargar_trabajadores()
        except Exception as e:
            mostrar_error("Error", str(e))

    def _agregar_carga_familiar(self):
        fila = self.tabla_trabajadores.fila_seleccionada()
        if not fila:
            mostrar_error("Sin selección", "Seleccione un trabajador de la tabla.")
            return
        rut = fila[0]
        dialogo = DialogoCargaFamiliar(self, rut)
        self.wait_window(dialogo)
        if dialogo.resultado:
            try:
                insert("carga_familiar", dialogo.resultado)
                mostrar_exito("Carga Familiar", "La carga familiar fue agregada.")
            except Exception as e:
                mostrar_error("Error", str(e))

    def _eliminar_trabajador(self):
        fila = self.tabla_trabajadores.fila_seleccionada()
        if not fila:
            mostrar_error("Sin selección", "Seleccione un trabajador de la tabla.")
            return
        rut = fila[0]
        if pedir_confirmacion("Confirmar", f"¿Eliminar al trabajador '{fila[1]}'?"):
            try:
                delete("datos_previsionales", {"trabajador_rut": rut})
                delete("datos_laborales", {"trabajador_rut": rut})
                delete("trabajador", {"rut": rut})
                mostrar_exito("Trabajador Eliminado", "El trabajador fue eliminado.")
                self._cargar_trabajadores()
            except Exception as e:
                mostrar_error("Error", str(e))

    # ------------------------------------------------------------------
    # Panel: Liquidaciones
    # ------------------------------------------------------------------
    def mostrar_liquidaciones(self):
        self._limpiar_contenido()
        self.barra_estado.mostrar("Liquidaciones de Sueldo")

        ttk.Label(self.contenido, text="Liquidaciones de Sueldo", style="Titulo.TLabel").pack(anchor="w", pady=(0, 10))

        botones = ttk.Frame(self.contenido, style="Contenido.TFrame")
        botones.pack(fill="x", pady=(0, 8))
        crear_boton(botones, "Calcular Liquidación", self._calcular_liquidacion).pack(side="left", padx=4)
        crear_boton(botones, "Actualizar", self._cargar_liquidaciones, tipo="Secundario").pack(side="left", padx=4)

        columnas = ["trabajador_rut", "anio", "mes", "sueldo_base", "sueldo_liquido"]
        self.tabla_liquidaciones = TablaDatos(self.contenido, columnas)
        self.tabla_liquidaciones.pack(fill="both", expand=True)

        self._cargar_liquidaciones()

    def _cargar_liquidaciones(self):
        self.tabla_liquidaciones.cargar_datos(fetch_all("liquidacion"))
        self.barra_estado.mostrar("Liquidaciones actualizadas")

    def _calcular_liquidacion(self):
        trabajadores = fetch_all("trabajador")
        if not trabajadores:
            mostrar_error("Sin trabajadores", "Debe registrar al menos un trabajador.")
            return

        dialogo = DialogoSeleccionLiquidacion(self, trabajadores)
        self.wait_window(dialogo)
        if not dialogo.resultado:
            return

        rut = dialogo.resultado["rut"]
        anio = dialogo.resultado["anio"]
        mes = dialogo.resultado["mes"]

        trabajador = fetch_one("trabajador", {"rut": rut})

        self.barra_estado.iniciar_progreso()
        self.barra_estado.mostrar("Calculando liquidación...")
        self.update_idletasks()
        try:
            liquidacion = calcular_liquidacion(rut, trabajador["empresa_codigo"], anio, mes)
            guardar_liquidacion(liquidacion)
            self._cargar_liquidaciones()
            nombre = f"{trabajador['nombre']} {trabajador.get('ap_paterno', '')}".strip()
            DialogoResumenLiquidacion(self, nombre, liquidacion, formatear_moneda)
        except Exception as e:
            mostrar_error("Error al calcular", str(e))
        finally:
            self.barra_estado.detener_progreso()
            self.barra_estado.mostrar("Liquidación calculada")

    # ------------------------------------------------------------------
    # Panel: Instituciones Previsionales
    # ------------------------------------------------------------------
    def mostrar_previsional(self):
        self._limpiar_contenido()
        self.barra_estado.mostrar("Instituciones Previsionales")

        ttk.Label(self.contenido, text="Instituciones Previsionales", style="Titulo.TLabel").pack(anchor="w", pady=(0, 10))

        notebook = ttk.Notebook(self.contenido)
        notebook.pack(fill="both", expand=True)

        secciones = [
            ("AFP", "afp", ["codigo", "nombre", "factor_cotizacion"]),
            ("Isapres", "isapre", ["codigo", "nombre"]),
            ("CCAF", "ccaf", ["codigo", "nombre"]),
            ("Mutuales", "mutual", ["codigo", "nombre"]),
            ("APV", "ahorro_previsional", ["codigo", "nombre"]),
        ]
        for etiqueta, tabla, columnas in secciones:
            marco = ttk.Frame(notebook, style="Contenido.TFrame", padding=10)
            notebook.add(marco, text=etiqueta)
            tabla_datos = TablaDatos(marco, columnas)
            tabla_datos.pack(fill="both", expand=True)
            tabla_datos.cargar_datos(fetch_all(tabla))

    # ------------------------------------------------------------------
    # Panel: Reportes
    # ------------------------------------------------------------------
    def mostrar_reportes(self):
        self._limpiar_contenido()
        self.barra_estado.mostrar("Informes y Reportes")

        panel = PanelReportes(self.contenido, self.barra_estado)
        panel.pack(fill="both", expand=True)


def iniciar_aplicacion():
    """Punto de entrada para lanzar la interfaz gráfica."""
    app = VentanaPrincipal()
    app.mainloop()
