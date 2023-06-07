import configuracion
import utiles
import logging
import logging.handlers
import openpyxl
import csv
import os

conf = None

def validar_configuracion():
    global conf
    try:
        conf = configuracion.Configuracion()
        claves = list(conf.configuracion.keys())
        if ("vdb" in claves and "vdb_generado" in claves):
            claves_vdb_generado = list(conf.configuracion["vdb_generado"].keys())
            if ("nessus" in claves_vdb_generado and "columnas_criticidades" in claves_vdb_generado):
                pass
            else:
                raise Exception("Error en la configuración de VDBauto, por favor, configure la aplicación desde el panel de configuración")
        else:
            raise Exception("Error en la configuración de VDBauto, por favor, configure la aplicación desde el panel de configuración")
    except FileNotFoundError:
        raise FileNotFoundError("No se encuentra el fichero de configuracion. Asegurese de que en el directorio raiz de VDBauto se encuentre un fichero llamado 'configuracion.json'")
    except Exception:
        raise Exception("Error en la configuración de VDBauto, por favor, configure la aplicación desde el panel de configuración")

def iniciar_gestion_logs():
    nivel_log = logging.INFO
    try:
        if (conf.configuracion["nivel_log"] == "info"):
            nivel_log = logging.INFO
        elif (conf.configuracion["nivel_log"] == "debug"):
            nivel_log = logging.DEBUG
        elif (conf.configuracion["nivel_log"] == "warning"):
            nivel_log = logging.WARNING
        elif (conf.configuracion["nivel_log"] == "error"):
            nivel_log = logging.ERROR
        else:
            conf.configuracion["nivel_log"] = "info"
            conf.guardar_configuracion()
            raise Exception("Se ha encontrado un error en la configuracion de logs, Se ha corregido estableciendo el nivel de logs a 'info'. Puede cambiarlo si lo desea desde el menu de configuracion")
    except Exception:
        conf.configuracion["nivel_log"] = "info"
        conf.guardar_configuracion()
        raise Exception("Se ha encontrado un error en la configuracion de logs, Se ha corregido estableciendo el nivel de logs a 'info'. Puede cambiarlo si lo desea desde el menu de configuracion")
    
    os.makedirs("logs/", exist_ok=True) #Crea la carpeta donde se guardan los logs si no existe ya
    logHandler = logging.handlers.RotatingFileHandler('logs/vdbauto_logs.log', maxBytes=1048576, backupCount=2)
    logHandler.setLevel(nivel_log)
    
    logging.basicConfig(
        level=nivel_log,
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%d-%m-%Y %H:%M:%S',
        handlers=[logHandler],
    )
    
    logging.addLevelName(conf.vdbauto_nivel_log, 'vdbauto')

def validar_nessus(ruta_nessus):
    try:
        conf.ruta_nessus = ruta_nessus

        conf.fichero_nessus = open(ruta_nessus, mode ='r')
        
        conf.nessus_reader = csv.reader(conf.fichero_nessus, delimiter=',')
        cabecera = next(conf.nessus_reader)
        
        lista_cabeceras_conf = list(conf.configuracion["vdb_generado"]["nessus"].keys())
        if len(lista_cabeceras_conf) < 2: 
            raise Exception("Configuración de Nessus errónea. Es obligatorio la presencia de las columnas que contengan los Plugin ID y los CVEs del Nessus report. Cambie la configuración de VDBauto")

        fila_comprobar_vul = next(conf.nessus_reader) #Segunda fila para comprobar que en la conf esten bien puestas las columnas que contienen los plugin id y los cves
        indice_plugin_id = utiles.get_indice_columna_nessus(cabecera, lista_cabeceras_conf[0]) #la primera entrada del json "vdb_generado" "nessus" tiene que ser el plugin id
        
        if not fila_comprobar_vul[indice_plugin_id].isdigit(): #comprueba que esa columna contenga plugins id (unicamente digitos)
            raise Exception("Configuración de Nessus errónea. La columna que contiene los Plugin ID es incorrecta. Cambie la configuración de VDBauto")
        
        conf.fichero_nessus.seek(0) #reseteamos para no perder la vulnerabilidad de la fila 1 que hemos usado para la comprobacion

        columnas_faltantes = set(lista_cabeceras_conf) - set(cabecera)
        if columnas_faltantes != set():
            raise Exception("Faltan en el Nessus report las columnas " + str(columnas_faltantes) + ". Introduzca un Nessus report válido o cambie la configuración por defecto de VDBauto")
    except FileNotFoundError:
        raise FileNotFoundError("La ruta del reporte Nessus introducida no es válida")
    except UnicodeDecodeError:
        raise Exception("El reporte Nessus introducido no tiene un formato válido. Debe ser un csv")
    except ValueError:
        raise ValueError("Configuración de Nessus errónea. Introduzca un Nessus report válido o cambie la configuración de VBDauto")
    except Exception:
        raise Exception("Error en la validación del reporte de Nessus")

