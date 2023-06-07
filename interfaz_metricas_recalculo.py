import customtkinter as ctk
import configuracion

class InterfazMetricasRecalculo(ctk.CTkFrame):

    combobox_integridad = None
    combobox_disponibilidad = None
    combobox_confidencialidad = None

    conf = configuracion.Configuracion()

    def __init__(self, parent):
        ctk.CTkFrame.__init__(self, parent)
        self.parent = parent

        texto_superior=ctk.CTkLabel(self, text="Valores de \n'env score metrics'\npara realizar los recálculos:", font=("Arial", 24))
        texto_superior.grid(row=0, column=0, columnspan=2, padx=30, pady=30)

        texto_confidencialidad=ctk.CTkLabel(self, text="Confidencialidad", font=("Arial", 22))
        texto_confidencialidad.grid(row=1, column=0, padx=(50, 15), pady=15, sticky = ctk.E)

        self.combobox_confidencialidad = ctk.StringVar(value="LOW")
        combobox1 = ctk.CTkComboBox(master=self,
                                     values=["LOW", "MEDIUM", "HIGH"],
                                     variable=self.combobox_confidencialidad,
                                     state="readonly",
                                     justify="center")
        combobox1.grid(row=1, column=1, padx=(5, 50), pady=15)

        texto_integridad=ctk.CTkLabel(self, text="Integridad", font=("Arial", 22))
        texto_integridad.grid(row=2, column=0, padx=15, pady=15, sticky = ctk.E)

        self.combobox_integridad = ctk.StringVar(value="LOW")
        combobox2 = ctk.CTkComboBox(master=self,
                                     values=["LOW", "MEDIUM", "HIGH"],
                                     variable=self.combobox_integridad,
                                     state="readonly",
                                     justify="center")
        combobox2.grid(row=2, column=1, padx=(5, 50), pady=15)

        texto_disponibilidad=ctk.CTkLabel(self, text="Disponibilidad", font=("Arial", 22))
        texto_disponibilidad.grid(row=3, column=0, padx=15, pady=15, sticky = ctk.E)

        self.combobox_disponibilidad = ctk.StringVar(value="LOW")
        combobox3 = ctk.CTkComboBox(master=self,
                                     values=["LOW", "MEDIUM", "HIGH"],
                                     variable=self.combobox_disponibilidad,
                                     state="readonly",
                                     justify="center")
        combobox3.grid(row=3, column=1, padx=(5, 50), pady=15)

        boton_siguiente=ctk.CTkButton(self, text="Siguiente", font=("Arial", 24), border_spacing=5, command=self.boton_siguiente_command)
        boton_siguiente.grid(row=4, column=0, columnspan=2, padx=50, pady=(35, 30))

    def boton_siguiente_command(self):
        self.conf.metricas_recalculo = [self.combobox_confidencialidad.get()[0], self.combobox_integridad.get()[0], self.combobox_disponibilidad.get()[0]] #El [0] es porque para montar el vector hay que usar L, M o H, si pones LOW, MEDIUM o HIGH da error
        self.parent.mostrar_contenedor("columnas_fijas")