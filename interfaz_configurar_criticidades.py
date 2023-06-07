import customtkinter as ctk
import configuracion
import utiles
import utiles_interfaz

class InterfazConfigurarCriticidades(ctk.CTkFrame):
    
    conf = configuracion.Configuracion()

    diccionario_criticidades = {}

    diccionario_cabecera_vdb_restante = {} #contiene como claves el valor de la cabecera y valores el indice que corresponden en el vdb

    def __init__(self, parent):
        ctk.CTkFrame.__init__(self, parent)
        self.parent = parent

        texto_superior1=ctk.CTkLabel(self, text="Inserta los índices donde deben ir \nlas siguiente columnas en el VDB generado:", font=("Arial", 24))
        texto_superior1.grid(row=0, column=0, columnspan=2, padx=30, pady=(35, 0))

        texto_superior2=ctk.CTkLabel(self, text="Nota: solo se muestran las columnas del VDB que no estan \nya escogidas en la configuración de Nessus Report", font=ctk.CTkFont(family="arial", size=14, slant="italic"))
        texto_superior2.grid(row=1, column=0, columnspan=2, padx=30, pady=20)

        texto_cvss_2=ctk.CTkLabel(self, text="CVSS v2.0 Base Score", font=("Arial", 22))
        texto_cvss_2.grid(row=2, column=0, padx=(50, 15), pady=15, sticky = ctk.E)
        self.combobox_cvss_2 = ctk.CTkComboBox(master=self,
                                     values=None,
                                     state="readonly",
                                     justify="center")
        self.combobox_cvss_2.grid(row=2, column=1, padx=(15, 30), sticky = "WE", pady=15)

        texto_cvss_3_0=ctk.CTkLabel(self, text="CVSS v3.0 Base Score", font=("Arial", 22))
        texto_cvss_3_0.grid(row=3, column=0, padx=(50, 15), pady=15, sticky = ctk.E)
        self.combobox_cvss_3_0 = ctk.CTkComboBox(master=self,
                                     values=None,
                                     state="readonly",
                                     justify="center")
        self.combobox_cvss_3_0.grid(row=3, column=1, padx=(15, 30), sticky = "WE", pady=15)

        texto_cvss_3_1=ctk.CTkLabel(self, text="CVSS v3.1 Base Score", font=("Arial", 22))
        texto_cvss_3_1.grid(row=4, column=0, padx=(50, 15), pady=15, sticky = ctk.E)
        self.combobox_cvss_3_1 = ctk.CTkComboBox(master=self,
                                     values=None,
                                     state="readonly",
                                     justify="center")
        self.combobox_cvss_3_1.grid(row=4, column=1, padx=(15, 30), sticky = "WE", pady=15)

        texto_cvss_3_0_recalculo=ctk.CTkLabel(self, text="CVSS v3.0 recálculo", font=("Arial", 22))
        texto_cvss_3_0_recalculo.grid(row=5, column=0, padx=(50, 15), pady=15, sticky = ctk.E)
        self.combobox_cvss_3_0_recalculo = ctk.CTkComboBox(master=self,
                                     values=None,
                                     state="readonly",
                                     justify="center")
        self.combobox_cvss_3_0_recalculo.grid(row=5, column=1, padx=(15, 30), sticky = "WE", pady=15)

        texto_cvss_3_1_recalculo=ctk.CTkLabel(self, text="CVSS v3.1 recálculo", font=("Arial", 22))
        texto_cvss_3_1_recalculo.grid(row=6, column=0, padx=(50, 15), pady=15, sticky = ctk.E)
        self.combobox_cvss_3_1_recalculo = ctk.CTkComboBox(master=self,
                                     values=None,
                                     state="readonly",
                                     justify="center")
        self.combobox_cvss_3_1_recalculo.grid(row=6, column=1, padx=(15, 30), sticky = "WE", pady=15)

        texto_plugin_publication_date=ctk.CTkLabel(self, text="Plugin publication date", font=("Arial", 22))
        texto_plugin_publication_date.grid(row=7, column=0, padx=(50, 15), pady=15, sticky = ctk.E)
        self.combobox_plugin_publication_date = ctk.CTkComboBox(master=self,
                                     values=None,
                                     state="readonly",
                                     justify="center")
        self.combobox_plugin_publication_date.grid(row=7, column=1, padx=(15, 30), sticky = "WE", pady=15)

        boton_atras=ctk.CTkButton(self, text="Atras", font=("Arial", 24), border_spacing=5, command=self.mostrar_anterior)
        boton_atras.grid(row=8, column=0, padx=35, pady=(40, 30))

        boton_guardar=ctk.CTkButton(self, text="Guardar", font=("Arial", 24), border_spacing=5, command=self.boton_guardar)
        boton_guardar.grid(row=8, column=1, sticky = "WE", padx=(0, 40), pady=(40, 30))
    
    def iniciar_desplegables(self):
        lista_columnas_nessus = list(self.conf.configuracion["vdb_generado"]["nessus"].values())

        lista_indices_cabecera_vdb_restante = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
        
        cabecera_vdb = utiles.get_cabecera_xlsx_combinada(self.conf.vdb_hoja)
        lista_indices_cabecera_vdb_restante = lista_indices_cabecera_vdb_restante[0:len(cabecera_vdb)]

        i=0
        for indice in lista_columnas_nessus:
            try:
                if i!=3 and i!=4 and i!=5: #para que no quite la de cvss2.0 y 3.0 basescorae, esas se deben poder elegir
                    lista_indices_cabecera_vdb_restante.remove(indice)
                i+=1
            except ValueError:
                i+=1
                pass

        for indice in lista_indices_cabecera_vdb_restante:
            self.diccionario_cabecera_vdb_restante[cabecera_vdb[utiles.get_indice_a_partir_columna(indice)]] = indice
        
        self.combobox_cvss_2.configure(values=self.diccionario_cabecera_vdb_restante.keys())
        self.combobox_cvss_3_0.configure(values=self.diccionario_cabecera_vdb_restante.keys())
        self.combobox_cvss_3_1.configure(values=self.diccionario_cabecera_vdb_restante.keys())
        self.combobox_cvss_3_0_recalculo.configure(values=self.diccionario_cabecera_vdb_restante.keys())
        self.combobox_cvss_3_1_recalculo.configure(values=self.diccionario_cabecera_vdb_restante.keys())
        self.combobox_plugin_publication_date.configure(values=self.diccionario_cabecera_vdb_restante.keys())
    
    def boton_guardar(self):
        if (self.combobox_cvss_2.get() == "" or self.combobox_cvss_3_0.get() == "" or self.combobox_cvss_3_1.get() == "" or self.combobox_plugin_publication_date.get() == "" or self.combobox_cvss_3_0_recalculo.get() == "" or self.combobox_cvss_3_1_recalculo.get() == ""):
            utiles_interfaz.mostrar_error("Debe rellenar todos los desplegables obligatorios")
        else:
            self.diccionario_criticidades["cvssV2_basescore"] = self.combobox_cvss_2.get().lower()
            self.diccionario_criticidades["cvssV3_0_basescore"] = self.combobox_cvss_3_0.get().lower()
            self.diccionario_criticidades["cvssV3_1_basescore"] = self.combobox_cvss_3_1.get().lower()
            self.diccionario_criticidades["cvssV3_0_basescore_recalculo"] = self.combobox_cvss_3_0_recalculo.get().lower()
            self.diccionario_criticidades["cvssV3_1_basescore_recalculo"] = self.combobox_cvss_3_1_recalculo.get().lower()
            self.diccionario_criticidades["fecha_publicacion"] = self.combobox_plugin_publication_date.get().lower()
            
            i=0
            for key in list(self.conf.configuracion["vdb_generado"]["nessus"].keys()): #cvss2.0, cvss3.0 y fecha de publicacion tienen que tener el mismo valor para la configuracion de nessus como para la de criticidades
                if (i==3):
                    self.conf.configuracion["vdb_generado"]["nessus"][key] = self.combobox_cvss_2.get().lower()
                elif (i==4):
                    self.conf.configuracion["vdb_generado"]["nessus"][key] = self.combobox_cvss_3_0.get().lower()
                elif (i==5):
                    self.conf.configuracion["vdb_generado"]["nessus"][key] = self.combobox_plugin_publication_date.get().lower()
                i+=1
            
            self.conf.cambiar_configuracion_nessus(self.conf.configuracion["vdb_generado"]["nessus"])
            self.conf.cambiar_configuracion_vdb_generado(self.diccionario_criticidades)
            self.conf.guardar_configuracion()
            utiles_interfaz.mostrar_info("La configuración se ha guardado correctamente")
    
    def mostrar_anterior(self):
        self.combobox_cvss_2.set("")
        self.combobox_cvss_3_0.set("")
        self.combobox_cvss_3_1.set("")
        self.combobox_cvss_3_0_recalculo.set("")
        self.combobox_cvss_3_1_recalculo.set("")
        self.combobox_plugin_publication_date.set("")
        self.diccionario_criticidades = {}
        self.diccionario_nessus = {}
        self.parent.mostrar_contenedor("configuracion")