"""
Ventana principal de la aplicación
"""
import tkinter as tk
from tkinter import ttk, messagebox
from gui.estilos import COLORES, FUENTES, aplicar_estilo_boton
from gui.widgets import TablaDatos, BarraEstado
from gui.dialogs import DialogoEmpresa, DialogoTrabajador
from database.models import fetch_all, fetch_one, delete
from calculos.impuesto_unico import calcular_impuesto_unico
from calculos.previsiones import calcular_afp, calcular_salud
from modules.liquidacion import calcular_liquidacion, guardar_liquidacion


class VentanaPrincipal(ttk.Frame):
    """
    Ventana principal de la aplicación
    """
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.root.config(bg=COLORES['fondo_principal'])
        self.pack(fill='both', expand=True)
        
        # Crear interfaz
        self._crear_menu()
        self._crear_sidebar()
        self._crear_area_contenido()
        self._crear_barra_estado()
        
        # Mostrar panel de inicio
        self.mostrar_empresas()
    
    def _crear_menu(self):
        """
        Crea el menú superior
        """
        menubar = tk.Menu(self.root, bg=COLORES['azul_primario'], fg='white')
        self.root.config(menu=menubar)
        
        # Menú Archivo
        menu_archivo = tk.Menu(menubar, tearoff=0, bg=COLORES['fondo_secundario'])
        menubar.add_cascade(label='Archivo', menu=menu_archivo)
        menu_archivo.add_command(label='Salir', command=self.root.quit)
        
        # Menú Gestión
        menu_gestion = tk.Menu(menubar, tearoff=0, bg=COLORES['fondo_secundario'])
        menubar.add_cascade(label='Gestión', menu=menu_gestion)
        menu_gestion.add_command(label='Empresas', command=self.mostrar_empresas)
        menu_gestion.add_command(label='Trabajadores', command=self.mostrar_trabajadores)
        menu_gestion.add_separator()
        menu_gestion.add_command(label='Liquidaciones', command=self.mostrar_liquidaciones)
        
        # Menú Ayuda
        menu_ayuda = tk.Menu(menubar, tearoff=0, bg=COLORES['fondo_secundario'])
        menubar.add_cascade(label='Ayuda', menu=menu_ayuda)
        menu_ayuda.add_command(label='Acerca de', command=self._mostrar_acerca_de)
    
    def _crear_sidebar(self):
        """
        Crea el panel lateral de navegación
        """
        self.sidebar = ttk.Frame(self)
        self.sidebar.pack(side='left', fill='y', padx=10, pady=10)
        
        # Título
        lbl_titulo = ttk.Label(
            self.sidebar,
            text='SISTEMA',
            font=FUENTES['titulo']
        )
        lbl_titulo.pack(pady=20)
        
        # Botones de navegación
        botones = [
            ('Empresas', self.mostrar_empresas),
            ('Trabajadores', self.mostrar_trabajadores),
            ('Instituciones', self.mostrar_instituciones),
            ('Liquidaciones', self.mostrar_liquidaciones),
        ]
        
        for texto, comando in botones:
            btn = tk.Button(
                self.sidebar,
                text=texto,
                width=15,
                command=comando,
                bg=COLORES['azul_primario'],
                fg='white',
                font=FUENTES['normal'],
                relief=tk.FLAT,
                cursor='hand2',
                pady=10
            )
            btn.pack(pady=5, fill='x')
    
    def _crear_area_contenido(self):
        """
        Crea el área principal de contenido
        """
        self.frame_contenido = ttk.Frame(self)
        self.frame_contenido.pack(side='right', fill='both', expand=True, padx=10, pady=10)
    
    def _crear_barra_estado(self):
        """
        Crea la barra de estado
        """
        self.barra_estado = BarraEstado(self.root)
        self.barra_estado.pack(side='bottom', fill='x')
    
    def _limpiar_contenido(self):
        """
        Limpia el área de contenido
        """
        for widget in self.frame_contenido.winfo_children():
            widget.destroy()
    
    def mostrar_empresas(self):
        """
        Muestra el panel de empresas
        """
        self._limpiar_contenido()
        self.barra_estado.actualizar_estado('Gestión de Empresas')
        
        # Título
        lbl_titulo = ttk.Label(
            self.frame_contenido,
            text='Gestión de Empresas',
            font=FUENTES['titulo']
        )
        lbl_titulo.pack(pady=10)
        
        # Frame botones
        frame_botones = ttk.Frame(self.frame_contenido)
        frame_botones.pack(fill='x', pady=10)
        
        btn_nueva = tk.Button(
            frame_botones,
            text='+ Nueva Empresa',
            command=self._crear_empresa
        )
        aplicar_estilo_boton(btn_nueva, 'primario')
        btn_nueva.pack(side='left', padx=5)
        
        btn_eliminar = tk.Button(
            frame_botones,
            text='Eliminar',
            command=self._eliminar_empresa
        )
        aplicar_estilo_boton(btn_eliminar, 'peligro')
        btn_eliminar.pack(side='left', padx=5)
        
        # Tabla de empresas
        empresas = fetch_all('empresa')
        if empresas:
            columnas = ['codigo', 'rut', 'razon_social', 'ciudad', 'region']
            tabla = TablaDatos(self.frame_contenido, columnas, empresas)
            tabla.pack(fill='both', expand=True, pady=10)
            self.tabla_actual = tabla
        else:
            lbl_vacio = ttk.Label(
                self.frame_contenido,
                text='No hay empresas registradas',
                font=FUENTES['normal']
            )
            lbl_vacio.pack(pady=50)
    
    def _crear_empresa(self):
        """
        Abre diálogo para crear empresa
        """
        dialogo = DialogoEmpresa(self.root)
        self.root.wait_window(dialogo)
        self.mostrar_empresas()
    
    def _eliminar_empresa(self):
        """
        Elimina la empresa seleccionada
        """
        if not hasattr(self, 'tabla_actual'):
            messagebox.showwarning('Advertencia', 'Seleccione una empresa')
            return
        
        empresa = self.tabla_actual.obtener_seleccion()
        if not empresa:
            messagebox.showwarning('Advertencia', 'Seleccione una empresa')
            return
        
        if messagebox.askyesno('Confirmar', f'¿Eliminar {empresa["razon_social"]}?'):
            delete('empresa', {'codigo': empresa['codigo']})
            self.mostrar_empresas()
    
    def mostrar_trabajadores(self):
        """
        Muestra el panel de trabajadores
        """
        self._limpiar_contenido()
        self.barra_estado.actualizar_estado('Gestión de Trabajadores')
        
        # Título
        lbl_titulo = ttk.Label(
            self.frame_contenido,
            text='Gestión de Trabajadores',
            font=FUENTES['titulo']
        )
        lbl_titulo.pack(pady=10)
        
        # Frame botones
        frame_botones = ttk.Frame(self.frame_contenido)
        frame_botones.pack(fill='x', pady=10)
        
        btn_nuevo = tk.Button(
            frame_botones,
            text='+ Nuevo Trabajador',
            command=self._crear_trabajador
        )
        aplicar_estilo_boton(btn_nuevo, 'primario')
        btn_nuevo.pack(side='left', padx=5)
        
        # Tabla de trabajadores
        trabajadores = fetch_all('trabajador')
        if trabajadores:
            columnas = ['rut', 'nombre', 'ap_paterno', 'ap_materno']
            tabla = TablaDatos(self.frame_contenido, columnas, trabajadores)
            tabla.pack(fill='both', expand=True, pady=10)
            self.tabla_actual = tabla
        else:
            lbl_vacio = ttk.Label(
                self.frame_contenido,
                text='No hay trabajadores registrados',
                font=FUENTES['normal']
            )
            lbl_vacio.pack(pady=50)
    
    def _crear_trabajador(self):
        """
        Abre diálogo para crear trabajador
        """
        dialogo = DialogoTrabajador(self.root)
        self.root.wait_window(dialogo)
        self.mostrar_trabajadores()
    
    def mostrar_instituciones(self):
        """
        Muestra instituciones previsionales
        """
        self._limpiar_contenido()
        self.barra_estado.actualizar_estado('Instituciones Previsionales')
        
        # Título
        lbl_titulo = ttk.Label(
            self.frame_contenido,
            text='Instituciones Previsionales',
            font=FUENTES['titulo']
        )
        lbl_titulo.pack(pady=10)
        
        # Notebook con instituciones
        notebook = ttk.Notebook(self.frame_contenido)
        notebook.pack(fill='both', expand=True)
        
        # AFP
        afps = fetch_all('afp')
        if afps:
            frame_afp = ttk.Frame(notebook)
            notebook.add(frame_afp, text='AFP')
            tabla_afp = TablaDatos(frame_afp, ['codigo', 'nombre', 'factor_cotizacion'], afps)
            tabla_afp.pack(fill='both', expand=True)
        
        # Isapres
        isapres = fetch_all('isapre')
        if isapres:
            frame_isapre = ttk.Frame(notebook)
            notebook.add(frame_isapre, text='Isapre')
            tabla_isapre = TablaDatos(frame_isapre, ['codigo', 'nombre'], isapres)
            tabla_isapre.pack(fill='both', expand=True)
    
    def mostrar_liquidaciones(self):
        """
        Muestra panel de liquidaciones
        """
        self._limpiar_contenido()
        self.barra_estado.actualizar_estado('Liquidaciones de Sueldo')
        
        # Título
        lbl_titulo = ttk.Label(
            self.frame_contenido,
            text='Liquidaciones de Sueldo',
            font=FUENTES['titulo']
        )
        lbl_titulo.pack(pady=10)
        
        # Frame datos
        frame_datos = ttk.LabelFrame(self.frame_contenido, text='Seleccionar Trabajador')
        frame_datos.pack(fill='x', pady=10, padx=10)
        
        ttk.Label(frame_datos, text='Trabajador:').pack(side='left', padx=5, pady=5)
        trabajadores = fetch_all('trabajador')
        nombres = [f"{t['rut']} - {t['nombre']}" for t in trabajadores]
        combo_trabajador = ttk.Combobox(frame_datos, values=nombres, state='readonly')
        combo_trabajador.pack(side='left', padx=5, pady=5, fill='x', expand=True)
        
        ttk.Label(frame_datos, text='Año:').pack(side='left', padx=5, pady=5)
        entry_anio = ttk.Entry(frame_datos, width=5)
        entry_anio.pack(side='left', padx=5, pady=5)
        
        ttk.Label(frame_datos, text='Mes:').pack(side='left', padx=5, pady=5)
        entry_mes = ttk.Entry(frame_datos, width=5)
        entry_mes.pack(side='left', padx=5, pady=5)
        
        def calcular():
            if not combo_trabajador.get():
                messagebox.showwarning('Advertencia', 'Seleccione un trabajador')
                return
            
            try:
                rut = combo_trabajador.get().split(' - ')[0]
                anio = int(entry_anio.get())
                mes = int(entry_mes.get())
                
                trabajador = fetch_one('trabajador', {'rut': rut})
                liq = calcular_liquidacion(rut, trabajador['empresa_codigo'], anio, mes)
                guardar_liquidacion(liq)
                
                # Mostrar resumen
                resumen = f"""Liquidación de Sueldo
                
Trabajador: {trabajador['nombre']}
Año-Mes: {mes}/{anio}

Sueldo Base: ${liq['sueldo_base']:,.0f}
Total Haberes: ${liq['total_haberes']:,.0f}
AFP: ${liq['monto_afp']:,.0f}
Salud: ${liq['monto_salud']:,.0f}
Impuesto Único: ${liq['impuesto_unico']:,.0f}
Total Descuentos: ${liq['total_descuentos']:,.0f}
Sueldo Líquido: ${liq['sueldo_liquido']:,.0f}"""
                
                messagebox.showinfo('Liquidación Calculada', resumen)
            except Exception as e:
                messagebox.showerror('Error', str(e))
        
        btn_calcular = tk.Button(
            frame_datos,
            text='Calcular',
            command=calcular
        )
        aplicar_estilo_boton(btn_calcular, 'primario')
        btn_calcular.pack(side='left', padx=5, pady=5)
    
    def _mostrar_acerca_de(self):
        """
        Muestra ventana de ayuda
        """
        messagebox.showinfo(
            'Acerca de',
            'Sistema Profesional de Remuneraciones - Chile\nV1.0\n\nGestión integral de nómina y liquidación de sueldo'
        )
