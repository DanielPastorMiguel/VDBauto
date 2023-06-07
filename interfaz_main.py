import customtkinter as ctk
import interfaz_inicio
import interfaz_configuracion
import interfaz_metricas_recalculo
import interfaz_columnas_fijas
import interfaz_previsualizar
import interfaz_generacion_vdb
import interfaz_configurar_nessus
import interfaz_configurar_criticidades
import interfaz_configurar_vdb

class AplicacionPrincipal(ctk.CTkFrame):
    def __init__(self, parent, *args, **kwargs):

        # Modos soportados : Light, Dark, System
        ctk.set_appearance_mode("Dark")
        
        # Temas soportados : green, dark-blue, blue
        ctk.set_default_color_theme("green")

        ctk.CTkFrame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        
        self.contenedor1 = interfaz_inicio.Inicio(self)
        self.contenedor2 = interfaz_configuracion.InterfazConfiguracion(self)
        self.contenedor3 = interfaz_metricas_recalculo.InterfazMetricasRecalculo(self)
        self.contenedor4 = interfaz_columnas_fijas.InterfazColumnasFijas(self)
        self.contenedor5 = interfaz_previsualizar.InterfazPrevisualizar(self)
        self.contenedor6 = interfaz_generacion_vdb.InterfazGeneracionVdb(self)
        self.contenedor7 = interfaz_configurar_nessus.InterfazConfigurarNessus(self)
        self.contenedor8 = interfaz_configurar_criticidades.InterfazConfigurarCriticidades(self)
        self.contenedor9 = interfaz_configurar_vdb.InterfazConfigurarVdb(self)
        
        # Define el tamaño y la posición de cada contenedor
        self.contenedor1.pack()
        self.contenedor2.pack_forget()
        self.contenedor3.pack_forget()
        self.contenedor4.pack_forget()
        self.contenedor5.pack_forget()
        self.contenedor6.pack_forget()
        self.contenedor7.pack_forget()
        self.contenedor8.pack_forget()
        self.contenedor9.pack_forget()
        
        # Configura la ventana
        self.parent.title("VDBauto")
        self.parent.resizable(False, False)
        self.parent.iconbitmap('logo.ico')

        #Centramos la ventana en funcion al Contenedor1 que es el primero que va a aparecer
        windowWidth = self.contenedor1.winfo_reqwidth()
        windowHeight = self.contenedor1.winfo_reqheight()
        positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
        positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)
        root.geometry("+{}+{}".format(positionRight, positionDown))

    def mostrar_contenedor(self, contenedor):
        if contenedor == "inicio":
            self.contenedor1.pack()
            self.contenedor2.pack_forget()
            self.contenedor3.pack_forget()
            self.contenedor4.pack_forget()
            self.contenedor5.pack_forget()
        elif contenedor == "configuracion":
            self.contenedor1.pack_forget()
            self.contenedor2.pack()
            self.contenedor3.pack_forget()
            self.contenedor4.pack_forget()
            self.contenedor5.pack_forget()
            self.contenedor7.pack_forget()
            self.contenedor8.pack_forget()
            self.contenedor9.pack_forget()
        elif contenedor == "metricas_recalculo":
            self.contenedor1.pack_forget()
            self.contenedor2.pack_forget()
            self.contenedor3.pack()
            self.contenedor4.pack_forget()
            self.contenedor5.pack_forget()
        elif contenedor == "columnas_fijas":
            self.contenedor1.pack_forget()
            self.contenedor2.pack_forget()
            self.contenedor3.pack_forget()
            self.contenedor4.iniciar_desplegable()
            self.contenedor4.pack()
            self.contenedor5.pack_forget()
        elif contenedor == "previsualizar":
            self.contenedor1.pack_forget()
            self.contenedor2.pack_forget()
            self.contenedor3.pack_forget()
            self.contenedor4.pack_forget()
            self.contenedor5.iniciar_contenedor()
            self.contenedor5.pack()
        elif contenedor == "generar_vdb":
            self.contenedor1.pack_forget()
            self.contenedor2.pack_forget()
            self.contenedor3.pack_forget()
            self.contenedor4.pack_forget()
            self.contenedor5.pack_forget()
            self.contenedor6.pack()
            self.contenedor6.iniciar_contenedor()
        elif contenedor == "configurar_nessus":
            self.contenedor2.pack_forget()
            self.contenedor7.iniciar_desplegables()
            self.contenedor7.pack()
        elif contenedor == "configurar_criticidades":
            self.contenedor2.pack_forget()
            self.contenedor8.iniciar_desplegables()
            self.contenedor8.pack()
        elif contenedor == "configurar_vdb":
            self.contenedor2.pack_forget()
            self.contenedor9.iniciar_desplegables()
            self.contenedor9.pack()

if __name__ == "__main__":
    root = ctk.CTk()
    app = AplicacionPrincipal(root)
    app.pack()
    root.mainloop()
