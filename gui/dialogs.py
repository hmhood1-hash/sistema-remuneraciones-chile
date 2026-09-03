"""
Diálogos para crear/editar datos en la aplicación
"""
import tkinter as tk
from tkinter import ttk, messagebox
from gui.estilos import COLORES, FUENTES, aplicar_estilo_boton
from gui.widgets import CampoFormulario
from database.models import insert, update, fetch_one
from utils.validaciones import validar_rut


class DialogoEmpresa(tk.Toplevel):
    """
    Diálogo para crear/editar empresa con campos visibles
    """
    def __init__(self, parent, empresa=None):
        super().__init__(parent)
        self.title('Nueva Empresa' if not empresa else 'Editar Empresa')
        self.geometry('600x700')
        self.resizable(False, False)
        self.empresa = empresa
        self.resultado = None
        
        # Hacer que el diálogo sea modal
        self.transient(parent)
        self.grab_set()
        
        # Configurar color de fondo
        self.config(bg=COLORES['fondo_principal'])
        
        # Frame principal con scrollbar
        main_frame = ttk.Frame(self, padding='20')
        main_frame.pack(fill='both', expand=True)
        
        # Título del diálogo
        lbl_titulo = ttk.Label(
            main_frame,
            text='Nueva Empresa' if not empresa else 'Editar Empresa',
            font=FUENTES['titulo']
        )
        lbl_titulo.pack(pady=15)
        
        # Separador
        ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=10)
        
        # Frame de campos
        frame_campos = ttk.Frame(main_frame)
        frame_campos.pack(fill='both', expand=True, pady=10)
        
        # RUT
        lbl_rut = ttk.Label(frame_campos, text='RUT *', font=FUENTES['etiqueta'])
        lbl_rut.pack(anchor='w', pady=(10, 0))
        self.campo_rut = ttk.Entry(frame_campos, font=FUENTES['normal'], width=40)
        self.campo_rut.pack(fill='x', pady=(0, 15))
        
        # Razón Social
        lbl_razon = ttk.Label(frame_campos, text='Razón Social *', font=FUENTES['etiqueta'])
        lbl_razon.pack(anchor='w', pady=(10, 0))
        self.campo_razon = ttk.Entry(frame_campos, font=FUENTES['normal'], width=40)
        self.campo_razon.pack(fill='x', pady=(0, 15))
        
        # Ciudad
        lbl_ciudad = ttk.Label(frame_campos, text='Ciudad', font=FUENTES['etiqueta'])
        lbl_ciudad.pack(anchor='w', pady=(10, 0))
        self.campo_ciudad = ttk.Entry(frame_campos, font=FUENTES['normal'], width=40)
        self.campo_ciudad.pack(fill='x', pady=(0, 15))
        
        # Región
        lbl_region = ttk.Label(frame_campos, text='Región', font=FUENTES['etiqueta'])
        lbl_region.pack(anchor='w', pady=(10, 0))
        self.campo_region = ttk.Entry(frame_campos, font=FUENTES['normal'], width=40)
        self.campo_region.pack(fill='x', pady=(0, 15))
        
        # Correo
        lbl_correo = ttk.Label(frame_campos, text='Correo', font=FUENTES['etiqueta'])
        lbl_correo.pack(anchor='w', pady=(10, 0))
        self.campo_correo = ttk.Entry(frame_campos, font=FUENTES['normal'], width=40)
        self.campo_correo.pack(fill='x', pady=(0, 15))
        
        # Teléfono
        lbl_fono = ttk.Label(frame_campos, text='Teléfono', font=FUENTES['etiqueta'])
        lbl_fono.pack(anchor='w', pady=(10, 0))
        self.campo_fono = ttk.Entry(frame_campos, font=FUENTES['normal'], width=40)
        self.campo_fono.pack(fill='x', pady=(0, 15))
        
        # Separador antes de botones
        ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=10)
        
        # Frame botones
        frame_botones = ttk.Frame(main_frame)
        frame_botones.pack(fill='x', pady=20)
        
        # Botón Guardar
        btn_guardar = tk.Button(
            frame_botones,
            text='💾 Guardar',
            command=self.guardar,
            font=FUENTES['boton'],
            bg=COLORES['azul_primario'],
            fg='white',
            padx=20,
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
            font=FUENTES['boton'],
            bg=COLORES['rojo_primario'],
            fg='white',
            padx=20,
            pady=10,
            relief='flat',
            cursor='hand2'
        )
        btn_cancelar.pack(side='left', padx=5)
        
        # Si es edición, cargar datos
        if empresa:
            self.campo_rut.insert(0, empresa.get('rut', ''))
            self.campo_rut.config(state='readonly')
            self.campo_razon.insert(0, empresa.get('razon_social', ''))
            self.campo_ciudad.insert(0, empresa.get('ciudad', ''))
            self.campo_region.insert(0, empresa.get('region', ''))
            self.campo_correo.insert(0, empresa.get('correo', ''))
            self.campo_fono.insert(0, empresa.get('fono', ''))
        
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
        rut = self.campo_rut.get().strip()
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
            'ciudad': self.campo_ciudad.get().strip() or None,
            'region': self.campo_region.get().strip() or None,
            'correo': self.campo_correo.get().strip() or None,
            'fono': self.campo_fono.get().strip() or None,
        }
        
        try:
            if self.empresa:
                # Actualizar empresa existente
                update('empresas', datos, f"rut = '{rut}'")
                messagebox.showinfo('Éxito', 'Empresa actualizada correctamente')
            else:
                # Crear nueva empresa
                insert('empresas', datos)
                messagebox.showinfo('Éxito', 'Empresa creada correctamente')
            
            self.resultado = datos
            self.destroy()
        except Exception as e:
            messagebox.showerror('Error', f'Error al guardar empresa:\n{str(e)}')


