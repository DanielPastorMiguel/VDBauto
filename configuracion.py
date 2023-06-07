import json

class Configuracion(object):
    """Clase que tiene como atributo la configuracion que se carga al iniciar la aplicación. 
    Esta implementada siguiendo el patron Singleton para evitar multiples instancias de esta clase"""

    configuracion = None
    ruta_configuracion = None
    ruta_vdb = None
    ruta_nessus = None

    fichero_nessus = None

    componente = None
    
    vdbauto_nivel_log = None
    
    nessus_reader = None
    vdb_hoja = None
    ruta_vdb_generado = None

    metricas_recalculo = []
    columnas_fijas = {}

    #Configuracion de Nessus Report
    conf_cabecera_nessus_report = None
    #Configuracion VDB
    conf_cabecera_vdb = None
    conf_hoja_vdb = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
          cls.instance = super(Configuracion, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.ruta_configuracion = "configuracion.json"
        self.cargar_configuracion()
        self.vdbauto_nivel_log = 25


    def cargar_configuracion(self):
        with open(self.ruta_configuracion) as json_file:
            self.configuracion = json.load(json_file)

    def guardar_configuracion(self):
        with open(self.ruta_configuracion, "w") as json_file:
            json.dump(self.configuracion, json_file, indent=4)

    def cambiar_configuracion_vdb(self, hoja, columna_vulnerabilidad, columna_componente, estado):
        self.configuracion["vdb"]["hoja"] = hoja
        self.configuracion["vdb"]["columna_vulnerabilidad"] = columna_vulnerabilidad
        self.configuracion["vdb"]["columna_componente"] = columna_componente
        self.configuracion["vdb"]["estado"] = estado

    def cambiar_configuracion_nessus(self, diccionario_nessus):
        self.configuracion["vdb_generado"]["nessus"] = diccionario_nessus

    def cambiar_configuracion_vdb_generado(self, diccionario_columnas_criticidades):
        self.configuracion["vdb_generado"]["columnas_criticidades"] = diccionario_columnas_criticidades
    
    def cambiar_configuracion_api_key(self, api_key):
        self.configuracion["nist_api_key"] = api_key