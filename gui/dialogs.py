"""
Diálogos para crear/editar datos en la aplicación
"""
import tkinter as tk
from tkinter import ttk, messagebox
from gui.estilos import COLORES, FUENTES, aplicar_estilo_boton
from gui.widgets import CampoFormulario
from database.models import insert, update, fetch_one, delete
from ui.utils import validar_rut
import re


class CampoRUT(ttk.Entry):
    """
    Campo de entrada especializado para RUT con formateo automático
    """
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.var = tk.StringVar()
        self.config(textvariable=self.var)
        self.var.trace('w', self._formatear_rut)
    
    def _formatear_rut(self, *args):
        """Formatea el RUT automáticamente"""
        valor = self.var.get().upper()
        # Eliminar caracteres no permitidos
        valor = re.sub(r'[^0-9K\-.]', '', valor)
        
        # Limitar a 12 caracteres (sin puntos)
        valor_sin_formato = valor.replace('.', '').replace('-', '')
        if len(valor_sin_formato) > 9:
            valor_sin_formato = valor_sin_formato[:9]
        
        # Formatear como XX.XXX.XXX-K
        if len(valor_sin_formato) > 0:
            if len(valor_sin_formato) <= 2:
                valor_formateado = valor_sin_formato
            elif len(valor_sin_formato) <= 5:
                valor_formateado = valor_sin_formato[:2] + '.' + valor_sin_formato[2:]
            elif len(valor_sin_formato) <= 8:
                valor_formateado = valor_sin_formato[:2] + '.' + valor_sin_formato[2:5] + '.' + valor_sin_formato[5:]
            else:
                valor_formateado = valor_sin_formato[:2] + '.' + valor_sin_formato[2:5] + '.' + valor_sin_formato[5:8] + '-' + valor_sin_formato[8]
        else:
            valor_formateado = ''
        
        self.var.set(valor_formateado)


class CampoFecha(ttk.Entry):
    """
    Campo de entrada especializado para fechas con formateo automático DD/MM/YYYY
    """
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.var = tk.StringVar()
        self.config(textvariable=self.var)
        self.var.trace('w', self._formatear_fecha)
    
    def _formatear_fecha(self, *args):
        """Formatea la fecha automáticamente como DD/MM/YYYY"""
        valor = self.var.get()
        # Eliminar caracteres no permitidos
        valor = re.sub(r'[^0-9/]', '', valor)
        
        # Limitar a 8 dígitos
        valor_sin_formato = valor.replace('/', '')
        if len(valor_sin_formato) > 8:
            valor_sin_formato = valor_sin_formato[:8]
        
        # Formatear como DD/MM/YYYY
        if len(valor_sin_formato) > 0:
            if len(valor_sin_formato) <= 2:
                valor_formateado = valor_sin_formato
            elif len(valor_sin_formato) <= 4:
                valor_formateado = valor_sin_formato[:2] + '/' + valor_sin_formato[2:]
            else:
                valor_formateado = valor_sin_formato[:2] + '/' + valor_sin_formato[2:4] + '/' + valor_sin_formato[4:]
        else:
            valor_formateado = ''
        
        self.var.set(valor_formateado)


