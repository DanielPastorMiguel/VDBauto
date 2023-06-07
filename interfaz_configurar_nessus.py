import customtkinter as ctk
import configuracion
import utiles
import utiles_interfaz

class InterfazConfigurarNessus(ctk.CTkFrame):
    
    conf = configuracion.Configuracion()

    combobox_plugin_id = None
    diccionario_columnas_nessus = {}
    diccionario_columnas_extra = {}
    
    diccionario_cabecera_vdb_restante = {} #contiene como claves el valor de la cabecera y valores el indice que corresponden en el vdb

    def __init__(self, parent):
        ctk.CTkFrame.__init__(self, parent)
        self.parent = parent

        texto_superior1=ctk.CTkLabel(self, text="Columna obligatoria:", font=("Arial", 24))
        texto_superior1.grid(row=0, column=0, padx=30, pady=30)
        texto_superior2=ctk.CTkLabel(self, text="Columna Nessus Report:", font=("Arial", 24))
        texto_superior2.grid(row=0, column=1, padx=30, pady=30)
        texto_superior3=ctk.CTkLabel(self, text="Columna VDB generado:", font=("Arial", 24))
        texto_superior3.grid(row=0, column=2, padx=30, pady=30)
        
        texto_plugin_id=ctk.CTkLabel(self, text="Plugin ID", font=("Arial", 22))
        texto_plugin_id.grid(row=1, column=0, padx=(50, 15), pady=15, sticky = ctk.E)
        self.combobox_plugin_id = ctk.CTkComboBox(master=self,
                                     values=None,
                                     state="readonly",
                                     justify="center")
        self.combobox_plugin_id.grid(row=1, column=1, sticky = "WE", padx=(15, 30), pady=15)
        texto_plugin_id_nota = ctk.CTkLabel(self, text="Se usa la misma columna\nque para el CVE", font=ctk.CTkFont(family="arial", size=14, slant="italic"))
        texto_plugin_id_nota.grid(row=1, column=2, padx=(15, 30), sticky = "WE", pady=15)

        texto_cve=ctk.CTkLabel(self, text="CVE", font=("Arial", 22))
        texto_cve.grid(row=2, column=0, padx=(50, 15), pady=15, sticky = ctk.E)
        self.combobox_cve = ctk.CTkComboBox(master=self,
                                     values=None,
                                     state="readonly",
                                     justify="center")
        self.combobox_cve.grid(row=2, column=1, padx=(15, 30), sticky = "WE", pady=15)
        self.combobox_cve_vdb = ctk.CTkComboBox(master=self,
                                     values=None,
                                     state="readonly",
                                     justify="center")
        self.combobox_cve_vdb.grid(row=2, column=2, padx=(15, 30), sticky = "WE", pady=15)

        texto_severidad=ctk.CTkLabel(self, text="Severidad", font=("Arial", 22))
        texto_severidad.grid(row=3, column=0, padx=(50, 15), pady=15, sticky = ctk.E)
        self.combobox_severidad = ctk.CTkComboBox(master=self,
                                     values=None,
                                     state="readonly",
                                     justify="center")
        self.combobox_severidad.grid(row=3, column=1, padx=(15, 30), sticky = "WE", pady=15)
        self.combobox_severidad_vdb = ctk.CTkComboBox(master=self,
                                     values=None,
                                     state="readonly",
                                     justify="center")
        self.combobox_severidad_vdb.grid(row=3, column=2, padx=(15, 30), sticky = "WE", pady=15)

        texto_cvss_2=ctk.CTkLabel(self, text="CVSS v2.0 Base Score", font=("Arial", 22))
        texto_cvss_2.grid(row=4, column=0, padx=(50, 15), pady=15, sticky = ctk.E)
        self.combobox_cvss_2 = ctk.CTkComboBox(master=self,
                                     values=None,
                                     state="readonly",
                                     justify="center")
        self.combobox_cvss_2.grid(row=4, column=1, padx=(15, 30), sticky = "WE", pady=15)
        texto_cvss_2_nota = ctk.CTkLabel(self, text="El índice de esta columna en el \nVDB generado se modifica en \nla configuración de criticidades", font=ctk.CTkFont(family="arial", size=14, slant="italic"))
        texto_cvss_2_nota.grid(row=4, column=2, padx=(15, 30), pady=15)

        texto_cvss_3=ctk.CTkLabel(self, text="CVSS v3.0 Base Score", font=("Arial", 22))
        texto_cvss_3.grid(row=5, column=0, padx=(50, 15), pady=15, sticky = ctk.E)
        self.combobox_cvss_3 = ctk.CTkComboBox(master=self,
                                     values=None,
                                     state="readonly",
                                     justify="center")
        self.combobox_cvss_3.grid(row=5, column=1, padx=(15, 30), sticky = "WE", pady=15)
        texto_cvss_3_nota = ctk.CTkLabel(self, text="El índice de esta columna en el \nVDB generado se modifica en \nla configuración de criticidades", font=ctk.CTkFont(family="arial", size=14, slant="italic"))
        texto_cvss_3_nota.grid(row=5, column=2, padx=(15, 30), pady=15)

        texto_plugin_publication_date=ctk.CTkLabel(self, text="Plugin publication date", font=("Arial", 22))
        texto_plugin_publication_date.grid(row=6, column=0, padx=(50, 15), pady=15, sticky = ctk.E)
        self.combobox_plugin_publication_date = ctk.CTkComboBox(master=self,
                                     values=None,
                                     state="readonly",
                                     justify="center")
        self.combobox_plugin_publication_date.grid(row=6, column=1, padx=(15, 30), sticky = "WE", pady=15)
        texto_plugin_publication_date_nota = ctk.CTkLabel(self, text="El índice de esta columna en el \nVDB generado se modifica en \nla configuración de criticidades", font=ctk.CTkFont(family="arial", size=14, slant="italic"))
        texto_plugin_publication_date_nota.grid(row=6, column=2, padx=(15, 30), pady=15)

        texto_columnas_extra=ctk.CTkLabel(self, text="Añade columnas extra:", font=("Arial", 24))
        texto_columnas_extra.grid(row=7, column=0, columnspan=3, padx=30, pady=(30,15))
        texto_nota=ctk.CTkLabel(self, text="Nota: en el campo izquierdo selecciona la columna y en el derecho la posición en el VDB generado", font=ctk.CTkFont(family="arial", size=14, slant="italic"))
        texto_nota.grid(row=8, column=0, columnspan=3, padx=30, pady=(0, 0))

        self.combobox_columnas_extra = ctk.CTkComboBox(master=self,
                                     values=None,
                                     state="readonly",
                                     justify="center")
        self.combobox_columnas_extra.grid(row=9, column=0, columnspan=2, padx=(250, 50), sticky = "WE", pady=15)
        self.combobox_columna_extra_2 = ctk.CTkComboBox(master=self,
                                     values=None,
                                     state="readonly",
                                     justify="center")
        self.combobox_columna_extra_2.grid(row=9, column=2, padx=(40, 40), sticky = "WE", pady=30)

        boton_anadir=ctk.CTkButton(self, text="Añadir", font=("Arial", 24), fg_color="#272b28", hover_color="#333834", border_spacing=5, command=self.boton_anadir)
        boton_anadir.grid(row=10, column=1, columnspan=2, sticky = "WE", padx=150, pady=(0, 15))

        boton_atras=ctk.CTkButton(self, text="Atras", font=("Arial", 24), border_spacing=5, command=self.mostrar_anterior)
        boton_atras.grid(row=11, column=0, sticky = "WE", padx=50, pady=(35, 30))

        boton_guardar=ctk.CTkButton(self, text="Guardar", font=("Arial", 24), border_spacing=5, command=self.boton_guardar)
        boton_guardar.grid(row=11, column=1, columnspan=2, padx=(50, 100), sticky = "WE", pady=(35, 30))

    def boton_anadir(self):
        valor_columna_nessus = self.combobox_columnas_extra.get()
        columna_vdb = self.combobox_columna_extra_2.get()
        if (valor_columna_nessus == "" or columna_vdb== ""):
            utiles_interfaz.mostrar_error("Debe seleccionar un valor de los desplegables de añadir columnas extra")
        else:
            self.diccionario_columnas_extra[valor_columna_nessus] = self.diccionario_cabecera_vdb_restante[columna_vdb]
            utiles_interfaz.mostrar_info("Columna extra añadida.\nRecuerda guardar la configuración para que se aplique")
            self.combobox_columnas_extra.set(value="")
            self.combobox_columna_extra_2.set(value="")
    
    def boton_guardar(self):
        if (self.combobox_cve.get() == "" or self.combobox_severidad.get() == "" or self.combobox_cvss_2.get() == "" or self.combobox_cvss_3.get() == "" or self.combobox_plugin_publication_date.get() == "" or
            self.combobox_plugin_id.get() == "" or self.combobox_cve_vdb.get() == "" or self.combobox_severidad_vdb.get() == ""):
            utiles_interfaz.mostrar_error("Debe rellenar todos los desplegables obligatorios")
        else:
            self.diccionario_columnas_nessus[self.combobox_plugin_id.get()] = "n/a"
            self.diccionario_columnas_nessus[self.combobox_cve.get()] = self.diccionario_cabecera_vdb_restante[self.combobox_cve_vdb.get()]
            if self.combobox_severidad_vdb.get() == "n/a":  self.diccionario_columnas_nessus[self.combobox_severidad.get()] = "n/a"
            else: self.diccionario_columnas_nessus[self.combobox_severidad.get()] = self.diccionario_cabecera_vdb_restante[self.combobox_severidad_vdb.get()]
            self.diccionario_columnas_nessus[self.combobox_cvss_2.get()] = list(self.conf.configuracion["vdb_generado"]["columnas_criticidades"].values())[0].lower()
            self.diccionario_columnas_nessus[self.combobox_cvss_3.get()] = list(self.conf.configuracion["vdb_generado"]["columnas_criticidades"].values())[1].lower()
            self.diccionario_columnas_nessus[self.combobox_plugin_publication_date.get()] = list(self.conf.configuracion["vdb_generado"]["columnas_criticidades"].values())[5].lower()
            self.diccionario_columnas_nessus.update(self.diccionario_columnas_extra)
            self.conf.cambiar_configuracion_nessus(self.diccionario_columnas_nessus)
            self.conf.guardar_configuracion()
            utiles_interfaz.mostrar_info("La configuración se ha guardado correctamente")
    
    def iniciar_desplegables(self):
        self.combobox_plugin_id.configure(values=self.conf.conf_cabecera_nessus_report)
        self.combobox_cve.configure(values=self.conf.conf_cabecera_nessus_report)
        self.combobox_severidad.configure(values=self.conf.conf_cabecera_nessus_report)
        self.combobox_cvss_2.configure(values=self.conf.conf_cabecera_nessus_report)
        self.combobox_cvss_3.configure(values=self.conf.conf_cabecera_nessus_report)
        self.combobox_plugin_publication_date.configure(values=self.conf.conf_cabecera_nessus_report)
        self.combobox_columnas_extra.configure(values=self.conf.conf_cabecera_nessus_report)

        cabecera_vdb = utiles.get_cabecera_xlsx_combinada(self.conf.vdb_hoja)
        lista_indices_cabecera_vdb_restante = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
        lista_indices_cabecera_vdb_restante = lista_indices_cabecera_vdb_restante[0:len(cabecera_vdb)]
        for indice in lista_indices_cabecera_vdb_restante:
            self.diccionario_cabecera_vdb_restante[cabecera_vdb[utiles.get_indice_a_partir_columna(indice)]] = indice
        
        self.combobox_cve_vdb.configure(values=self.diccionario_cabecera_vdb_restante.keys())
        lista_severidad = list(self.diccionario_cabecera_vdb_restante.keys())
        lista_severidad.insert(0, "n/a")
        self.combobox_severidad_vdb.configure(values=lista_severidad)
        self.combobox_columna_extra_2.configure(values=self.diccionario_cabecera_vdb_restante.keys())
    
    def mostrar_anterior(self):
        self.combobox_cve.set("")
        self.combobox_severidad.set("")
        self.combobox_cvss_2.set("")
        self.combobox_cvss_3.set("")
        self.combobox_plugin_publication_date.set("")
        self.combobox_columnas_extra.set("")
        self.combobox_plugin_id.set("")
        self.combobox_cve_vdb.set("")
        self.combobox_severidad_vdb.set("")
        self.diccionario_columnas_extra = {}
        self.diccionario_columnas_nessus = {}
        self.parent.mostrar_contenedor("configuracion")