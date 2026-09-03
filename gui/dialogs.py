"""
Ventanas de diálogo modales
"""
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from gui.estilos import COLORES, FUENTES, aplicar_estilo_boton, aplicar_estilo_entrada
from gui.widgets import CampoFormulario
from database.models import fetch_one, insert, update
from calculos.validaciones import validar_rut
from datetime import datetime


class DialogoEmpresa(tk.Toplevel):
    """
    Diálogo para crear/editar empresa
    """
    def __init__(self, parent, empresa=None):
        super().__init__(parent)
        self.title('Empresa' if not empresa else 'Editar Empresa')
        self.geometry('500x600')
        self.empresa = empresa
        self.resultado = None
        
        # Frame principal
        frame_principal = ttk.Frame(self, padding='20')
        frame_principal.pack(fill='both', expand=True)
        
        # Campos
        self.campo_rut = CampoFormulario(frame_principal, 'RUT', obligatorio=True)
        self.campo_rut.pack(fill='x', pady=10)
        
        self.campo_razon = CampoFormulario(frame_principal, 'Razón Social', obligatorio=True)
        self.campo_razon.pack(fill='x', pady=10)
        
        self.campo_ciudad = CampoFormulario(frame_principal, 'Ciudad')
        self.campo_ciudad.pack(fill='x', pady=10)
        
        self.campo_region = CampoFormulario(frame_principal, 'Región')
        self.campo_region.pack(fill='x', pady=10)
        
        self.campo_correo = CampoFormulario(frame_principal, 'Correo')
        self.campo_correo.pack(fill='x', pady=10)
        
        self.campo_fono = CampoFormulario(frame_principal, 'Teléfono')
        self.campo_fono.pack(fill='x', pady=10)
        
        # Frame botones
        frame_botones = ttk.Frame(frame_principal)
        frame_botones.pack(fill='x', pady=20)
        
        btn_guardar = tk.Button(frame_botones, text='Guardar', command=self.guardar)
        aplicar_estilo_boton(btn_guardar, 'primario')
        btn_guardar.pack(side='left', padx=5)
        
        btn_cancelar = tk.Button(frame_botones, text='Cancelar', command=self.destroy)
        aplicar_estilo_boton(btn_cancelar, 'secundario')
        btn_cancelar.pack(side='left', padx=5)
        
        # Si es edición, cargar datos
        if empresa:
            self.campo_rut.establecer_valor(empresa.get('rut', ''))
            self.campo_razon.establecer_valor(empresa.get('razon_social', ''))
            self.campo_ciudad.establecer_valor(empresa.get('ciudad', ''))
            self.campo_region.establecer_valor(empresa.get('region', ''))
            self.campo_correo.establecer_valor(empresa.get('correo', ''))
            self.campo_fono.establecer_valor(empresa.get('fono', ''))
            self.campo_rut.entrada.config(state='readonly')
    
    def guardar(self):
        """
        Valida y guarda los datos
        """
        # Validar
        if not self.campo_rut.validar() or not self.campo_razon.validar():
            return
        
        rut = self.campo_rut.obtener_valor()
        if not validar_rut(rut):
            messagebox.showerror('Error', 'RUT inválido')
            return
        
        datos = {
            'rut': rut,
            'razon_social': self.campo_razon.obtener_valor(),
            'ciudad': self.campo_ciudad.obtener_valor(),
            'region': self.campo_region.obtener_valor(),
            'correo': self.campo_correo.obtener_valor(),
            'fono': self.campo_fono.obtener_valor(),
        }
        
        try:
            if self.empresa:
                from database.models import update
                update('empresa', datos, {'rut': self.empresa['rut']})
                messagebox.showinfo('Éxito', 'Empresa actualizada')
            else:
                from database.models import insert
                insert('empresa', datos)
                messagebox.showinfo('Éxito', 'Empresa creada')
            
            self.resultado = datos
            self.destroy()
        except Exception as e:
            messagebox.showerror('Error', f'Error al guardar: {str(e)}')