class DialogoEmpresa(tk.Toplevel):
    """
    Diálogo para crear/editar empresa con campos visibles
    """
    def __init__(self, parent, empresa=None):
        super().__init__(parent)
        self.title('Nueva Empresa' if not empresa else 'Editar Empresa')
        self.geometry('700x800')
        self.resizable(True, True)
        self.empresa = empresa
        self.resultado = None
        
        # Hacer que el diálogo sea modal
        self.transient(parent)
        self.grab_set()
        
        # Configurar color de fondo
        self.config(bg=COLORES['fondo_principal'])
        
        # Frame principal con Canvas para scroll
        main_frame = ttk.Frame(self)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Canvas con scrollbar
        canvas = tk.Canvas(main_frame, bg=COLORES['fondo_principal'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient='vertical', command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, padding='20')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Permitir scroll con rueda del mouse
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Grid layout
        canvas.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        scrollbar.grid(row=0, column=1, sticky='ns')
        main_frame.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # Título del diálogo
        lbl_titulo = ttk.Label(
            scrollable_frame,
            text='Nueva Empresa' if not empresa else 'Editar Empresa',
            font=FUENTES['titulo']
        )
        lbl_titulo.pack(pady=15)
        
        # Separador
        ttk.Separator(scrollable_frame, orient='horizontal').pack(fill='x', pady=10)
        
        # Frame de campos
        frame_campos = ttk.Frame(scrollable_frame)
        frame_campos.pack(fill='both', expand=True, pady=10)
        
        # RUT
        lbl_rut = ttk.Label(frame_campos, text='RUT * (Formato automático)', font=FUENTES['normal'])
        lbl_rut.pack(anchor='w', pady=(10, 2))
        self.campo_rut = CampoRUT(frame_campos, font=FUENTES['normal'], width=50)
        self.campo_rut.pack(fill='x', pady=(0, 15))
        
        # Razón Social
        lbl_razon = ttk.Label(frame_campos, text='Razón Social *', font=FUENTES['normal'])
        lbl_razon.pack(anchor='w', pady=(10, 2))
        self.campo_razon = ttk.Entry(frame_campos, font=FUENTES['normal'], width=50)
        self.campo_razon.pack(fill='x', pady=(0, 15))
        
        # Calle
        lbl_calle = ttk.Label(frame_campos, text='Calle', font=FUENTES['normal'])
        lbl_calle.pack(anchor='w', pady=(10, 2))
        self.campo_calle = ttk.Entry(frame_campos, font=FUENTES['normal'], width=50)
        self.campo_calle.pack(fill='x', pady=(0, 15))
        
        # Número
        lbl_numero = ttk.Label(frame_campos, text='Número', font=FUENTES['normal'])
        lbl_numero.pack(anchor='w', pady=(10, 2))
        self.campo_numero = ttk.Entry(frame_campos, font=FUENTES['normal'], width=50)
        self.campo_numero.pack(fill='x', pady=(0, 15))
        
        # Depto
        lbl_depto = ttk.Label(frame_campos, text='Depto', font=FUENTES['normal'])
        lbl_depto.pack(anchor='w', pady=(10, 2))
        self.campo_depto = ttk.Entry(frame_campos, font=FUENTES['normal'], width=50)
        self.campo_depto.pack(fill='x', pady=(0, 15))
        
        # Comuna
        lbl_comuna = ttk.Label(frame_campos, text='Comuna', font=FUENTES['normal'])
        lbl_comuna.pack(anchor='w', pady=(10, 2))
        self.campo_comuna = ttk.Entry(frame_campos, font=FUENTES['normal'], width=50)
        self.campo_comuna.pack(fill='x', pady=(0, 15))
        
        # Ciudad
        lbl_ciudad = ttk.Label(frame_campos, text='Ciudad', font=FUENTES['normal'])
        lbl_ciudad.pack(anchor='w', pady=(10, 2))
        self.campo_ciudad = ttk.Entry(frame_campos, font=FUENTES['normal'], width=50)
        self.campo_ciudad.pack(fill='x', pady=(0, 15))
        
        # Región
        lbl_region = ttk.Label(frame_campos, text='Región', font=FUENTES['normal'])
        lbl_region.pack(anchor='w', pady=(10, 2))
        self.campo_region = ttk.Entry(frame_campos, font=FUENTES['normal'], width=50)
        self.campo_region.pack(fill='x', pady=(0, 15))
        
        # Correo
        lbl_correo = ttk.Label(frame_campos, text='Correo', font=FUENTES['normal'])
        lbl_correo.pack(anchor='w', pady=(10, 2))
        self.campo_correo = ttk.Entry(frame_campos, font=FUENTES['normal'], width=50)
        self.campo_correo.pack(fill='x', pady=(0, 15))
        
        # Teléfono
        lbl_fono = ttk.Label(frame_campos, text='Teléfono', font=FUENTES['normal'])
        lbl_fono.pack(anchor='w', pady=(10, 2))
        self.campo_fono = ttk.Entry(frame_campos, font=FUENTES['normal'], width=50)
        self.campo_fono.pack(fill='x', pady=(0, 15))
        
        # Giro Comercial
        lbl_giro = ttk.Label(frame_campos, text='Giro Comercial', font=FUENTES['normal'])
        lbl_giro.pack(anchor='w', pady=(10, 2))
        self.campo_giro = ttk.Entry(frame_campos, font=FUENTES['normal'], width=50)
        self.campo_giro.pack(fill='x', pady=(0, 15))
        
        # RUT Representante Legal
        lbl_rep_rut = ttk.Label(frame_campos, text='RUT Representante Legal', font=FUENTES['normal'])
        lbl_rep_rut.pack(anchor='w', pady=(10, 2))
        self.campo_rep_rut = CampoRUT(frame_campos, font=FUENTES['normal'], width=50)
        self.campo_rep_rut.pack(fill='x', pady=(0, 15))
        
        # Nombre Representante
        lbl_rep_nombre = ttk.Label(frame_campos, text='Nombre Representante', font=FUENTES['normal'])
        lbl_rep_nombre.pack(anchor='w', pady=(10, 2))
        self.campo_rep_nombre = ttk.Entry(frame_campos, font=FUENTES['normal'], width=50)
        self.campo_rep_nombre.pack(fill='x', pady=(0, 30))
        
        # Separador
        ttk.Separator(scrollable_frame, orient='horizontal').pack(fill='x', pady=10)
        
        # Frame botones
        frame_botones = ttk.Frame(scrollable_frame)
        frame_botones.pack(fill='x', pady=20)
        
        # Botón Guardar
        btn_guardar = tk.Button(
            frame_botones,
            text='💾 Guardar',
            command=self.guardar,
            font=FUENTES['normal'],
            bg=COLORES['azul_primario'],
            fg='white',
            padx=30,
            pady=10,
            relief='flat',
            cursor='hand2'
        )
        btn_guardar.pack(side='left', padx=5)
        
        # Botón Cancelar
        btn_cancelar = tk.Button(
            frame_botones,
            text='❌ Cancelar',
            command=self.destroy,
            font=FUENTES['normal'],
            bg=COLORES['rojo_error'],
            fg='white',
            padx=30,
            pady=10,
            relief='flat',
            cursor='hand2'
        )
        btn_cancelar.pack(side='left', padx=5)
        
        # Si es edición, cargar datos
        if empresa:
            self.campo_rut.var.set(empresa.get('rut', ''))
            self.campo_rut.config(state='readonly')
            self.campo_razon.insert(0, empresa.get('razon_social', ''))
            self.campo_calle.insert(0, empresa.get('calle', '') or '')
            self.campo_numero.insert(0, empresa.get('numero', '') or '')
            self.campo_depto.insert(0, empresa.get('depto', '') or '')
            self.campo_comuna.insert(0, empresa.get('comuna', '') or '')
            self.campo_ciudad.insert(0, empresa.get('ciudad', '') or '')
            self.campo_region.insert(0, empresa.get('region', '') or '')
            self.campo_correo.insert(0, empresa.get('correo', '') or '')
            self.campo_fono.insert(0, empresa.get('fono', '') or '')
            self.campo_giro.insert(0, empresa.get('giro_comercial', '') or '')
            self.campo_rep_rut.var.set(empresa.get('rep_legal_rut', '') or '')
            self.campo_rep_nombre.insert(0, empresa.get('rep_legal_nombres', '') or '')
        
        # Centrar en pantalla
        self.update_idletasks()
        x = self.winfo_screenwidth() // 2 - self.winfo_width() // 2
        y = self.winfo_screenheight() // 2 - self.winfo_height() // 2
        self.geometry(f'+{x}+{y}')
        
        # Focus en primer campo
        self.campo_rut.focus()
    
    def guardar(self):
        """
        Valida y guarda los datos
        """
        # Validar campos obligatorios
        rut = self.campo_rut.var.get().strip()
        razon = self.campo_razon.get().strip()
        
        if not rut:
            messagebox.showerror('Error', 'Ingrese el RUT de la empresa')
            self.campo_rut.focus()
            return
        
        if not razon:
            messagebox.showerror('Error', 'Ingrese la Razón Social')
            self.campo_razon.focus()
            return
        
        # Validar formato RUT
        if not validar_rut(rut):
            messagebox.showerror('Error', 'RUT inválido. Formato: XX.XXX.XXX-K')
            self.campo_rut.focus()
            return
        
        datos = {
            'rut': rut,
            'razon_social': razon,
            'calle': self.campo_calle.get().strip() or None,
            'numero': self.campo_numero.get().strip() or None,
            'depto': self.campo_depto.get().strip() or None,
            'comuna': self.campo_comuna.get().strip() or None,
            'ciudad': self.campo_ciudad.get().strip() or None,
            'region': self.campo_region.get().strip() or None,
            'correo': self.campo_correo.get().strip() or None,
            'fono': self.campo_fono.get().strip() or None,
            'giro_comercial': self.campo_giro.get().strip() or None,
            'rep_legal_rut': self.campo_rep_rut.var.get().strip() or None,
            'rep_legal_nombres': self.campo_rep_nombre.get().strip() or None,
        }
        
        try:
            if self.empresa:
                # Actualizar empresa existente
                update('empresa', datos, {'rut': rut})
                messagebox.showinfo('Éxito', 'Empresa actualizada correctamente')
            else:
                # Crear nueva empresa
                insert('empresa', datos)
                messagebox.showinfo('Éxito', 'Empresa creada correctamente')
            
            self.resultado = datos
            self.destroy()
        except Exception as e:
            messagebox.showerror('Error', f'Error al guardar empresa:\n{str(e)}')


class DialogoTrabajador(tk.Toplevel):
    """
    Diálogo para crear/editar trabajador
    """
    def __init__(self, parent, trabajador=None, empresa_codigo=None):
        super().__init__(parent)
        self.title('Nuevo Trabajador' if not trabajador else 'Editar Trabajador')
        self.geometry('700x900')
        self.resizable(True, True)
        self.trabajador = trabajador
        self.empresa_codigo = empresa_codigo
        self.resultado = None
        
        # Hacer que el diálogo sea modal
        self.transient(parent)
        self.grab_set()
        
        # Configurar color de fondo
        self.config(bg=COLORES['fondo_principal'])
        
        # Frame principal con Canvas para scroll
        main_frame = ttk.Frame(self)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Canvas con scrollbar
        canvas = tk.Canvas(main_frame, bg=COLORES['fondo_principal'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient='vertical', command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, padding='20')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Permitir scroll con rueda del mouse
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Grid layout
        canvas.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        scrollbar.grid(row=0, column=1, sticky='ns')
        main_frame.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # Título
        lbl_titulo = ttk.Label(
            scrollable_frame,
            text='Nuevo Trabajador' if not trabajador else 'Editar Trabajador',
            font=FUENTES['titulo']
        )
        lbl_titulo.pack(pady=15)
        
        # Separador
        ttk.Separator(scrollable_frame, orient='horizontal').pack(fill='x', pady=10)
        
        # Frame de campos
        frame_campos = ttk.Frame(scrollable_frame)
        frame_campos.pack(fill='both', expand=True, pady=10)
        
        # RUT
        lbl_rut = ttk.Label(frame_campos, text='RUT * (Formato automático)', font=FUENTES['normal'])
        lbl_rut.pack(anchor='w', pady=(10, 2))
        self.campo_rut = CampoRUT(frame_campos, font=FUENTES['normal'], width=50)
        self.campo_rut.pack(fill='x', pady=(0, 15))
        
        # Nombre
        lbl_nombre = ttk.Label(frame_campos, text='Nombre Completo *', font=FUENTES['normal'])
        lbl_nombre.pack(anchor='w', pady=(10, 2))
        self.campo_nombre = ttk.Entry(frame_campos, font=FUENTES['normal'], width=50)
        self.campo_nombre.pack(fill='x', pady=(0, 15))
        
        # Apellido Paterno
        lbl_ap_paterno = ttk.Label(frame_campos, text='Apellido Paterno', font=FUENTES['normal'])
        lbl_ap_paterno.pack(anchor='w', pady=(10, 2))
        self.campo_ap_paterno = ttk.Entry(frame_campos, font=FUENTES['normal'], width=50)
        self.campo_ap_paterno.pack(fill='x', pady=(0, 15))
        
        # Apellido Materno
        lbl_ap_materno = ttk.Label(frame_campos, text='Apellido Materno', font=FUENTES['normal'])
        lbl_ap_materno.pack(anchor='w', pady=(10, 2))
        self.campo_ap_materno = ttk.Entry(frame_campos, font=FUENTES['normal'], width=50)
        self.campo_ap_materno.pack(fill='x', pady=(0, 15))
        
        # Correo
        lbl_correo = ttk.Label(frame_campos, text='Correo', font=FUENTES['normal'])
        lbl_correo.pack(anchor='w', pady=(10, 2))
        self.campo_correo = ttk.Entry(frame_campos, font=FUENTES['normal'], width=50)
        self.campo_correo.pack(fill='x', pady=(0, 15))
        
        # Teléfono
        lbl_fono = ttk.Label(frame_campos, text='Teléfono', font=FUENTES['normal'])
        lbl_fono.pack(anchor='w', pady=(10, 2))
        self.campo_fono = ttk.Entry(frame_campos, font=FUENTES['normal'], width=50)
        self.campo_fono.pack(fill='x', pady=(0, 30))
        
        # Separador - Datos Laborales
        ttk.Separator(scrollable_frame, orient='horizontal').pack(fill='x', pady=10)
        
        lbl_laborales = ttk.Label(scrollable_frame, text='DATOS LABORALES', font=FUENTES['subtitulo'])
        lbl_laborales.pack(anchor='w', pady=(10, 10))
        
        frame_laborales = ttk.Frame(scrollable_frame)
        frame_laborales.pack(fill='both', expand=True, pady=10)
        
        # Cargo
        lbl_cargo = ttk.Label(frame_laborales, text='Cargo *', font=FUENTES['normal'])
        lbl_cargo.pack(anchor='w', pady=(10, 2))
        self.campo_cargo = ttk.Entry(frame_laborales, font=FUENTES['normal'], width=50)
        self.campo_cargo.pack(fill='x', pady=(0, 15))
        
        # Sueldo Base
        lbl_sueldo = ttk.Label(frame_laborales, text='Sueldo Base (CLP) *', font=FUENTES['normal'])
        lbl_sueldo.pack(anchor='w', pady=(10, 2))
        self.campo_sueldo = ttk.Entry(frame_laborales, font=FUENTES['normal'], width=50)
        self.campo_sueldo.pack(fill='x', pady=(0, 15))
        
        # Fecha Ingreso
        lbl_fecha = ttk.Label(frame_laborales, text='Fecha Ingreso (DD/MM/YYYY - Formato automático)', font=FUENTES['normal'])
        lbl_fecha.pack(anchor='w', pady=(10, 2))
        self.campo_fecha = CampoFecha(frame_laborales, font=FUENTES['normal'], width=50)
        self.campo_fecha.pack(fill='x', pady=(0, 30))
        
        # Separador - Datos Previsionales
        ttk.Separator(scrollable_frame, orient='horizontal').pack(fill='x', pady=10)
        
        lbl_previsionales = ttk.Label(scrollable_frame, text='DATOS PREVISIONALES', font=FUENTES['subtitulo'])
        lbl_previsionales.pack(anchor='w', pady=(10, 10))
        
        frame_previsionales = ttk.Frame(scrollable_frame)
        frame_previsionales.pack(fill='both', expand=True, pady=10)
        
        # AFP
        lbl_afp = ttk.Label(frame_previsionales, text='AFP (%)', font=FUENTES['normal'])
        lbl_afp.pack(anchor='w', pady=(10, 2))
        self.campo_afp = ttk.Entry(frame_previsionales, font=FUENTES['normal'], width=50)
        self.campo_afp.insert(0, '10.0')
        self.campo_afp.pack(fill='x', pady=(0, 15))
        
        # Salud
        lbl_salud = ttk.Label(frame_previsionales, text='Salud (%)', font=FUENTES['normal'])
        lbl_salud.pack(anchor='w', pady=(10, 2))
        self.campo_salud = ttk.Entry(frame_previsionales, font=FUENTES['normal'], width=50)
        self.campo_salud.insert(0, '7.0')
        self.campo_salud.pack(fill='x', pady=(0, 30))
        
        # Separador
        ttk.Separator(scrollable_frame, orient='horizontal').pack(fill='x', pady=10)
        
        # Frame botones
        frame_botones = ttk.Frame(scrollable_frame)
        frame_botones.pack(fill='x', pady=20)
        
        # Botón Guardar
        btn_guardar = tk.Button(
            frame_botones,
            text='💾 Guardar',
            command=self.guardar,
            font=FUENTES['normal'],
            bg=COLORES['azul_primario'],
            fg='white',
            padx=30,
            pady=10,
            relief='flat',
            cursor='hand2'
        )
        btn_guardar.pack(side='left', padx=5)
        
        # Botón Cancelar
        btn_cancelar = tk.Button(
            frame_botones,
            text='❌ Cancelar',
            command=self.destroy,
            font=FUENTES['normal'],
            bg=COLORES['rojo_error'],
            fg='white',
            padx=30,
            pady=10,
            relief='flat',
            cursor='hand2'
        )
        btn_cancelar.pack(side='left', padx=5)
        
        # Si es edición, cargar datos
        if trabajador:
            self.campo_rut.var.set(trabajador.get('rut', ''))
            self.campo_rut.config(state='readonly')
            self.campo_nombre.insert(0, trabajador.get('nombre', ''))
            self.campo_ap_paterno.insert(0, trabajador.get('ap_paterno', '') or '')
            self.campo_ap_materno.insert(0, trabajador.get('ap_materno', '') or '')
            self.campo_correo.insert(0, trabajador.get('correo', '') or '')
            self.campo_fono.insert(0, trabajador.get('fono', '') or '')
            self.campo_cargo.insert(0, trabajador.get('cargo', '') or '')
            self.campo_sueldo.insert(0, str(trabajador.get('sueldo_base', '')))
            self.campo_afp.delete(0, 'end')
            self.campo_afp.insert(0, str(trabajador.get('afp', '10.0')))
            self.campo_salud.delete(0, 'end')
            self.campo_salud.insert(0, str(trabajador.get('salud', '7.0')))
            fecha = trabajador.get('fecha_ingreso', '')
            if fecha:
                # Convertir de YYYY-MM-DD a DD/MM/YYYY si es necesario
                if '-' in fecha:
                    partes = fecha.split('-')
                    fecha = f"{partes[2]}/{partes[1]}/{partes[0]}"
            self.campo_fecha.var.set(fecha)
        
        # Centrar en pantalla
        self.update_idletasks()
        x = self.winfo_screenwidth() // 2 - self.winfo_width() // 2
        y = self.winfo_screenheight() // 2 - self.winfo_height() // 2
        self.geometry(f'+{x}+{y}')
        
        # Focus en primer campo
        self.campo_rut.focus()
    
    def guardar(self):
        """
        Valida y guarda los datos del trabajador en las tablas correctas
        """
        rut = self.campo_rut.var.get().strip()
        nombre = self.campo_nombre.get().strip()
        cargo = self.campo_cargo.get().strip()
        sueldo = self.campo_sueldo.get().strip()
        
        if not rut:
            messagebox.showerror('Error', 'Ingrese el RUT del trabajador')
            return
        
        if not nombre:
            messagebox.showerror('Error', 'Ingrese el nombre del trabajador')
            return
        
        if not cargo:
            messagebox.showerror('Error', 'Ingrese el cargo')
            return
        
        if not sueldo:
            messagebox.showerror('Error', 'Ingrese el sueldo base')
            return
        
        try:
            sueldo_float = float(sueldo)
            afp_float = float(self.campo_afp.get())
            salud_float = float(self.campo_salud.get())
        except ValueError:
            messagebox.showerror('Error', 'Ingrese valores numéricos válidos')
            return
        
        # Convertir fecha de DD/MM/YYYY a YYYY-MM-DD
        fecha_ingreso = self.campo_fecha.var.get().strip()
        if fecha_ingreso:
            try:
                partes = fecha_ingreso.split('/')
                if len(partes) == 3:
                    fecha_ingreso = f"{partes[2]}-{partes[1]}-{partes[0]}"
            except:
                fecha_ingreso = None
        else:
            fecha_ingreso = None
        
        # Datos para tabla TRABAJADOR
        datos_trabajador = {
            'rut': rut,
            'nombre': nombre,
            'ap_paterno': self.campo_ap_paterno.get().strip() or None,
            'ap_materno': self.campo_ap_materno.get().strip() or None,
            'correo': self.campo_correo.get().strip() or None,
            'fono': self.campo_fono.get().strip() or None,
            'empresa_codigo': self.empresa_codigo,
        }
        
        # Datos para tabla DATOS_LABORALES
        datos_laborales = {
            'trabajador_rut': rut,
            'cargo': cargo,
            'sueldo_base': sueldo_float,
            'fecha_contrato': fecha_ingreso,
        }
        
        # Datos para tabla DATOS_PREVISIONALES
        datos_previsionales = {
            'trabajador_rut': rut,
            'afp_cotiza_afc': afp_float,
            'modalidad_salud': salud_float,
        }
        
        try:
            if self.trabajador:
                # Actualizar trabajador existente
                update('trabajador', datos_trabajador, {'rut': rut})
                update('datos_laborales', datos_laborales, {'trabajador_rut': rut})
                update('datos_previsionales', datos_previsionales, {'trabajador_rut': rut})
                messagebox.showinfo('Éxito', 'Trabajador actualizado correctamente')
            else:
                # Crear nuevo trabajador
                insert('trabajador', datos_trabajador)
                insert('datos_laborales', datos_laborales)
                insert('datos_previsionales', datos_previsionales)
                messagebox.showinfo('Éxito', 'Trabajador creado correctamente')
            
            self.resultado = datos_trabajador
            self.destroy()
        except Exception as e:
            messagebox.showerror('Error', f'Error al guardar trabajador:\n{str(e)}')
