import configuracion
import vdb_generado
import utiles
import criticidades
import logging
import requests
import re
import time
from threading import Thread

class Iterador_Nessus_Vdb(Thread):

    conf = configuracion.Configuracion()

    componente = None
    columnas_fijas = None
    environmental_impact_subscore_modifiers = None
    ruta_nessus = None

    progressbar = None
    textbox = None

    vulnerabilidades_rejected = []

    def __init__(self, componente, columnas_fijas, environmental_impact_subscore_modifiers, ruta_nessus, progressbar, textbox):
        super().__init__()
        self.componente = componente
        self.columnas_fijas = columnas_fijas
        self.environmental_impact_subscore_modifiers = environmental_impact_subscore_modifiers
        self.ruta_nessus = ruta_nessus
        self.progressbar = progressbar
        self.textbox = textbox

    def run(self):
        logging.log(self.conf.vdbauto_nivel_log, "######## COMIENZA ITERACION DE "+utiles.get_nombre_fichero(self.conf.ruta_nessus)+" ########")
        self.insertar_texto_textbox("####### COMIENZA ITERACION DE "+utiles.get_nombre_fichero(self.conf.ruta_nessus)+" #######\n")
        
        self.iterar_nessus_csv(self.componente, self.columnas_fijas, self.environmental_impact_subscore_modifiers, self.ruta_nessus)
    
    def insertar_texto_textbox(self, texto):
        self.textbox.insert("end", texto)
        self.textbox.see("end")

    def iterar_nessus_csv(self, componente, columnas_fijas, environmental_impact_subscore_modifiers, ruta_nessus):
        
        vulnerabilidades_vdb = self.extraer_vulnerabilidades_vdb(self.conf.vdb_hoja, componente)
        vulnerabilidades_duplicadas = [] #almacena las vulnerabilidades que no se han insertado porque estaban en el vdb introducido
        vulnerabilidades_error = [] #almacena los cves que no se han añadido por un error en la peticion API

        lista_cabeceras_nessus_conf = list(self.conf.configuracion["vdb_generado"]["nessus"])
        cabeceras_nessus_csv = next(self.conf.nessus_reader) #sacamos las cabeceras del fichero csv Nessus para luego poder coger las columnas que se vayan a insertar en el metodo "anadir_columnas_nessus_fila"

        vdb_final = vdb_generado.Vdb_generado()

        plugin_id_anterior = "" #para evitar duplicidades ya que todos los cves asociados a un mismo plugin id tienen una entrada cada uno. (La aplicacion coge el plugin id y saca los CVEs que hay que meter, por tanto, las entradas que contienen esos CVEs en el excel no nos importan porque meten tambien las de Reference Information)

        numero_filas_total = sum(1 for row in self.conf.nessus_reader)

        self.conf.fichero_nessus.seek(0)
        next(self.conf.nessus_reader) #quitamos la cabecera

        indice_fila_plugin_id = utiles.get_indice_columna_nessus(cabeceras_nessus_csv, lista_cabeceras_nessus_conf[0])
        indice_fila_risk = utiles.get_indice_columna_nessus(cabeceras_nessus_csv, lista_cabeceras_nessus_conf[2])

        numero_fila_actual = 1
        for fila in self.conf.nessus_reader:
            vul_id = fila[indice_fila_plugin_id] #guardamos el plugin ID

            if fila[indice_fila_risk] != "None": #si tiene None en la columna de "Risk" es porque es INFO, y, por tanto, pasamos de largo
                if (vul_id != plugin_id_anterior): #para evitar la duplicidad
                    plugin_id_anterior = vul_id

                    fila_insertar = [""] * 26
                    
                    multiples_cves = [] #por si tiene varios CVEs asociados un plugin ID

                    indice_columna_cve = utiles.get_indice_columna_nessus(cabeceras_nessus_csv, lista_cabeceras_nessus_conf[1])
                    if fila[indice_columna_cve] != "": #si tiene CVE, entonces tenemos que hacer una petición http para extraer los CVEs asociados a ese plugin ID, ya que si usamos los del csv nos metería también los CVEs de Reference Information, los cuales no metemos
                        
                        conexion_tenable = True
                        contador_reintentos = 0
                        while(conexion_tenable):
                            try:
                                multiples_cves = self.extraer_cves_de_plugin_id(vul_id)
                                self.progressbar.configure(progress_color="#2CC985")
                                conexion_tenable = False
                                contador_reintentos = 0
                                    
                                for cve in multiples_cves:
                                    if cve in vulnerabilidades_vdb:
                                        self.insertar_texto_textbox("VULNERABILIDAD QUE CONTINÚA "+cve+"\n")
                                        logging.warning("vulnerabilidad que continúa: "+cve)
                                        vulnerabilidades_duplicadas.append(cve)
                                    else:
                                        self.anadir_columnas_fijas_fila(fila_insertar, columnas_fijas)
                                        self.anadir_columnas_nessus_fila(fila_insertar, cve, fila, cabeceras_nessus_csv)
                                        
                                        conexion_nist = True
                                        contador_reintentos = 0
                                        while (conexion_nist):
                                            try:
                                                time.sleep(2)
                                                
                                                respuesta = criticidades.peticion_cve_api_nist(cve, self.conf.configuracion["nist_api_key"])
                                                self.progressbar.configure(progress_color="#2CC985")
                                                cvss2_base_score, cvss3_base_score = criticidades.get_cvss2_cvss3_base_score_api_nist(respuesta) #devuelve una lista con cvss2.0 y cvss3.0 base scores
                                                version_cvss3 = criticidades.get_version_cvss3_api_nist(respuesta) #contiene 3.0, 3.1 o N/A
                                                vector_cvss3 = criticidades.get_vector_ataque_cvss3_api_nist(respuesta)
                                                fecha_publicacion_cve = criticidades.get_fecha_publicacion_cve_api_nist(respuesta)
                                                all_scores = self.get_criticidades_cve(cve, cvss2_base_score, cvss3_base_score, version_cvss3, vector_cvss3, environmental_impact_subscore_modifiers) #cvss2.0, cvss3.0 base, cvss3.1 base, cvss3.0 enviromental, cvss3.1 enviromental, fecha publicacion
                                                all_scores.append(utiles.formatear_fecha(fecha_publicacion_cve)) #añadimos la fecha de publicacion
                                                self.anadir_criticidades_fila(fila_insertar, all_scores)
                                                vdb_final.insertar_fila_vdb_generado(fila_insertar)
                                                
                                                conexion_nist = False
                                                contador_reintentos = 0
                                                logging.info("insertado el cve: "+cve+" que viene del plugin id: "+vul_id)
                                                self.insertar_texto_textbox("INSERTADO "+cve+"\n")
                                            except requests.exceptions.ConnectionError:
                                                if contador_reintentos == 0: 
                                                    logging.critical("El ordenador ha sido desconectado de internet durante la ejecucion de: "+cve+" asociado al plugin id: "+vul_id)
                                                    self.progressbar.configure(progress_color="red")
                                                    self.insertar_texto_textbox("CONEXIÓN A INTERNET PÉRDIDA\n")
                                                contador_reintentos += 1
                                                self.insertar_texto_textbox("REINTENTO DE CONEXIÓN "+str(contador_reintentos)+"\n")
                                                time.sleep(5)
                                            except Exception:
                                                logging.error("en la peticion API para la vulnerabilidad: "+cve+" que viene del plugin id: "+vul_id)
                                                self.insertar_texto_textbox("ERROR PETICION API PARA "+cve+"\n")
                                                vulnerabilidades_error.append(cve)
                                                conexion_nist = False

                            except requests.exceptions.ConnectionError:
                                if contador_reintentos == 0: 
                                    logging.critical("El ordenador ha sido desconectado de internet durante la ejecucion del plugin id: "+vul_id+" el cual contiene CVEs asociados")
                                    self.progressbar.configure(progress_color="red")
                                    self.insertar_texto_textbox("CONEXIÓN A INTERNET PÉRDIDA\n")
                                contador_reintentos += 1
                                self.insertar_texto_textbox("REINTENTO DE CONEXIÓN "+str(contador_reintentos)+"\n")
                                time.sleep(5)
                            except Exception:
                                logging.error("en la peticion HTTP para extraer los CVEs del plugin id: "+vul_id)
                                self.insertar_texto_textbox("ERROR PETICIÓN HTTP PARA PLUGIN ID "+vul_id+"\n")
                                vulnerabilidades_error.append(cve)
                                conexion_tenable = False

                    else: #Si no hay CVE, entonces se pone solo el plugin id
                        if vul_id in vulnerabilidades_vdb:
                                logging.info("vulnerabilidad que continúa: "+vul_id)
                                self.insertar_texto_textbox("VULNERABILIDAD QUE CONTINÚA PLUGIN ID"+vul_id+"\n")
                                vulnerabilidades_duplicadas.append(vul_id)
                        else:
                            self.anadir_columnas_fijas_fila(fila_insertar, columnas_fijas)
                            self.anadir_columnas_nessus_fila(fila_insertar, vul_id, fila, cabeceras_nessus_csv)
                            
                            claves = list(self.conf.configuracion["vdb_generado"]["nessus"].keys())  

                            conexion_tenable = True
                            contador_reintentos = 0
                            while conexion_tenable:
                                try:
                                    time.sleep(2)
                                    
                                    all_scores = self.get_criticidades_plugin_id(fila, cabeceras_nessus_csv, claves, vul_id, environmental_impact_subscore_modifiers) #cvss2.0, cvss3.0 base, cvss3.1 base, cvss3.0 enviromental, cvss3.1 enviromental
                                    self.progressbar.configure(progress_color="#2CC985")

                                    all_scores.append("") #el metodo anadir_criticalidades_fila añade tambien la fecha de publicacion. Añadimos esto para que no de error. Va a sobreescribir la fecha con "" pero da igual porque justo debajo vamos a añadir la fecha formateada sobreescribiendo este ""
                                    self.anadir_criticidades_fila(fila_insertar, all_scores)

                                    fila_insertar[utiles.get_indice_a_partir_columna(self.conf.configuracion["vdb_generado"]["nessus"][claves[5]])] = utiles.voltear_fecha(fila[utiles.get_indice_columna_nessus(cabeceras_nessus_csv, claves[5])]) #añadimos la fecha del plugin formateada

                                    vdb_final.insertar_fila_vdb_generado(fila_insertar)
                                    
                                    conexion_tenable = False
                                    contador_reintentos = 0
                                    logging.info("insertado el plugin id: "+vul_id)
                                    self.insertar_texto_textbox("INSERTADO PLUGIN ID "+vul_id+"\n")
                                
                                except requests.exceptions.ConnectionError:
                                    if contador_reintentos == 0: 
                                        logging.critical("El ordenador ha sido desconectado de internet durante la ejecucion del plugin id: "+vul_id)
                                        self.progressbar.configure(progress_color="red")
                                        self.insertar_texto_textbox("CONEXIÓN A INTERNET PÉRDIDA\n")
                                    contador_reintentos += 1
                                    self.insertar_texto_textbox("REINTENTO DE CONEXIÓN "+str(contador_reintentos)+"\n")
                                    time.sleep(5)
                                except Exception:
                                    logging.error("en la peticion HTTP para extraer el vector cvss3.X del plugin id: "+vul_id)
                                    self.insertar_texto_textbox("ERROR PETICION HTTP VECTOR CVSS3.X PLUGIN ID "+vul_id+"\n")
                                    vulnerabilidades_error.append(vul_id)
                                    conexion_tenable = False
            else:
                logging.debug("El plugin id: "+vul_id+" es una entrada de INFO, por tanto, no se inserta")
                self.insertar_texto_textbox("INFO: "+vul_id+"\n")
                self.textbox.see("end")
            
            self.progressbar.set(numero_fila_actual/(numero_filas_total+2))
            numero_fila_actual += 1
        
        
        self.insertar_duplicados_y_errores(vdb_final, vulnerabilidades_error, self.vulnerabilidades_rejected, vulnerabilidades_duplicadas, vulnerabilidades_vdb)

        self.progressbar.set(numero_fila_actual/(numero_filas_total))
        logging.log(self.conf.vdbauto_nivel_log, "######## FINALIZADA ITERACION DE "+utiles.get_nombre_fichero(ruta_nessus)+" ########")
        self.insertar_texto_textbox("###### FINALIZADA ITERACION DE "+utiles.get_nombre_fichero(ruta_nessus)+" ######")
    
    def insertar_duplicados_y_errores(self, vdb_final, vulnerabilidades_error, vulnerabilidades_rejected, vulnerabilidades_duplicadas, vulnerabilidades_antiguas):
        for i in range(2, len(vulnerabilidades_error)+2):
            vdb_final.insertar_celda(vdb_final.hoja2, i, 1, vulnerabilidades_error[i-2])
        
        for i in range(2, len(vulnerabilidades_rejected)+2):
            vdb_final.insertar_celda(vdb_final.hoja2, i, 3, vulnerabilidades_rejected[i-2])

        vulnerabilidades_pueden_cerrar = [item for item in vulnerabilidades_antiguas if item not in vulnerabilidades_duplicadas]
        for i in range(2, len(vulnerabilidades_pueden_cerrar)+2):
            vdb_final.insertar_celda(vdb_final.hoja2, i, 5, vulnerabilidades_pueden_cerrar[i-2])

        for i in range(2, len(vulnerabilidades_duplicadas)+2):
            vdb_final.insertar_celda(vdb_final.hoja2, i, 7, vulnerabilidades_duplicadas[i-2])
        
        vdb_final.workbook.save(vdb_final.ruta)

    def get_criticidades_cve(self, cve, cvss2_base_score, cvss3_base_score, version_cvss3, vector_cvss3, environmental_impact_subscore_modifiers):
        """Devuelve una lista con cvss2.0, cvss3.0 base, cvss3.1 base, cvss3.0 enviromental y cvss3.1 enviromental"""
        all_criticidades = []

        if version_cvss3 == "N/A": #solo hay cvss2.0
            if cvss2_base_score == "N/A": #ES UN CVE REJECTED (no tiene ni cvss3.x ni cvss2.0)
                all_criticidades.append("N/A")
                logging.warning(cve+" es un posible CVE rejected")
                self.insertar_texto_textbox("POSIBLE CVE REJECTED "+cve+"\n")
                self.vulnerabilidades_rejected.append(cve)
            else: all_criticidades.append(str(float(cvss2_base_score))) #lo pasamos a float para convertir lo 5 en 5.0 y luego a string porque sino si tienes el excel en español al insertarlo te convierte los . en , porque detecta que son numeros. Al ser un String no cambia nada
            for i in range(4):
                all_criticidades.append("N/A")
        
        elif version_cvss3 == "3.0":
            if cvss2_base_score == "N/A": all_criticidades.append("N/A") #Puede que tenga cvss3.x pero no tenga cvss2.0
            else: all_criticidades.append(str(float(cvss2_base_score))) #queremos que queden con 5.2. Reemplazamos las comas por puntos y convertimos a float para que pase los 5 a 5.0
            all_criticidades.append(str(float(cvss3_base_score))) #cvss3.0
            all_criticidades.append("N/A") #ponemos N/A al cvss3.1 base
            all_criticidades.append(str(float(criticidades.get_recalculo_cvssv3(vector_cvss3, environmental_impact_subscore_modifiers[0], environmental_impact_subscore_modifiers[1], environmental_impact_subscore_modifiers[2]))))
            all_criticidades.append("N/A") #ponemos N/A al cvss3.1 enviromental

        else: #es cvss3.1
            if cvss2_base_score == "N/A": all_criticidades.append("N/A") #Puede que tenga cvss3.x pero no tenga cvss2.0
            else: all_criticidades.append(str(float(cvss2_base_score)))
            all_criticidades.append("N/A") #ponemos N/A al cvss3.0 base
            all_criticidades.append(str(float(cvss3_base_score)))
            all_criticidades.append("N/A") #ponemos N/A al cvss3.0 enviromental
            all_criticidades.append(str(float(criticidades.get_recalculo_cvssv3(vector_cvss3, environmental_impact_subscore_modifiers[0], environmental_impact_subscore_modifiers[1], environmental_impact_subscore_modifiers[2]))))
        
        return all_criticidades

    def get_criticidades_plugin_id(self, fila, cabeceras_nessus_csv, claves, vul_id, environmental_impact_subscore_modifiers):
        """Devuelve una lista con cvss2.0, cvss3.0 base, cvss3.1 base, cvss3.0 enviromental y cvss3.1 enviromental"""
        all_scores = [] #cvss2.0, cvss3.0 base, cvss3.1 base, cvss3.0 enviromental, cvss3.1 enviromental, fecha_publicacion 
                            
        cvss2 = fila[utiles.get_indice_columna_nessus(cabeceras_nessus_csv, claves[3])]
        if (cvss2 == ""): all_scores.append("N/A") #Puede pasar que tenga un Risk Factor de High pero no tenga ni criticidad 2.0 ni 3.0.
        else: all_scores.append(str(float(cvss2))) #añadimos el CVSS2.0 basescore                    
                            
        cvss3 = fila[utiles.get_indice_columna_nessus(cabeceras_nessus_csv, claves[4])] #CVSS3.0 basescore.
        
        if (cvss3 == ""): #no tiene cvss3.x
                all_scores.append("N/A") #3.0 base
                all_scores.append("N/A") #3.1 base
                all_scores.append("N/A") #3.0 env
                all_scores.append("N/A") #3.1 env
        else:
            vector_cvss3 = self.extraer_vector_cvss3_plugin_id(vul_id)
            cvss3_recalculo = cvss3_recalculo = criticidades.get_recalculo_cvssv3(vector_cvss3, environmental_impact_subscore_modifiers[0], environmental_impact_subscore_modifiers[1], environmental_impact_subscore_modifiers[2])

            if vector_cvss3[:8] == "CVSS:3.0":
                all_scores.append(str(float(cvss3))) #3.0 base
                all_scores.append("N/A") #3.1 base
                all_scores.append(str(float(cvss3_recalculo))) #3.0 env
                all_scores.append("N/A") #3.1 env
            elif vector_cvss3[:8] == "CVSS:3.1":
                all_scores.append("N/A") #3.0 base
                all_scores.append(str(float(cvss3))) #3.1 base
                all_scores.append("N/A") #3.0 env
                all_scores.append(str(float(cvss3_recalculo))) #3.1 env
            else:
                logging.error("Error en la iteracion del plugin: "+vul_id)
        
        return all_scores

    def extraer_vulnerabilidades_vdb(self, vdb_hoja, componente):
        """Devuelve las vulnerabilidades abiertas de un componente dado, iterando un VDB"""
        vulnerabilidades_vdb_componente = []

        indice_columna_componentes = utiles.get_indice_columna_vdb(vdb_hoja, "columna_componente")
        indice_columna_id_vulnerabilidad = utiles.get_indice_columna_vdb(vdb_hoja, "columna_vulnerabilidad")
        indice_columna_status = utiles.get_indice_columna_vdb(vdb_hoja, "estado")

        for fila in range(3, vdb_hoja.max_row+1):
            if vdb_hoja.cell(row=fila, column=indice_columna_componentes).value == componente and vdb_hoja.cell(row=fila, column=indice_columna_status).value == "Open":
                vulnerabilidades_vdb_componente.append(vdb_hoja.cell(row=fila, column=indice_columna_id_vulnerabilidad).value)
        
        return vulnerabilidades_vdb_componente

    def extraer_cves_de_plugin_id(self, plugin_id):
        """Extrae los CVEs asociados a un plugin id en la parte de CVSS2.0 y CVSS3.0"""
        url = 'https://www.tenable.com/plugins/nessus/'+plugin_id
        r = requests.get(url)

        htmlRespuesta = r.content.decode("utf-8")

        indiceInicial = htmlRespuesta.index("Risk Information")
        indiceFinal = htmlRespuesta.index("Vulnerability Information")

        htmlFormateado = htmlRespuesta[indiceInicial:indiceFinal]

        cveRegex = re.compile(r'CVE-\d*-\d*<')
        cvesBuenos = cveRegex.findall(htmlFormateado)

        for i in range(len(cvesBuenos)): #Elimina el < en los strings con cves extraidos del html
            cvesBuenos[i] = cvesBuenos[i][:len(cvesBuenos[i])-1]

        return cvesBuenos

    def extraer_vector_cvss3_plugin_id(self, plugin_id):
        """Extrae el vector de ataque cvss3 de un plugin id"""
        url = 'https://www.tenable.com/plugins/nessus/'+plugin_id
        r = requests.get(url)

        htmlRespuesta = r.content.decode("utf-8")

        indiceInicial = htmlRespuesta.index("CVSS v3")
        indiceFinal = htmlRespuesta.index("Vulnerability Information")

        htmlFormateado = htmlRespuesta[indiceInicial:indiceFinal]

        indice_inicio_vector = htmlFormateado.rfind("CVSS:3.")
        vector = htmlFormateado[indice_inicio_vector:]
        indice_fin_vector = vector.find("<")
        vector = vector[:indice_fin_vector]

        return vector

    def anadir_columnas_fijas_fila(self, fila_insertar, columnas_fijas):
        """Añade las columnas fijas a la fila que se va a insertar en el VBD generado"""
        for clave, valor in columnas_fijas.items():
            fila_insertar[utiles.get_indice_a_partir_columna(clave)] = valor

    def anadir_columnas_nessus_fila(self, fila_insertar, id_vulnerabilidad, fila_nessus, cabeceras_nessus_csv):
        """Añade las columnas del reporte de Nessus a la fila que se va a insertar en el VBD generado (excepto el CVSS2.0 basescore ya que para los CVE se hace con la petición a la API y para los plugin en "iterar_nessus_csv"). Recibe la fila y el Plugin ID/CVE"""
        i=0
        for clave, valor in self.conf.configuracion["vdb_generado"]["nessus"].items():
            if valor != "n/a":
                if i==1: #se mete el plugin/cve
                    fila_insertar[utiles.get_indice_a_partir_columna(valor)] = id_vulnerabilidad
                else:
                    fila_insertar[utiles.get_indice_a_partir_columna(valor)] = fila_nessus[utiles.get_indice_columna_nessus(cabeceras_nessus_csv, clave)]
            i+=1

    def anadir_criticidades_fila(self, fila_insertar, cvs):
        """Recibe la fila donde se insertan las criticidades y una lista con las mismas en el siguiente orden: cvss2.0, cvss3.0 base, cvss3.1 base, cvss3.0 enviromental, cvss3.1 enviromental y fecha de publicacion"""
        i = 0
        for clave, valor in self.conf.configuracion["vdb_generado"]["columnas_criticidades"].items():
            fila_insertar[utiles.get_indice_a_partir_columna(valor)] = cvs[i]
            i+=1