def validar_vdb(ruta_vdb, componente_seleccionado):
    try:
        vdb_fichero = openpyxl.load_workbook(ruta_vdb)
        conf.vdb_hoja = vdb_fichero[conf.configuracion["vdb"]["hoja"]]
        
        cabecera = utiles.get_cabecera_xlsx(conf.vdb_hoja)[0]

        if conf.configuracion["vdb"]["columna_vulnerabilidad"] not in cabecera:
            raise Exception("La cabecera del VDB no contiene la columna '"+conf.configuracion["vdb"]["columna_vulnerabilidad"]+"' introduzca un VDB válido o cambie la configuración de VDB")
        if conf.configuracion["vdb"]["columna_componente"] not in cabecera:
            raise Exception("La cabecera del VDB no contiene la columna '"+conf.configuracion["vdb"]["columna_componente"]+"' introduzca un VDB válido o cambie la configuración de VDB")
        
        indice_columna_componentes = cabecera.index(conf.configuracion["vdb"]["columna_componente"])
        componentes = []
        for celda in conf.vdb_hoja[utiles.asignar_letra_a_numero(indice_columna_componentes)]:
            componentes.append(celda.value)
        numero_ocurrencias_componente = 0
        for componente in componentes:
            if componente == componente_seleccionado : numero_ocurrencias_componente += 1
        
        if numero_ocurrencias_componente == 0:
            if (componente_seleccionado != "n/a" and componente_seleccionado != "N/A"):
                logging.warning("No hay ninguna entrada para el componente '" + componente_seleccionado + "' en el VDB introducido")
                raise BufferError("No hay ninguna entrada para el componente '" + componente_seleccionado + "' en el VDB introducido")
        
        conf.ruta_vdb = ruta_vdb #Hay que ponerlo aqui abajo por si mete un componente que no este en el VDB. Si esto pasa el VDB no se acepta y por tanto en interfaz_previsualizar debe salir 'VDB: No introducido'
        conf.componente = componente_seleccionado
            
    except FileNotFoundError:
        raise FileNotFoundError("La ruta del VDB introducido no es valida")
    except openpyxl.utils.exceptions.InvalidFileException:
        raise openpyxl.utils.exceptions.InvalidFileException("El VDB introducido tiene un formato erroneo, introduzca un VDB con formato xlsx")
    except PermissionError:
        raise PermissionError("VDBauto no tiene permisos suficientes para abrir el VDB. Compruebe que el fichero no este actualmente abierto o cambie los permisos")
    except IndexError:
        raise IndexError("El indice del libro del VDB no es valido, cambie la configuración por defecto de VDBauto")
    except KeyError:
        raise Exception("La hoja '" + conf.configuracion["vdb"]["hoja"] + "' no se encuentra en el VDB. Introduzca un VDB válido o cambie la configuración por defecto de VDBauto")

def validar_api_key():
    try:
        if(conf.configuracion["nist_api_key"] == ""):
            raise Exception("Error en la configuración. Introduce la API Key")
    except KeyError:
        raise KeyError("Error en la configuracion. No se encuentra la API key de NIST")