class DialogoTrabajador(tk.Toplevel):
    """
    Diálogo para crear/editar trabajador
    """
    def __init__(self, parent, trabajador=None, empresa_rut=None):
        super().__init__(parent)
        self.title('Nuevo Trabajador' if not trabajador else 'Editar Trabajador')
        self.geometry('600x800')
        self.resizable(False, False)
        self.trabajador = trabajador
        self.empresa_rut = empresa_rut
        self.resultado = None
        
        # Hacer que el diálogo sea modal
        self.transient(parent)
        self.grab_set()
        
        # Configurar color de fondo
        self.config(bg=COLORES['fondo_principal'])
        
        # Frame principal
        main_frame = ttk.Frame(self, padding='20')
        main_frame.pack(fill='both', expand=True)
        
        # Título
        lbl_titulo = ttk.Label(
            main_frame,
            text='Nuevo Trabajador' if not trabajador else 'Editar Trabajador',
            font=FUENTES['titulo']
        )
        lbl_titulo.pack(pady=15)
        
        # Separador
        ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=10)
        
        # Frame de campos
        frame_campos = ttk.Frame(main_frame)
        frame_campos.pack(fill='both', expand=True, pady=10)
        
        # RUT
        lbl_rut = ttk.Label(frame_campos, text='RUT *', font=FUENTES['etiqueta'])
        lbl_rut.pack(anchor='w', pady=(10, 0))
        self.campo_rut = ttk.Entry(frame_campos, font=FUENTES['normal'], width=40)
        self.campo_rut.pack(fill='x', pady=(0, 15))
        
        # Nombre
        lbl_nombre = ttk.Label(frame_campos, text='Nombre Completo *', font=FUENTES['etiqueta'])
        lbl_nombre.pack(anchor='w', pady=(10, 0))
        self.campo_nombre = ttk.Entry(frame_campos, font=FUENTES['normal'], width=40)
        self.campo_nombre.pack(fill='x', pady=(0, 15))
        
        # Cargo
        lbl_cargo = ttk.Label(frame_campos, text='Cargo *', font=FUENTES['etiqueta'])
        lbl_cargo.pack(anchor='w', pady=(10, 0))
        self.campo_cargo = ttk.Entry(frame_campos, font=FUENTES['normal'], width=40)
        self.campo_cargo.pack(fill='x', pady=(0, 15))
        
        # Sueldo Base
        lbl_sueldo = ttk.Label(frame_campos, text='Sueldo Base (CLP) *', font=FUENTES['etiqueta'])
        lbl_sueldo.pack(anchor='w', pady=(10, 0))
        self.campo_sueldo = ttk.Entry(frame_campos, font=FUENTES['normal'], width=40)
        self.campo_sueldo.pack(fill='x', pady=(0, 15))
        
        # AFP
        lbl_afp = ttk.Label(frame_campos, text='AFP (%)', font=FUENTES['etiqueta'])
        lbl_afp.pack(anchor='w', pady=(10, 0))
        self.campo_afp = ttk.Entry(frame_campos, font=FUENTES['normal'], width=40)
        self.campo_afp.insert(0, '10.0')
        self.campo_afp.pack(fill='x', pady=(0, 15))
        
        # Salud
        lbl_salud = ttk.Label(frame_campos, text='Salud (%)', font=FUENTES['etiqueta'])
        lbl_salud.pack(anchor='w', pady=(10, 0))
        self.campo_salud = ttk.Entry(frame_campos, font=FUENTES['normal'], width=40)
        self.campo_salud.insert(0, '7.0')
        self.campo_salud.pack(fill='x', pady=(0, 15))
        
        # Fecha Ingreso
        lbl_fecha = ttk.Label(frame_campos, text='Fecha Ingreso (YYYY-MM-DD)', font=FUENTES['etiqueta'])
        lbl_fecha.pack(anchor='w', pady=(10, 0))
        self.campo_fecha = ttk.Entry(frame_campos, font=FUENTES['normal'], width=40)
        self.campo_fecha.pack(fill='x', pady=(0, 15))
        
        # Separador
        ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=10)
        
        # Frame botones
        frame_botones = ttk.Frame(main_frame)
        frame_botones.pack(fill='x', pady=20)
        
        # Botón Guardar
        btn_guardar = tk.Button(
            frame_botones,
            text='💾 Guardar',
            command=self.guardar,
            font=FUENTES['boton'],
            bg=COLORES['azul_primario'],
            fg='white',
            padx=20,
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
            font=FUENTES['boton'],
            bg=COLORES['rojo_primario'],
            fg='white',
            padx=20,
            pady=10,
            relief='flat',
            cursor='hand2'
        )
        btn_cancelar.pack(side='left', padx=5)
        
        # Si es edición, cargar datos
        if trabajador:
            self.campo_rut.insert(0, trabajador.get('rut', ''))
            self.campo_rut.config(state='readonly')
            self.campo_nombre.insert(0, trabajador.get('nombre', ''))
            self.campo_cargo.insert(0, trabajador.get('cargo', ''))
            self.campo_sueldo.insert(0, str(trabajador.get('sueldo_base', '')))
            self.campo_afp.delete(0, 'end')
            self.campo_afp.insert(0, str(trabajador.get('afp', '10.0')))
            self.campo_salud.delete(0, 'end')
            self.campo_salud.insert(0, str(trabajador.get('salud', '7.0')))
            self.campo_fecha.insert(0, trabajador.get('fecha_ingreso', ''))
        
        # Centrar en pantalla
        self.update_idletasks()
        x = self.winfo_screenwidth() // 2 - self.winfo_width() // 2
        y = self.winfo_screenheight() // 2 - self.winfo_height() // 2
        self.geometry(f'+{x}+{y}')
        
        # Focus en primer campo
        self.campo_rut.focus()
    
    def guardar(self):
        """
        Valida y guarda los datos del trabajador
        """
        rut = self.campo_rut.get().strip()
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
        
        datos = {
            'rut': rut,
            'nombre': nombre,
            'cargo': cargo,
            'sueldo_base': sueldo_float,
            'afp': afp_float,
            'salud': salud_float,
            'fecha_ingreso': self.campo_fecha.get().strip() or None,
            'empresa_rut': self.empresa_rut,
        }
        
        try:
            if self.trabajador:
                update('trabajadores', datos, f"rut = '{rut}'")
                messagebox.showinfo('Éxito', 'Trabajador actualizado correctamente')
            else:
                insert('trabajadores', datos)
                messagebox.showinfo('Éxito', 'Trabajador creado correctamente')
            
            self.resultado = datos
            self.destroy()
        except Exception as e:
            messagebox.showerror('Error', f'Error al guardar trabajador:\n{str(e)}')
