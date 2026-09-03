"""
Ventanas modales (popup) para captura de datos, confirmaciones y mensajes.
"""
import tkinter as tk
from tkinter import ttk, messagebox

from gui.estilos import COLOR_FONDO
from gui.widgets import CampoFormulario, crear_boton


def mostrar_info(titulo, mensaje):
    messagebox.showinfo(titulo, mensaje)


def mostrar_error(titulo, mensaje):
    messagebox.showerror(titulo, mensaje)


def mostrar_exito(titulo, mensaje):
    messagebox.showinfo(titulo, mensaje)


def pedir_confirmacion(titulo, mensaje):
    """Retorna True si el usuario confirma la acción."""
    return messagebox.askyesno(titulo, mensaje)


class DialogoBase(tk.Toplevel):
    """
    Ventana modal base: se centra sobre la ventana principal y bloquea
    la interacción con el resto de la aplicación hasta que se cierra.
    """

    def __init__(self, parent, titulo, ancho=480, alto=420):
        super().__init__(parent)
        self.title(titulo)
        self.configure(bg=COLOR_FONDO)
        self.resizable(False, False)
        self.transient(parent)
        self.resultado = None

        self.geometry(f"{ancho}x{alto}")
        self.update_idletasks()
        x = parent.winfo_rootx() + (parent.winfo_width() // 2) - (ancho // 2)
        y = parent.winfo_rooty() + (parent.winfo_height() // 2) - (alto // 2)
        self.geometry(f"+{max(x, 0)}+{max(y, 0)}")

        self.contenedor = ttk.Frame(self, style="Contenido.TFrame", padding=16)
        self.contenedor.pack(fill="both", expand=True)

        self.grab_set()
        self.focus_set()

    def cerrar(self):
        self.grab_release()
        self.destroy()


class FormularioEmpresa(DialogoBase):
    """
    Formulario modal para crear o editar una empresa.
    """

    def __init__(self, parent, empresa=None):
        super().__init__(parent, "Empresa" if empresa is None else "Editar Empresa", ancho=520, alto=560)
        self.empresa_original = empresa

        ttk.Label(self.contenedor, text="Datos de la Empresa", style="Titulo.TLabel").pack(anchor="w", pady=(0, 10))

        campos_frame = ttk.Frame(self.contenedor, style="Tarjeta.TFrame", padding=12)
        campos_frame.pack(fill="both", expand=True)

        self.campos = {}
        definiciones = [
            ("rut", "RUT Empresa", "rut", True),
            ("razon_social", "Razón Social", "texto", True),
            ("giro_comercial", "Giro Comercial", "texto", False),
            ("calle", "Calle", "texto", False),
            ("numero", "Número", "texto", False),
            ("comuna", "Comuna", "texto", False),
            ("ciudad", "Ciudad", "texto", False),
            ("region", "Región", "texto", False),
            ("correo", "Correo", "texto", False),
            ("fono", "Fono", "texto", False),
            ("rep_legal_rut", "RUT Representante Legal", "rut", True),
            ("rep_legal_nombres", "Nombres Representante", "texto", False),
        ]
        for clave, etiqueta, tipo, obligatorio in definiciones:
            campo = CampoFormulario(campos_frame, etiqueta, tipo=tipo, obligatorio=obligatorio)
            campo.pack(fill="x", pady=2)
            self.campos[clave] = campo

        if empresa:
            for clave, campo in self.campos.items():
                campo.set(empresa.get(clave, ""))
            self.campos["rut"].widget.configure(state="disabled")

        botones = ttk.Frame(self.contenedor, style="Contenido.TFrame")
        botones.pack(fill="x", pady=(12, 0))
        crear_boton(botones, "Guardar", self._guardar, tipo="Primario").pack(side="right", padx=4)
        crear_boton(botones, "Cancelar", self.cerrar, tipo="Secundario").pack(side="right", padx=4)

    def _guardar(self):
        valido = True
        for campo in self.campos.values():
            if campo.widget.instate(["disabled"]):
                continue
            if not campo.validar():
                valido = False
        if not valido:
            mostrar_error("Datos inválidos", "Revise los campos marcados en rojo.")
            return

        self.resultado = {clave: campo.get() for clave, campo in self.campos.items()}
        self.cerrar()


class FormularioTrabajador(DialogoBase):
    """
    Formulario modal completo para crear un trabajador: datos personales,
    laborales y previsionales.
    """

    AFP_OPCIONES = ["EMPART", "SSS", "CAPITAL", "CUPRUM", "HABITAT", "MODELO", "PLANVITAL", "PROVIDA", "UNO"]
    ISAPRE_OPCIONES = ["FONASA", "VIDATRES", "CONSALUD", "BANMEDICA", "MASVIDA", "CRUZBLANCA"]

    def __init__(self, parent, empresas):
        super().__init__(parent, "Nuevo Trabajador", ancho=560, alto=640)
        self.empresas = empresas

        notebook = ttk.Notebook(self.contenedor)
        notebook.pack(fill="both", expand=True)

        tab_personal = ttk.Frame(notebook, style="Tarjeta.TFrame", padding=12)
        tab_laboral = ttk.Frame(notebook, style="Tarjeta.TFrame", padding=12)
        tab_previsional = ttk.Frame(notebook, style="Tarjeta.TFrame", padding=12)

        notebook.add(tab_personal, text="Datos Personales")
        notebook.add(tab_laboral, text="Datos Laborales")
        notebook.add(tab_previsional, text="Datos Previsionales")

        self.campos = {}

        opciones_empresa = [f"{e['codigo']} - {e['razon_social']}" for e in empresas]

        personal = [
            ("rut", "RUT Trabajador", "rut", True, None),
            ("empresa", "Empresa", "opciones", True, opciones_empresa),
            ("nombre", "Nombre", "texto", True, None),
            ("ap_paterno", "Apellido Paterno", "texto", False, None),
            ("ap_materno", "Apellido Materno", "texto", False, None),
            ("fecha_nacimiento", "Fecha Nacimiento", "fecha", True, None),
            ("sexo", "Sexo (M/F/O)", "texto", True, None),
            ("estado_civil", "Estado Civil", "texto", False, None),
            ("comuna", "Comuna", "texto", False, None),
            ("correo", "Correo", "texto", False, None),
            ("fono", "Fono", "texto", False, None),
        ]
        for clave, etiqueta, tipo, obligatorio, valores in personal:
            campo = CampoFormulario(tab_personal, etiqueta, tipo=tipo, obligatorio=obligatorio, valores=valores)
            campo.pack(fill="x", pady=2)
            self.campos[clave] = campo

        laboral = [
            ("sueldo_tipo", "Tipo Sueldo", "opciones", True, ["Mensual", "Diario", "Part Time"]),
            ("sueldo_base", "Sueldo Base", "monto", True, None),
            ("gratificacion_tipo", "Tipo Gratificación", "opciones", False, ["Ninguna", "Mensual", "Anual"]),
            ("horas_semanales", "Horas Semanales", "entero", True, None),
            ("dias_laborales_semana", "Días Laborales/Semana", "entero", True, None),
            ("fecha_contrato", "Fecha Contrato", "fecha", True, None),
            ("cargo", "Cargo", "texto", False, None),
            ("aplica_sis", "¿Aplica SIS?", "opciones", True, ["S", "N"]),
        ]
        for clave, etiqueta, tipo, obligatorio, valores in laboral:
            campo = CampoFormulario(tab_laboral, etiqueta, tipo=tipo, obligatorio=obligatorio, valores=valores)
            campo.pack(fill="x", pady=2)
            self.campos[clave] = campo

        previsional = [
            ("afp_codigo", "AFP", "opciones", True, self.AFP_OPCIONES),
            ("isapre_codigo", "Isapre", "opciones", True, self.ISAPRE_OPCIONES),
            ("modalidad_salud", "Modalidad Salud", "opciones", False, ["7%", "UF", "Pesos"]),
            ("cotizacion_pactada", "Cotización Pactada (%)", "monto", True, None),
            ("tipo_trabajador", "Tipo Trabajador", "opciones", True,
             ["Activo No Pensionado", "Pensionado y cotiza", "Pensionado no cotiza"]),
        ]
        for clave, etiqueta, tipo, obligatorio, valores in previsional:
            campo = CampoFormulario(tab_previsional, etiqueta, tipo=tipo, obligatorio=obligatorio, valores=valores)
            campo.pack(fill="x", pady=2)
            self.campos[clave] = campo

        botones = ttk.Frame(self.contenedor, style="Contenido.TFrame")
        botones.pack(fill="x", pady=(12, 0))
        crear_boton(botones, "Guardar", self._guardar, tipo="Primario").pack(side="right", padx=4)
        crear_boton(botones, "Cancelar", self.cerrar, tipo="Secundario").pack(side="right", padx=4)

    def _guardar(self):
        valido = True
        for clave, campo in self.campos.items():
            if not campo.validar():
                valido = False
        if not valido:
            mostrar_error("Datos inválidos", "Revise los campos marcados en rojo.")
            return

        valores = {clave: campo.get() for clave, campo in self.campos.items()}
        valores["empresa_codigo"] = valores.pop("empresa").split(" - ")[0]
        self.resultado = valores
        self.cerrar()


class DialogoCargaFamiliar(DialogoBase):
    """Formulario modal para agregar una carga familiar a un trabajador."""

    def __init__(self, parent, rut_trabajador):
        super().__init__(parent, "Agregar Carga Familiar", ancho=420, alto=340)
        ttk.Label(self.contenedor, text=f"Trabajador: {rut_trabajador}", style="Titulo.TLabel").pack(anchor="w", pady=(0, 10))

        marco = ttk.Frame(self.contenedor, style="Tarjeta.TFrame", padding=12)
        marco.pack(fill="both", expand=True)

        self.campos = {}
        definiciones = [
            ("rut_carga", "RUT Carga", "rut", True, None),
            ("nombre", "Nombre", "texto", True, None),
            ("fecha_inicio", "Fecha Inicio", "fecha", True, None),
            ("tipo", "Tipo", "opciones", True, ["Simple", "Materna", "Invalidez"]),
            ("parentesco", "Parentesco", "opciones", True, ["Hijo", "Cónyuge", "Progenitor", "Hermano"]),
        ]
        for clave, etiqueta, tipo, obligatorio, valores in definiciones:
            campo = CampoFormulario(marco, etiqueta, tipo=tipo, obligatorio=obligatorio, valores=valores)
            campo.pack(fill="x", pady=2)
            self.campos[clave] = campo

        botones = ttk.Frame(self.contenedor, style="Contenido.TFrame")
        botones.pack(fill="x", pady=(12, 0))
        crear_boton(botones, "Guardar", self._guardar, tipo="Primario").pack(side="right", padx=4)
        crear_boton(botones, "Cancelar", self.cerrar, tipo="Secundario").pack(side="right", padx=4)
        self.rut_trabajador = rut_trabajador

    def _guardar(self):
        if not all(campo.validar() for campo in self.campos.values()):
            mostrar_error("Datos inválidos", "Revise los campos marcados en rojo.")
            return
        valores = {clave: campo.get() for clave, campo in self.campos.items()}
        valores["trabajador_rut"] = self.rut_trabajador
        self.resultado = valores
        self.cerrar()


class DialogoSeleccionLiquidacion(DialogoBase):
    """
    Formulario modal para seleccionar trabajador, año y mes previo al
    cálculo de una liquidación de sueldo.
    """

    def __init__(self, parent, trabajadores):
        super().__init__(parent, "Calcular Liquidación", ancho=420, alto=260)
        self.trabajadores = trabajadores

        marco = ttk.Frame(self.contenedor, style="Tarjeta.TFrame", padding=12)
        marco.pack(fill="both", expand=True)

        opciones = [f"{t['rut']} - {t['nombre']}" for t in trabajadores]
        self.campo_trabajador = CampoFormulario(marco, "Trabajador", tipo="opciones", obligatorio=True, valores=opciones)
        self.campo_anio = CampoFormulario(marco, "Año", tipo="entero", obligatorio=True)
        self.campo_mes = CampoFormulario(marco, "Mes (1-12)", tipo="entero", obligatorio=True)

        self.campo_trabajador.pack(fill="x", pady=4)
        self.campo_anio.pack(fill="x", pady=4)
        self.campo_mes.pack(fill="x", pady=4)

        botones = ttk.Frame(self.contenedor, style="Contenido.TFrame")
        botones.pack(fill="x", pady=(12, 0))
        crear_boton(botones, "Calcular", self._calcular, tipo="Primario").pack(side="right", padx=4)
        crear_boton(botones, "Cancelar", self.cerrar, tipo="Secundario").pack(side="right", padx=4)

    def _calcular(self):
        if not (self.campo_trabajador.validar() and self.campo_anio.validar() and self.campo_mes.validar()):
            mostrar_error("Datos inválidos", "Revise los campos marcados en rojo.")
            return
        mes = int(self.campo_mes.get())
        if mes < 1 or mes > 12:
            mostrar_error("Datos inválidos", "El mes debe estar entre 1 y 12.")
            return
        self.resultado = {
            "rut": self.campo_trabajador.get().split(" - ")[0],
            "anio": int(self.campo_anio.get()),
            "mes": mes,
        }
        self.cerrar()


class DialogoResumenLiquidacion(DialogoBase):
    """
    Ventana emergente con el resumen detallado de una liquidación calculada.
    """

    def __init__(self, parent, nombre_trabajador, liquidacion, formatear_moneda):
        super().__init__(parent, "Resumen de Liquidación", ancho=440, alto=520)

        ttk.Label(
            self.contenedor,
            text=f"Liquidación de {nombre_trabajador}\n{liquidacion['mes']}/{liquidacion['anio']}",
            style="Titulo.TLabel",
            justify="left",
        ).pack(anchor="w", pady=(0, 10))

        marco = ttk.Frame(self.contenedor, style="Tarjeta.TFrame", padding=12)
        marco.pack(fill="both", expand=True)

        filas = [
            ("Sueldo Base", liquidacion["sueldo_base"]),
            ("Gratificación", liquidacion["gratificacion"]),
            ("Total Haberes", liquidacion["total_haberes"]),
            ("AFP", -liquidacion["monto_afp"]),
            ("Salud", -liquidacion["monto_salud"]),
            ("AFC", -liquidacion["monto_afc"]),
            ("Impuesto Único", -liquidacion["impuesto_unico"]),
            ("Total Descuentos", -liquidacion["total_descuentos"]),
            ("Sueldo Líquido", liquidacion["sueldo_liquido"]),
        ]
        for etiqueta, valor in filas:
            fila = ttk.Frame(marco, style="Tarjeta.TFrame")
            fila.pack(fill="x", pady=2)
            negrita = etiqueta in ("Total Haberes", "Total Descuentos", "Sueldo Líquido")
            estilo = "Subtitulo.TLabel" if negrita else "Texto.TLabel"
            ttk.Label(fila, text=etiqueta, style=estilo).pack(side="left")
            ttk.Label(fila, text=formatear_moneda(abs(valor)), style=estilo).pack(side="right")

        botones = ttk.Frame(self.contenedor, style="Contenido.TFrame")
        botones.pack(fill="x", pady=(12, 0))
        crear_boton(botones, "Cerrar", self.cerrar, tipo="Primario").pack(side="right", padx=4)
