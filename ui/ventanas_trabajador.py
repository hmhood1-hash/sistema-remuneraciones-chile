# -*- coding: utf-8 -*-
"""Ventana de gestión de Trabajadores (datos personales, laborales, previsionales
y cargas familiares)."""
import tkinter as tk
from tkinter import ttk

from modules import trabajador as mod_trabajador
from modules import empresa as mod_empresa
from modules import previsional as mod_previsional
from calculos.validaciones import validar_rut

from ui.estilos import COLOR_FONDO
from ui.tablas import TablaInteractiva
from ui.utils import centrar_ventana, mostrar_info, mostrar_error, confirmar

COLUMNAS_LISTA = ["codigo_empleado", "rut", "nombres", "apellido_paterno", "cargo", "sueldo_base"]

OPCIONES_SEXO = ["M", "F", "O"]
OPCIONES_ESTADO_CIVIL = ["Soltero", "Casado", "Viudo", "Separado"]
OPCIONES_SUELDO_TIPO = ["Mensual", "Diario", "Part Time", "Empresarial"]
OPCIONES_GRATIFICACION = ["Mensual", "Anual"]
OPCIONES_MODALIDAD_SALUD = ["Pesos", "UF", "7%", "7%+UF", "7%+UF+pesos"]
OPCIONES_SEGURO_CESANTIA = ["Plazo Fijo", "Indefinido"]
OPCIONES_TIPO_TRABAJADOR = [
    "Activo No Pensionado", "Pensionado y cotiza", "Pensionado no cotiza", "Activo > 60 o 65 años",
]
OPCIONES_SI_NO = ["S", "N"]
OPCIONES_TIPO_CARGA = ["Simple", "Materna", "Invalidez"]
OPCIONES_PARENTESCO = ["Hijo", "Cónyuge", "Progenitor", "Hermano"]


def abrir_ventana_trabajadores(maestro):
    ventana = tk.Toplevel(maestro)
    ventana.title("Trabajadores")
    ventana.geometry("900x520")
    ventana.configure(bg=COLOR_FONDO)
    ventana.transient(maestro)

    barra = ttk.Frame(ventana, padding=8)
    barra.pack(fill=tk.X)
    ttk.Button(barra, text="Nuevo Trabajador", style="Acento.TButton",
               command=lambda: VentanaTrabajador(ventana, al_guardar=lambda: _cargar(tabla))).pack(
        side=tk.LEFT, padx=4
    )
    ttk.Button(barra, text="Editar", command=lambda: _editar(ventana, tabla)).pack(side=tk.LEFT, padx=4)
    ttk.Button(barra, text="Dar de Baja", command=lambda: _eliminar(tabla)).pack(side=tk.LEFT, padx=4)

    tabla = TablaInteractiva(ventana, COLUMNAS_LISTA)
    tabla.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
    _cargar(tabla)

    centrar_ventana(ventana)
    return ventana


def _cargar(tabla):
    filas = mod_trabajador.listar_trabajadores()
    for fila in filas:
        fila["_id"] = fila["codigo_empleado"]
    tabla.cargar_datos(filas)


def _editar(maestro, tabla):
    seleccion = tabla.obtener_seleccion()
    if not seleccion:
        mostrar_info("Seleccione un trabajador", "Debe seleccionar un trabajador para editar.")
        return
    VentanaTrabajador(maestro, codigo_empleado=seleccion["codigo_empleado"],
                       al_guardar=lambda: _cargar(tabla))


def _eliminar(tabla):
    seleccion = tabla.obtener_seleccion()
    if not seleccion:
        mostrar_info("Seleccione un trabajador", "Debe seleccionar un trabajador para dar de baja.")
        return
    if confirmar("Confirmar baja", "¿Dar de baja al trabajador seleccionado?"):
        mod_trabajador.eliminar_trabajador(seleccion["codigo_empleado"])
        _cargar(tabla)


