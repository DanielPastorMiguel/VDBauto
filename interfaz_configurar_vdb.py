import customtkinter as ctk
import configuracion
import utiles_interfaz

class InterfazConfigurarVdb(ctk.CTkFrame):
    
    conf = configuracion.Configuracion()

    def __init__(self, parent):
        ctk.CTkFrame.__init__(self, parent)
        self.parent = parent

        texto_superior1=ctk.CTkLabel(self, text="Inserte los índices donde deben ir \nlas siguiente columnas en el VDB generado:", font=("Arial", 24))
        texto_superior1.grid(row=0, column=0, columnspan=2, padx=30, pady=35)

        texto_columna_vulnerabilidad=ctk.CTkLabel(self, text="Identificador vulnerabilidad", font=("Arial", 22))
        texto_columna_vulnerabilidad.grid(row=1, column=0, padx=(50, 15), pady=15, sticky = ctk.E)
        self.combobox_columna_vulnerabilidad = ctk.CTkComboBox(master=self,
                                     values=None,
                                     state="readonly",
                                     justify="center")
        self.combobox_columna_vulnerabilidad.grid(row=1, column=1, sticky = "WE", padx=(15, 30), pady=15)

        texto_componente_afectado=ctk.CTkLabel(self, text="Componente afectado", font=("Arial", 22))
        texto_componente_afectado.grid(row=2, column=0, padx=(50, 15), pady=15, sticky = ctk.E)
        self.combobox_componente_afectado = ctk.CTkComboBox(master=self,
                                     values=None,
                                     state="readonly",
                                     justify="center")
        self.combobox_componente_afectado.grid(row=2, column=1, sticky = "WE", padx=(15, 30), pady=15)

        texto_estado_vulnerabilidad=ctk.CTkLabel(self, text="Estado vulnerabilidad", font=("Arial", 22))
        texto_estado_vulnerabilidad.grid(row=3, column=0, padx=(50, 15), pady=15, sticky = ctk.E)
        self.combobox_estado_vulnerabilidad = ctk.CTkComboBox(master=self,
                                     values=None,
                                     state="readonly",
                                     justify="center")
        self.combobox_estado_vulnerabilidad.grid(row=3, column=1, sticky = "WE", padx=(15, 30), pady=15)

        boton_atras=ctk.CTkButton(self, text="Atras", font=("Arial", 24), border_spacing=5, command=self.mostrar_anterior)
        boton_atras.grid(row=4, column=0, padx=35, pady=(40, 30))

        boton_guardar=ctk.CTkButton(self, text="Guardar", font=("Arial", 24), border_spacing=5, command=self.boton_guardar)
        boton_guardar.grid(row=4, column=1, sticky = "WE", padx=(0, 40), pady=(40, 30))
    
    def iniciar_desplegables(self):
        cabecera_vdb = [i for i in self.conf.conf_cabecera_vdb if i != ""] #Quitamos los "" que pueden salir al combinar celdas
        self.combobox_columna_vulnerabilidad.configure(values=cabecera_vdb)
        self.combobox_componente_afectado.configure(values=cabecera_vdb)
        self.combobox_estado_vulnerabilidad.configure(values=cabecera_vdb)

    def boton_guardar(self):
        if (self.combobox_columna_vulnerabilidad.get() == "" or self.combobox_componente_afectado.get() == "" or self.combobox_estado_vulnerabilidad.get() == ""):
            utiles_interfaz.mostrar_error("Debe rellenar todos los desplegables obligatorios")
        else:
            hoja = self.conf.conf_hoja_vdb
            columna_vulnerabilidad = self.combobox_columna_vulnerabilidad.get()
            componente_afectado = self.combobox_componente_afectado.get()
            estado_vulnerabilidad = self.combobox_estado_vulnerabilidad.get()
            self.conf.cambiar_configuracion_vdb(hoja, columna_vulnerabilidad, componente_afectado, estado_vulnerabilidad)
            self.conf.guardar_configuracion()
            utiles_interfaz.mostrar_info("La configuración se ha guardado correctamente")
            self.mostrar_anterior()
    
    def mostrar_anterior(self):
        self.combobox_columna_vulnerabilidad.set("")
        self.combobox_componente_afectado.set("")
        self.combobox_estado_vulnerabilidad.set("")
        self.parent.mostrar_contenedor("configuracion")