class DialogoTrabajador(tk.Toplevel):
    """
    Diálogo para crear/editar trabajador
    """
    def __init__(self, parent, trabajador=None):
        super().__init__(parent)
        self.title('Trabajador' if not trabajador else 'Editar Trabajador')
        self.geometry('600x800')
        self.trabajador = trabajador
        self.resultado = None
        
        # Notebook con pestañas
        notebook = ttk.Notebook(self)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Pestaña 1: Datos Personales
        frame_personal = ttk.Frame(notebook, padding='20')
        notebook.add(frame_personal, text='Datos Personales')
        
        self.campo_rut = CampoFormulario(frame_personal, 'RUT', obligatorio=True)
        self.campo_rut.pack(fill='x', pady=10)
        
        self.campo_nombre = CampoFormulario(frame_personal, 'Nombre', obligatorio=True)
        self.campo_nombre.pack(fill='x', pady=10)
        
        self.campo_ap_paterno = CampoFormulario(frame_personal, 'Apellido Paterno')
        self.campo_ap_paterno.pack(fill='x', pady=10)
        
        self.campo_ap_materno = CampoFormulario(frame_personal, 'Apellido Materno')
        self.campo_ap_materno.pack(fill='x', pady=10)
        
        self.campo_correo = CampoFormulario(frame_personal, 'Correo')
        self.campo_correo.pack(fill='x', pady=10)
        
        self.campo_fono = CampoFormulario(frame_personal, 'Teléfono')
        self.campo_fono.pack(fill='x', pady=10)
        
        # Pestaña 2: Datos Laborales
        frame_laboral = ttk.Frame(notebook, padding='20')
        notebook.add(frame_laboral, text='Datos Laborales')
        
        self.campo_sueldo = CampoFormulario(frame_laboral, 'Sueldo Base', tipo='monto', obligatorio=True)
        self.campo_sueldo.pack(fill='x', pady=10)
        
        self.campo_cargo = CampoFormulario(frame_laboral, 'Cargo')
        self.campo_cargo.pack(fill='x', pady=10)
        
        self.campo_fecha_contrato = CampoFormulario(frame_laboral, 'Fecha Contrato (DD-MM-YYYY)')
        self.campo_fecha_contrato.pack(fill='x', pady=10)
        
        self.campo_horas = CampoFormulario(frame_laboral, 'Horas Semanales')
        self.campo_horas.pack(fill='x', pady=10)
        
        # Pestaña 3: Datos Previsionales
        frame_previsional = ttk.Frame(notebook, padding='20')
        notebook.add(frame_previsional, text='Datos Previsionales')
        
        ttk.Label(frame_previsional, text='AFP', font=FUENTES['normal']).pack(anchor='w', pady=(5, 2))
        self.combo_afp = ttk.Combobox(frame_previsional, values=['EMPART', 'SSS', 'CAPITAL', 'CUPRUM', 'HABITAT', 'MODELO', 'PLANVITAL', 'PROVIDA', 'UNO'])
        self.combo_afp.pack(fill='x', pady=(0, 10))
        
        ttk.Label(frame_previsional, text='Isapre', font=FUENTES['normal']).pack(anchor='w', pady=(5, 2))
        self.combo_isapre = ttk.Combobox(frame_previsional, values=['FONASA', 'VIDATRES', 'CONSALUD', 'BANMEDICA', 'MASVIDA', 'CRUZBLANCA'])
        self.combo_isapre.pack(fill='x', pady=(0, 10))
        
        self.campo_modalidad = CampoFormulario(frame_previsional, 'Modalidad Salud (7%/UF)')
        self.campo_modalidad.pack(fill='x', pady=10)
        
        # Frame botones
        frame_botones = ttk.Frame(self)
        frame_botones.pack(fill='x', pady=10, padx=10)
        
        btn_guardar = tk.Button(frame_botones, text='Guardar', command=self.guardar)
        aplicar_estilo_boton(btn_guardar, 'primario')
        btn_guardar.pack(side='left', padx=5)
        
        btn_cancelar = tk.Button(frame_botones, text='Cancelar', command=self.destroy)
        aplicar_estilo_boton(btn_cancelar, 'secundario')
        btn_cancelar.pack(side='left', padx=5)
    
    def guardar(self):
        """
        Valida y guarda los datos
        """
        if not self.campo_rut.validar() or not self.campo_nombre.validar():
            return
        
        try:
            rut = self.campo_rut.obtener_valor()
            if not validar_rut(rut):
                messagebox.showerror('Error', 'RUT inválido')
                return
            
            datos = {
                'rut': rut,
                'nombre': self.campo_nombre.obtener_valor(),
                'ap_paterno': self.campo_ap_paterno.obtener_valor(),
                'ap_materno': self.campo_ap_materno.obtener_valor(),
                'correo': self.campo_correo.obtener_valor(),
                'fono': self.campo_fono.obtener_valor(),
            }
            
            if self.trabajador:
                update('trabajador', datos, {'rut': rut})
            else:
                datos['empresa_codigo'] = 1  # Por defecto
                insert('trabajador', datos)
                
                # Crear datos laborales
                datos_laborales = {
                    'trabajador_rut': rut,
                    'sueldo_base': float(self.campo_sueldo.obtener_valor()),
                    'cargo': self.campo_cargo.obtener_valor(),
                    'fecha_contrato': self.campo_fecha_contrato.obtener_valor(),
                    'horas_semanales': int(self.campo_horas.obtener_valor() or 45),
                    'dias_laborales_semana': 5,
                    'sueldo_tipo': 'Mensual',
                    'aplica_sis': 'S',
                }
                insert('datos_laborales', datos_laborales)
                
                # Crear datos previsionales
                datos_previsionales = {
                    'trabajador_rut': rut,
                    'afp_codigo': self.combo_afp.get(),
                    'isapre_codigo': self.combo_isapre.get(),
                    'modalidad_salud': self.campo_modalidad.obtener_valor(),
                    'cotizacion_pactada': 7.0,
                    'tipo_trabajador': 'Activo No Pensionado',
                }
                insert('datos_previsionales', datos_previsionales)
            
            messagebox.showinfo('Éxito', 'Trabajador guardado')
            self.resultado = datos
            self.destroy()
        except Exception as e:
            messagebox.showerror('Error', f'Error al guardar: {str(e)}')