class VentanaTrabajador(tk.Toplevel):
    """Formulario completo (con pestañas) para crear/editar un trabajador."""

    def __init__(self, maestro, codigo_empleado=None, al_guardar=None):
        super().__init__(maestro)
        self.codigo_empleado = codigo_empleado
        self.al_guardar = al_guardar
        self.title("Ficha del Trabajador" if codigo_empleado else "Nuevo Trabajador")
        self.geometry("640x560")
        self.configure(bg=COLOR_FONDO)
        self.transient(maestro)
        self.grab_set()

        self.variables = {}
        self.trabajador_actual = (
            mod_trabajador.obtener_trabajador(codigo_empleado) if codigo_empleado else {}
        )

        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        self.tab_personales = ttk.Frame(notebook, padding=12)
        self.tab_laborales = ttk.Frame(notebook, padding=12)
        self.tab_previsionales = ttk.Frame(notebook, padding=12)
        self.tab_cargas = ttk.Frame(notebook, padding=12)

        notebook.add(self.tab_personales, text="Datos Personales")
        notebook.add(self.tab_laborales, text="Datos Laborales")
        notebook.add(self.tab_previsionales, text="Datos Previsionales")
        notebook.add(self.tab_cargas, text="Cargas Familiares")

        self._construir_datos_personales()
        self._construir_datos_laborales()
        self._construir_datos_previsionales()
        self._construir_cargas_familiares()

        botones = ttk.Frame(self, padding=8)
        botones.pack(fill=tk.X)
        ttk.Button(botones, text="Guardar", style="Acento.TButton", command=self._guardar).pack(
            side=tk.LEFT, padx=4
        )
        ttk.Button(botones, text="Cerrar", command=self.destroy).pack(side=tk.LEFT, padx=4)

        centrar_ventana(self)

    # ------------------------------------------------------------------
    def _campo(self, maestro, fila, nombre, etiqueta, tipo="texto", opciones=None):
        ttk.Label(maestro, text=etiqueta + ":").grid(row=fila, column=0, sticky=tk.W, padx=4, pady=3)
        valor = self.trabajador_actual.get(nombre, "")
        variable = tk.StringVar(value="" if valor is None else str(valor))
        if tipo == "combo":
            widget = ttk.Combobox(maestro, textvariable=variable, values=opciones, state="readonly", width=28)
        else:
            widget = ttk.Entry(maestro, textvariable=variable, width=30)
        widget.grid(row=fila, column=1, sticky=tk.W, padx=4, pady=3)
        self.variables[nombre] = variable

    def _construir_datos_personales(self):
        f = self.tab_personales
        campos = [
            ("rut", "RUT"), ("nombres", "Nombres"), ("apellido_paterno", "Apellido Paterno"),
            ("apellido_materno", "Apellido Materno"), ("fecha_nacimiento", "Fecha Nacimiento (YYYY-MM-DD)"),
            ("calle", "Calle"), ("numero", "Número"), ("dpto", "Depto."), ("comuna", "Comuna"),
            ("correo", "Correo Electrónico"), ("fono", "Fono"),
        ]
        for fila, (nombre, etiqueta) in enumerate(campos):
            self._campo(f, fila, nombre, etiqueta)
        self._campo(f, len(campos), "sexo", "Sexo", "combo", OPCIONES_SEXO)
        self._campo(f, len(campos) + 1, "estado_civil", "Estado Civil", "combo", OPCIONES_ESTADO_CIVIL)
        ttk.Label(f, text="Código Empleado (automático):").grid(row=len(campos) + 2, column=0, sticky=tk.W, padx=4, pady=3)
        ttk.Label(f, text=str(self.codigo_empleado or "Se asigna al guardar")).grid(
            row=len(campos) + 2, column=1, sticky=tk.W, padx=4, pady=3
        )

    def _construir_datos_laborales(self):
        f = self.tab_laborales
        empresas = mod_empresa.listar_empresas()
        opciones_empresa = ["{} - {}".format(e["codigo_empresa"], e["razon_social"]) for e in empresas]
        sucursales = mod_empresa.listar_sucursales()
        opciones_sucursal = ["{} - {}".format(s["codigo_sucursal"], s["nombre"]) for s in sucursales]
        centros = mod_empresa.listar_centros_costo()
        opciones_centro = [c["codigo_centro_costo"] for c in centros]

        ttk.Label(f, text="Empresa:").grid(row=0, column=0, sticky=tk.W, padx=4, pady=3)
        self.var_empresa = tk.StringVar()
        if self.trabajador_actual.get("codigo_empresa"):
            for opcion in opciones_empresa:
                if opcion.startswith(str(self.trabajador_actual["codigo_empresa"]) + " -"):
                    self.var_empresa.set(opcion)
        ttk.Combobox(f, textvariable=self.var_empresa, values=opciones_empresa, state="readonly",
                     width=28).grid(row=0, column=1, sticky=tk.W, padx=4, pady=3)

        self._campo(f, 1, "sueldo_tipo", "Tipo Sueldo", "combo", OPCIONES_SUELDO_TIPO)
        self._campo(f, 2, "sueldo_base", "Sueldo Base")
        self._campo(f, 3, "gratificacion_tipo", "Gratificación", "combo", OPCIONES_GRATIFICACION)
        self._campo(f, 4, "horas_semanales", "Horas Semanales")
        self._campo(f, 5, "dias_laborales_semana", "Días Laborales/Semana")
        self._campo(f, 6, "fecha_contrato", "Fecha Contrato (YYYY-MM-DD)")
        self._campo(f, 7, "cargo", "Cargo")
        self._campo(f, 8, "horarios", "Horarios")

        ttk.Label(f, text="Sucursal:").grid(row=9, column=0, sticky=tk.W, padx=4, pady=3)
        self.var_sucursal = tk.StringVar()
        if self.trabajador_actual.get("codigo_sucursal"):
            for opcion in opciones_sucursal:
                if opcion.startswith(str(self.trabajador_actual["codigo_sucursal"]) + " -"):
                    self.var_sucursal.set(opcion)
        ttk.Combobox(f, textvariable=self.var_sucursal, values=opciones_sucursal, state="readonly",
                     width=28).grid(row=9, column=1, sticky=tk.W, padx=4, pady=3)

        self._campo(f, 10, "codigo_centro_costo", "Centro de Costo", "combo", opciones_centro)
        self._campo(f, 11, "aplica_sis", "Aplica SIS", "combo", OPCIONES_SI_NO)

    def _construir_datos_previsionales(self):
        f = self.tab_previsionales
        afps = [a["codigo_afp"] for a in mod_previsional.listar_afp()]
        isapres = [i["codigo_isapre"] for i in mod_previsional.listar_isapres()]

        self._campo(f, 0, "codigo_afp", "AFP", "combo", afps)
        self._campo(f, 1, "codigo_isapre", "Salud (Isapre/Fonasa)", "combo", isapres)
        self._campo(f, 2, "modalidad_salud", "Modalidad Salud", "combo", OPCIONES_MODALIDAD_SALUD)
        self._campo(f, 3, "cotizacion_pactada", "Cotización Pactada (%)")
        self._campo(f, 4, "tope_salud", "Tope Salud (UF)")
        self._campo(f, 5, "seguro_cesantia", "Seguro de Cesantía", "combo", OPCIONES_SEGURO_CESANTIA)
        self._campo(f, 6, "fecha_inicio_afc", "Fecha Inicio AFC (YYYY-MM-DD)")
        self._campo(f, 7, "fecha_termino_afc", "Fecha Término AFC (YYYY-MM-DD)")
        self._campo(f, 8, "afp_cotiza_afc", "AFP Cotiza AFC", "combo", OPCIONES_SI_NO)
        self._campo(f, 9, "tipo_trabajador", "Tipo Trabajador", "combo", OPCIONES_TIPO_TRABAJADOR)

    def _construir_cargas_familiares(self):
        f = self.tab_cargas
        if not self.codigo_empleado:
            ttk.Label(f, text="Guarde primero al trabajador para gestionar sus cargas familiares.").pack(
                anchor=tk.W
            )
            return

        barra = ttk.Frame(f)
        barra.pack(fill=tk.X)
        ttk.Button(barra, text="Agregar Carga", command=self._agregar_carga).pack(side=tk.LEFT, padx=4)
        ttk.Button(barra, text="Eliminar Carga", command=self._eliminar_carga).pack(side=tk.LEFT, padx=4)

        columnas = ["rut_carga", "nombre", "fecha_inicio", "fecha_vencimiento", "tipo", "parentesco"]
        self.tabla_cargas = TablaInteractiva(f, columnas)
        self.tabla_cargas.pack(fill=tk.BOTH, expand=True, pady=8)
        self._cargar_cargas()

    def _cargar_cargas(self):
        filas = mod_trabajador.listar_cargas_familiares(self.codigo_empleado)
        for fila in filas:
            fila["_id"] = fila["id_carga"]
        self.tabla_cargas.cargar_datos(filas)

    def _agregar_carga(self):
        from ui.dialogs import FormularioModal

        campos = [
            {"nombre": "rut_carga", "etiqueta": "RUT Carga", "requerido": True},
            {"nombre": "nombre", "etiqueta": "Nombre", "requerido": True},
            {"nombre": "fecha_inicio", "etiqueta": "Fecha Inicio (YYYY-MM-DD)"},
            {"nombre": "fecha_vencimiento", "etiqueta": "Fecha Vencimiento (YYYY-MM-DD)"},
            {"nombre": "tipo", "etiqueta": "Tipo", "tipo": "combo", "opciones": OPCIONES_TIPO_CARGA},
            {"nombre": "parentesco", "etiqueta": "Parentesco", "tipo": "combo", "opciones": OPCIONES_PARENTESCO},
        ]

        def guardar(datos):
            datos["codigo_empleado"] = self.codigo_empleado
            mod_trabajador.crear_carga_familiar(datos)
            self._cargar_cargas()

        FormularioModal(self, "Nueva Carga Familiar", campos, al_guardar=guardar)

    def _eliminar_carga(self):
        seleccion = self.tabla_cargas.obtener_seleccion()
        if not seleccion:
            mostrar_info("Seleccione una carga", "Debe seleccionar una carga familiar para eliminar.")
            return
        if confirmar("Confirmar eliminación", "¿Eliminar la carga familiar seleccionada?"):
            mod_trabajador.eliminar_carga_familiar(seleccion["id_carga"])
            self._cargar_cargas()

    # ------------------------------------------------------------------
    def _valor(self, nombre, numerico=False):
        valor = self.variables[nombre].get().strip()
        if numerico:
            try:
                return float(valor) if valor else 0.0
            except ValueError:
                return 0.0
        return valor or None

    def _guardar(self):
        rut = self._valor("rut")
        if not rut or not validar_rut(rut):
            mostrar_error("RUT inválido", "El RUT ingresado no es válido.")
            return

        datos = {
            "rut": rut,
            "nombres": self._valor("nombres"),
            "apellido_paterno": self._valor("apellido_paterno"),
            "apellido_materno": self._valor("apellido_materno"),
            "fecha_nacimiento": self._valor("fecha_nacimiento"),
            "sexo": self._valor("sexo"),
            "estado_civil": self._valor("estado_civil"),
            "calle": self._valor("calle"),
            "numero": self._valor("numero"),
            "dpto": self._valor("dpto"),
            "comuna": self._valor("comuna"),
            "correo": self._valor("correo"),
            "fono": self._valor("fono"),
            "sueldo_tipo": self._valor("sueldo_tipo"),
            "sueldo_base": self._valor("sueldo_base", numerico=True),
            "gratificacion_tipo": self._valor("gratificacion_tipo"),
            "horas_semanales": self._valor("horas_semanales", numerico=True),
            "dias_laborales_semana": self._valor("dias_laborales_semana", numerico=True),
            "fecha_contrato": self._valor("fecha_contrato"),
            "cargo": self._valor("cargo"),
            "horarios": self._valor("horarios"),
            "codigo_centro_costo": self._valor("codigo_centro_costo"),
            "aplica_sis": self._valor("aplica_sis") or "N",
            "codigo_afp": self._valor("codigo_afp"),
            "codigo_isapre": self._valor("codigo_isapre"),
            "modalidad_salud": self._valor("modalidad_salud"),
            "cotizacion_pactada": self._valor("cotizacion_pactada", numerico=True),
            "tope_salud": self._valor("tope_salud"),
            "seguro_cesantia": self._valor("seguro_cesantia"),
            "fecha_inicio_afc": self._valor("fecha_inicio_afc"),
            "fecha_termino_afc": self._valor("fecha_termino_afc"),
            "afp_cotiza_afc": self._valor("afp_cotiza_afc") or "S",
            "tipo_trabajador": self._valor("tipo_trabajador") or "Activo No Pensionado",
        }

        if self.var_empresa.get():
            datos["codigo_empresa"] = int(self.var_empresa.get().split(" - ")[0])
        elif self.trabajador_actual.get("codigo_empresa"):
            datos["codigo_empresa"] = self.trabajador_actual["codigo_empresa"]
        else:
            mostrar_error("Empresa requerida", "Debe seleccionar la empresa del trabajador.")
            return

        if self.var_sucursal.get():
            datos["codigo_sucursal"] = int(self.var_sucursal.get().split(" - ")[0])

        try:
            if self.codigo_empleado:
                mod_trabajador.actualizar_trabajador(self.codigo_empleado, datos)
            else:
                self.codigo_empleado = mod_trabajador.crear_trabajador(datos)
        except Exception as error:  # noqa: BLE001
            mostrar_error("Error al guardar", str(error))
            return

        mostrar_info("Trabajador guardado", "Los datos del trabajador se guardaron correctamente.")
        if self.al_guardar:
            self.al_guardar()
        self.destroy()
