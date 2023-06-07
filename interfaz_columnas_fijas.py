import customtkinter as ctk
import tkinter as tk
import utiles_interfaz
import configuracion
import utiles

class InterfazColumnasFijas(ctk.CTkFrame):
    
    combobox_columna = None
    input_columna = None
    
    diccionario_cabecera_vdb_restante = {} #contiene como claves el valor de la cabecera y valores el indice que corresponden en el vdb

    conf = configuracion.Configuracion()

    def __init__(self, parent):
        ctk.CTkFrame.__init__(self, parent)
        self.parent = parent

        texto_superior=ctk.CTkLabel(self, text="Inserta columnas fijas:", font=("Arial", 24))
        texto_superior.grid(row=0, column=0, columnspan=2, padx=30, pady=30)

        texto_superior=ctk.CTkLabel(self, text="Nota: en el checkbox solo se muestran las columnas\n que no han sido utilizadas en la configuración", font=ctk.CTkFont(family="arial", size=14, slant="italic"))
        texto_superior.grid(row=1, column=0, columnspan=2, padx=30, pady=(0, 10))

        texto_columna=ctk.CTkLabel(self, text="Columna", font=("Arial", 22))
        texto_columna.grid(row=2, column=0, padx=(15, 30), pady=15, sticky = ctk.E)

        self.combobox_columna = ctk.CTkComboBox(master=self,
                                     values=None,
                                     state="readonly",
                                     justify="center")
        self.combobox_columna.grid(row=2, column=1, sticky = "WE", padx=(0, 30), pady=30)

        texto_valor=ctk.CTkLabel(self, text="Valor", font=("Arial", 22))
        texto_valor.grid(row=3, column=0, padx=(15, 30), pady=30, sticky = ctk.E)

        self.input_columna = ctk.CTkEntry(master=self, font=("Arial", 16))
        self.input_columna.grid(row=3, column=1, padx=(0, 30), pady=15, sticky = ctk.W, ipadx=40)

        boton_anadir_columna=ctk.CTkButton(self, text="Añadir columna", font=("Arial", 24), border_spacing=15, command=self.anadir_columna)
        boton_anadir_columna.grid(row=4, column=0, columnspan=2, pady=(20, 0))

        boton_atras=ctk.CTkButton(self, text="Atras", font=("Arial", 24), border_spacing=5, command=self.mostrar_anterior)
        boton_atras.grid(row=5, column=0, padx=(60, 0), pady=(45, 30), sticky = ctk.W)

        boton_siguiente=ctk.CTkButton(self, text="Siguiente", font=("Arial", 24), border_spacing=5, command=self.boton_siguiente_command)
        boton_siguiente.grid(row=5, column=1, padx=(0, 60), pady=(45, 30), sticky = ctk.E)


    def anadir_columna(self):
        if (self.combobox_columna.get() == ""):
            utiles_interfaz.mostrar_error("Debe seleccionar la columna donde se va a insertar")
        elif (self.input_columna.get() == ""):
            msg_box = tk.messagebox.askquestion('VDB', '¿Seguro que quiere insertar una columna vacia?', icon='warning')
            if msg_box == 'yes':
                self.conf.columnas_fijas[self.diccionario_cabecera_vdb_restante[self.combobox_columna.get()]] = self.input_columna.get()
                self.combobox_columna.set(value="")
        else:
            self.conf.columnas_fijas[self.diccionario_cabecera_vdb_restante[self.combobox_columna.get()]] = self.input_columna.get()
            utiles_interfaz.mostrar_info("Columna añadida correctamente")
            self.combobox_columna.set(value="")
            self.input_columna.delete(0, ctk.END) #vacia el campo
    
    def iniciar_desplegable(self):
        lista_columnas_nessus = list(self.conf.configuracion["vdb_generado"]["nessus"].values())
        lista_columnas_criticidades = list(self.conf.configuracion["vdb_generado"]["columnas_criticidades"].values())
        lista_columnas_nessus = [i for i in lista_columnas_nessus if i != "n/a"]
        lista_columnas_criticidades = [i for i in lista_columnas_criticidades if i != "n/a"]

        lista_indices_cabecera_vdb_restante = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
        
        cabecera_vdb = utiles.get_cabecera_xlsx_combinada(self.conf.vdb_hoja)
        lista_indices_cabecera_vdb_restante = lista_indices_cabecera_vdb_restante[0:len(cabecera_vdb)]

        for indice in lista_columnas_nessus:
            try:
                lista_indices_cabecera_vdb_restante.remove(indice)
            except ValueError:
                pass
        
        for indice in lista_columnas_criticidades:
            try:
                lista_indices_cabecera_vdb_restante.remove(indice)
            except ValueError:
                pass
        
        for indice in lista_indices_cabecera_vdb_restante:
            self.diccionario_cabecera_vdb_restante[cabecera_vdb[utiles.get_indice_a_partir_columna(indice)]] = indice
        
        self.combobox_columna.configure(values=self.diccionario_cabecera_vdb_restante.keys())
    
    def boton_siguiente_command(self):
        self.combobox_columna.set("")
        self.parent.mostrar_contenedor("previsualizar")
    
    def mostrar_anterior(self):
        self.combobox_columna.set("")
        self.parent.mostrar_contenedor("metricas_recalculo")