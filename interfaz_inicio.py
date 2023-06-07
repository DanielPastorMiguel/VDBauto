import customtkinter as ctk
import controlador
import utiles_interfaz
import utiles
from tkinter import filedialog as fd

class Inicio(ctk.CTkFrame):

    boton_introducir_vdb = None
    boton_introducir_nessus_report = None

    vdb_valido = False
    nessus_valido = False

    def __init__(self, parent):
        ctk.CTkFrame.__init__(self, parent)
        self.parent = parent

        self.boton_introducir_vdb=ctk.CTkButton(self, text="Introducir VDB", font=("Arial", 24), border_spacing=15, fg_color="red", hover_color="dark red", command=self.boton_introducir_vdb_command)
        self.boton_introducir_vdb.pack(side=ctk.TOP, fill=ctk.BOTH, expand=1, padx=100, pady=(40, 20))

        self.boton_introducir_nessus_report=ctk.CTkButton(self, text="Introducir Nessus Report", font=("Arial", 24), border_spacing=15, fg_color="red", hover_color="dark red", command=self.boton_introducir_nessus_report_command)
        self.boton_introducir_nessus_report.pack(side=ctk.TOP, fill=ctk.BOTH, expand=1, padx=100, pady=20)

        boton_iniciar=ctk.CTkButton(self, text="Iniciar", font=("Arial", 24), border_spacing=10, command=self.boton_iniciar_command)
        boton_iniciar.pack(side=ctk.TOP, padx=80, pady=20)

        texto_configuracion=ctk.CTkLabel(self, text="¿Desea cambiar la configuración?")
        texto_configuracion.pack(side=ctk.LEFT, padx=(10, 10), pady=(15, 10))
        boton_configurar=ctk.CTkButton(self, text="Configurar", fg_color="#272b28", hover_color="#333834", command=self.boton_configurar_command)
        boton_configurar.pack(side=ctk.LEFT, padx=(0, 20), pady=(15, 12))

        self.texto_autor=ctk.CTkLabel(self, text="Desarrollado por \nDaniel Pastor Miguel", font=ctk.CTkFont(family="Calibri", size=12, slant="italic"), text_color="#707070")
        self.texto_autor.pack(side=ctk.RIGHT, padx=20, pady=(15, 10))
        
        self.validaciones_iniciales()

    def validaciones_iniciales(self):
        try:
            controlador.validar_configuracion()
        except Exception as exc:
            utiles_interfaz.mostrar_error(exc)
        try:
            controlador.validar_api_key()
        except Exception as exc:
            utiles_interfaz.mostrar_error(exc)
        try:
            controlador.iniciar_gestion_logs()
        except Exception as exc:
            utiles_interfaz.mostrar_error(exc)

    def boton_introducir_vdb_command(self):
        ruta_vdb = fd.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
        
        if (ruta_vdb != ""): #Ha cerrado la pestaña de askopenfilename
            
            dialogo = ctk.CTkInputDialog(title='VDBauto', text='Introduce el nombre del componente a analizar\n\nNota: introduce n/a para saltar verificacion')
            
            componente = dialogo.get_input()
            
            if (componente != None and componente != ""): #Ha cerrado el InputDialog
                try:
                    controlador.validar_vdb(utiles.formatear_ruta(ruta_vdb), componente)
                    utiles_interfaz.mostrar_info("VDB introducido correctamente")
                    self.vdb_introducido_actualizar_estado(True)
                except Exception as exc:
                    utiles_interfaz.mostrar_error(exc)
                    self.vdb_introducido_actualizar_estado(False)
            else:
                utiles_interfaz.mostrar_error("Error al introducir el VDB, no ha introducido el nombre del componente a analizar")
                self.vdb_introducido_actualizar_estado(False)

    def boton_introducir_nessus_report_command(self):
        ruta_nessus_report = fd.askopenfilename(filetypes=[("CSV Files", "*.csv")])

        if (ruta_nessus_report != ""): #Ha cerrado la pestaña de askopenfilename
            try:
                controlador.validar_nessus(utiles.formatear_ruta(ruta_nessus_report))
                utiles_interfaz.mostrar_info("Reporte Nessus introducido correctamente")
                self.nessus_introducido_actualizar_estado(True)
            except Exception as exc:
                utiles_interfaz.mostrar_error(exc)
                self.nessus_introducido_actualizar_estado(False)

    def boton_iniciar_command(self):
        if (self.nessus_valido and self.vdb_valido):
            self.mostrar_siguiente("metricas_recalculo")
        elif self.nessus_valido: #No ha metido un VDB
            utiles_interfaz.mostrar_error('Debe introducir un VBD valido, aunque unicamente contenga la cabecera para poder generar un VDB acorde al introducido')
        else:
            utiles_interfaz.mostrar_error("Debe introducir un reporte de Nessus valido")

    def boton_configurar_command(self):
        self.mostrar_siguiente("configuracion")

    def vdb_introducido_actualizar_estado(self, estado):
        if (estado):
            self.vdb_valido = True
            self.boton_introducir_vdb.configure(fg_color=['#2CC985', '#2FA572'], hover_color=['#0C955A', '#106A43'])
        else:
            self.vdb_valido = False
            self.boton_introducir_vdb.configure(fg_color="red", hover_color="dark red")
    
    def nessus_introducido_actualizar_estado(self, estado):
        if (estado):
            self.nessus_valido = True
            self.boton_introducir_nessus_report.configure(fg_color=['#2CC985', '#2FA572'], hover_color=['#0C955A', '#106A43'])
        else:
            self.nessus_valido = False
            self.boton_introducir_nessus_report.configure(fg_color="red", hover_color="dark red")
        
    def mostrar_siguiente(self, contenedor):
        self.parent.mostrar_contenedor(contenedor)