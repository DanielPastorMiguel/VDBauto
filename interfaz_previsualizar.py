import customtkinter as ctk
import tkinter as tk
import configuracion
import utiles
import utiles_interfaz
from tkinter import filedialog as fd

class InterfazPrevisualizar(ctk.CTkFrame):

    conf = configuracion.Configuracion()

    def __init__(self, parent):
        ctk.CTkFrame.__init__(self, parent)
        self.parent = parent

    def iniciar_contenedor(self):
        texto_previsualizacion = ctk.CTkLabel(self, text="Previsualización", font=("Arial", 30))
        texto_previsualizacion.grid(row=0, column=0, padx= 60, pady=30, sticky='n')

        #Creamos un frame para el canvas con no-cero filas y columnas
        frame_canvas = tk.Frame(self)
        frame_canvas.grid(row=1, column=0, padx= 60, pady=(15, 15))
        frame_canvas.grid_rowconfigure(0, weight=1)
        frame_canvas.grid_columnconfigure(0, weight=1)

        frame_canvas.grid_propagate(False)

        #Añadimos el canvas al frame
        canvas = tk.Canvas(frame_canvas)
        canvas.grid(row=0, column=0, sticky="news")

        #Añadimos la barra de scroll al canvas
        vsb = tk.Scrollbar(frame_canvas, orient="horizontal", command=canvas.xview)
        vsb.grid(row=1, column=0, sticky='we')
        canvas.configure(xscrollcommand=vsb.set)

        #Creamos un frame para que contenga los botones
        frame_buttons = tk.Frame(canvas)
        canvas.create_window((0, 0), window=frame_buttons, anchor='nw')

        datos_tabla = self.get_datos_tabla() #Va a ser una lista con dos listas siempre (es decir, dos filas, una de indices y otra con los valores. Ambas van a tener la misma longitud siempre)

        rows = 3
        columns = len(datos_tabla[0])

        buttons = [[tk.Button() for j in range(columns)] for i in range(rows)]
        for j in range(0, columns):
            buttons[0][j] = tk.Button(frame_buttons, text=(datos_tabla[0][j]), font=ctk.CTkFont(family="Arial", size=14, slant="italic"))
            buttons[0][j].grid(row=0, column=j, sticky='news')
            buttons[1][j] = tk.Button(frame_buttons, text=(datos_tabla[1][j]), font=ctk.CTkFont(family="Arial", size=14, weight="bold", underline=True))
            buttons[1][j].grid(row=1, column=j, sticky='news')
            buttons[2][j] = tk.Button(frame_buttons, text=(datos_tabla[2][j]), font=("Arial", 12))
            buttons[2][j].grid(row=2, column=j, sticky='news')

        #Para que tkitner calcule el tamaño de los botones
        frame_buttons.update_idletasks()

        #Cambiamos el tamaño para que muestre las primeras 5 columnas
        first5columns_width = 500
        first5rows_height = buttons[0][0].winfo_height()*3
        frame_canvas.config(width=first5columns_width + vsb.winfo_width(),
                            height=first5rows_height + vsb.winfo_height() + 2)

        #Establecemos la region de scroll
        canvas.config(scrollregion=canvas.bbox("all"))

        metricas_recalculo = self.conf.metricas_recalculo
        texto_metricas_recalculo = ctk.CTkLabel(self, text="Confidencialidad: "+metricas_recalculo[0]+"\nIntegridad: "+metricas_recalculo[1]+"\nDisponibilidad: "+metricas_recalculo[2], font=("Arial", 20))
        texto_metricas_recalculo.grid(row=3, column=0, padx= 60, pady=15, sticky='n')

        try:
            ruta_vdb = utiles.get_nombre_y_extension_fichero(self.conf.ruta_vdb) #Si no has metido un VDB te va a dar una excepcion
            componente = self.conf.componente
            texto = "VDB: "+ruta_vdb+"\nComponente introducido: "+componente+"\nNessus Report: "+utiles.get_nombre_y_extension_fichero(self.conf.ruta_nessus)
        except Exception:
            ruta_vdb = "No introducido"
            texto = "VDB: "+ruta_vdb+"\nNessus Report: "+utiles.get_nombre_y_extension_fichero(self.conf.ruta_nessus)

        

        texto_rutas = ctk.CTkLabel(self, text=texto, font=("Arial", 20))
        texto_rutas.grid(row=4, column=0, padx= 60, pady=15, sticky='n')

        boton_atras=ctk.CTkButton(self, text="Atras", font=("Arial", 24), border_spacing=5, command=self.mostrar_anterior)
        boton_atras.grid(row=5, column=0, padx= 60, pady=(45, 30), sticky='w')

        boton_siguiente=ctk.CTkButton(self, text="Comenzar", font=("Arial", 24), border_spacing=5, command=self.boton_siguiente_command)
        boton_siguiente.grid(row=5, column=0, padx= 60, pady=(45, 30), sticky='e')
    
    def get_datos_tabla(self):
        """Devuelve una lista con tres listas. La primera indices de la A a la Z como maximo, la segunda con la cabecera vdb y la tercera con los valores de cada uno. Las tres listas tienen el mismo tamaño"""
        columnas_nessus = self.conf.configuracion["vdb_generado"]["nessus"].items()
        columnas_criticidades = self.conf.configuracion["vdb_generado"]["columnas_criticidades"].items()
        columnas_fijas = self.conf.columnas_fijas.items()

        cabecera_vdb = utiles.get_cabecera_xlsx_combinada(utiles.conf.vdb_hoja)

        lista_valores = [None] * len(cabecera_vdb)

        for clave, valor in columnas_fijas:
            try:
                indice = utiles.get_indice_a_partir_columna(clave)
                lista_valores[indice] = valor
            except TypeError: #Se produce cuando le pasas al metodo utiles.get_indice_a_partir_columna() algo que no sea un caracter. En este caso es cuando llega a algun n/a de la configuracion. Esos no hay que meterlos.
                pass
        
        for clave, valor in columnas_nessus:
            try:
                lista_valores[utiles.get_indice_a_partir_columna(valor)] = clave
            except TypeError:
                pass
        
        for clave, valor in columnas_criticidades:
            try:
                indice = utiles.get_indice_a_partir_columna(valor)
                lista_valores[indice] = clave
            except TypeError:
                pass
        
        lista_indices = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
        lista_indices = lista_indices[:len(lista_valores)]

        return [lista_indices, cabecera_vdb, lista_valores]
    
    def boton_siguiente_command(self):
        msg_box = tk.messagebox.askquestion('VDB', '¿Seguro que desea comenzar la generación del VDB?', icon='warning')
        if msg_box == 'yes':
            utiles_interfaz.mostrar_info("Selecciona la carpeta donde desea guardar el VDB generado y el nombre de este")
            directorio_vdb_generado = fd.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
            if (directorio_vdb_generado != ""):
                self.conf.ruta_vdb_generado = utiles.formatear_ruta(directorio_vdb_generado)
                self.parent.mostrar_contenedor("generar_vdb")
    
    def mostrar_anterior(self):
        self.parent.mostrar_contenedor("columnas_fijas")