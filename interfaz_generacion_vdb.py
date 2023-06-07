import customtkinter as ctk
import tkinter as tk
import sys
import nessus_iterador
import configuracion

class InterfazGeneracionVdb(ctk.CTkFrame):
    
    conf = configuracion.Configuracion()
    iterador = None

    def __init__(self, parent):
        ctk.CTkFrame.__init__(self, parent)
        self.parent = parent
    
    def __on_exit__(self):
        """When you click to exit, this function is called"""
        if (self.iterador.progressbar._determinate_value != 1.0):
            if tk.messagebox.askyesno("VDB", "¿Seguro que quieres cerrar la aplicación en medio de la generación del VDB?"):
                self.parent.parent.destroy()
                sys.exit()    
        else:
            self.parent.parent.destroy()
            sys.exit() 
    
    def iniciar_contenedor(self):
        self.parent.parent.wm_protocol("WM_DELETE_WINDOW", self.__on_exit__)
        
        progressbar = ctk.CTkProgressBar(self, width=400)
        progressbar.pack(padx=60, pady=(30, 15))

        textbox = ctk.CTkTextbox(self, width=400, font=("Arial", 14))
        textbox.pack(padx=60, pady=(15, 30))

        textbox.bind("<Key>", lambda e: self.txtEvent(e)) #Para evitar que se pueda escribir en el TextBox. Si lo ponemos en disabled entonces no te deja insertar texto con .insert. Si lo dejas habilitado entonces el usuario manulamente puede escribir. De esta manera cada vez que pulsa una tecla le lleva al metodo que no hace nada

        self.iterador = nessus_iterador.Iterador_Nessus_Vdb(self.conf.componente, self.conf.columnas_fijas, self.conf.metricas_recalculo, self.conf.ruta_nessus, progressbar, textbox)
        self.iterador.daemon = True #Para que al hacer sys.exit() al cerrar la interfaz mate al hilo
        self.iterador.start()

    def txtEvent(self, event):
        if(event.state==12 and event.keysym=='c' ): #solo deja hacer ctrl+c para copiar, el resto devuelve "break" que hace que no escriba nada
            return
        else:
            return "break"