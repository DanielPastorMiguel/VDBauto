import customtkinter as ctk
import configuracion
import utiles
import utiles_interfaz
from tkinter import filedialog as fd
import openpyxl
import controlador

class InterfazConfiguracion(ctk.CTkFrame):

    conf = configuracion.Configuracion()

    def __init__(self, parent):
        ctk.CTkFrame.__init__(self, parent)
        self.parent = parent

        self.boton_introducir_vdb=ctk.CTkButton(self, text="Configurar VDB", font=("Arial", 24), border_spacing=15, command=self.boton_configurar_vdb)
        self.boton_introducir_vdb.pack(side=ctk.TOP, fill=ctk.BOTH, expand=1, padx=100, pady=(40, 20))

        self.boton_introducir_nessus_report=ctk.CTkButton(self, text="Configurar Nessus Report", font=("Arial", 24), border_spacing=15, command=self.boton_configurar_nessus_report)
        self.boton_introducir_nessus_report.pack(side=ctk.TOP, fill=ctk.BOTH, expand=1, padx=100, pady=20)

        self.boton_introducir_vdb=ctk.CTkButton(self, text="Configurar criticidades", font=("Arial", 24), border_spacing=15, command=self.boton_configurar_criticidades)
        self.boton_introducir_vdb.pack(side=ctk.TOP, fill=ctk.BOTH, expand=1, padx=100, pady=20)

        boton_iniciar=ctk.CTkButton(self, text="API Key", font=("Arial", 24), border_spacing=10, command=self.boton_configurar_api_key)
        boton_iniciar.pack(side=ctk.TOP, fill=ctk.BOTH, expand=1, padx=100, pady=20)

        boton_atras=ctk.CTkButton(self, text="Atrás", font=("Arial", 24), border_spacing=10, fg_color="#272b28", hover_color="#333834", command=self.mostrar_anterior)
        boton_atras.pack(side=ctk.TOP, padx=80, pady=20)
    
    def boton_configurar_vdb(self):
        utiles_interfaz.mostrar_info("Introduce un VDB para comenzar a configurar la aplicación")
        ruta_vdb = fd.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])

        if (ruta_vdb != ""): #Ha cerrado la pestaña de askopenfilename
            try:
                nombre_hoja = ctk.CTkInputDialog(title='VDBauto', text='Introduce el nombre de la hoja donde se encuentran las vulnerabilidades').get_input()
                self.conf.conf_hoja_vdb = nombre_hoja
                vdb_fichero = openpyxl.load_workbook(ruta_vdb)
                vdb_hoja = vdb_fichero[nombre_hoja]
                self.conf.conf_cabecera_vdb = utiles.get_cabecera_xlsx_combinada(vdb_hoja)
                self.mostrar_siguiente("configurar_vdb")
            except KeyError:
                utiles_interfaz.mostrar_error("No existe ninguna hoja con el nombre de "+nombre_hoja+" en el VDB introducido")
            except PermissionError:
                utiles_interfaz.mostrar_error("Debe cerrar el fichero VDB para que VDBauto pueda abrirlo")

    def boton_configurar_criticidades(self):
        utiles_interfaz.mostrar_info("Introduce un VDB para coger las cabeceras")
        ruta_vdb = fd.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
        
        if (ruta_vdb != ""):
            try:
                controlador.validar_vdb(ruta_vdb, "n/a")
                self.mostrar_siguiente("configurar_criticidades")
            except Exception as exc:
                utiles_interfaz.mostrar_error(exc)
        

    def boton_configurar_nessus_report(self):
        utiles_interfaz.mostrar_info("Introduce un reporte de Nessus para comenzar a configurar la aplicación")
        ruta_nessus_report = fd.askopenfilename(filetypes=[("CSV Files", "*.csv")])

        if (ruta_nessus_report != ""): #Ha cerrado la pestaña de askopenfilename
            self.conf.conf_cabecera_nessus_report = utiles.get_cabecera_csv(ruta_nessus_report)
            utiles_interfaz.mostrar_info("Introduce un VDB para coger las cabeceras")
            ruta_vdb = fd.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
            
            if (ruta_vdb != ""):
                try:
                    controlador.validar_vdb(ruta_vdb, "n/a")
                    self.mostrar_siguiente("configurar_nessus")
                except Exception as exc:
                    utiles_interfaz.mostrar_error(exc)

    def boton_configurar_api_key(self):
        dialogo = ctk.CTkInputDialog(title='VDBauto', text='Introduce la API Key de NIST')
        api_key = dialogo.get_input()

        if (api_key != None and api_key != ""): #Ha cerrado el InputDialog
            self.conf.cambiar_configuracion_api_key(api_key)
            self.conf.guardar_configuracion()
            utiles_interfaz.mostrar_info("API Key actualizada correctamente")
        else:
            utiles_interfaz.mostrar_error("La API Key introducida no es válida")

    def mostrar_siguiente(self, contenedor):
        self.parent.mostrar_contenedor(contenedor)

    def mostrar_anterior(self):
        self.parent.mostrar_contenedor("inicio")