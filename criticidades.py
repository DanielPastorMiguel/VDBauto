import requests
import json
from cvss import CVSS3

def peticion_cve_api_nist(cve, api_key):
    """Hace una peticion a la API de Nist.gov para un CVE dado"""
    url = f"https://services.nvd.nist.gov/rest/json/cves/2.0/?cveId={cve}"
    cabecera = {'apiKey': api_key}
    answer = requests.get(url=url, headers=cabecera)

    if (answer.status_code != 200):
        raise Exception("ERROR en la petición a la API para el cve: " + cve)

    return json.loads(answer.text)

def get_cvss2_cvss3_base_score_api_nist(respuesta):
    """Extrae CVSS2.0 basescore y CVSS3.0 o CVSS3.1 basescore de una respuesta a una peticion API a Nist.gov"""
    impact = respuesta["vulnerabilities"][0]["cve"]["metrics"] #Devuelve error si el CVE no esta en la API
    
    try:
        cvssv2_basescore = impact["cvssMetricV2"][0]["cvssData"]["baseScore"]
    except Exception:
        cvssv2_basescore = "N/A"
    
    try:
        cvssv3_basescore = impact["cvssMetricV30"][0]["cvssData"]["baseScore"]
    except Exception:
        try: 
            cvssv3_basescore = impact["cvssMetricV31"][0]["cvssData"]["baseScore"] #Si da un error porque no tiene cvss3.0, que guarde el cvss3.1
        except Exception: #si vuelve a saltar excepcion es porque solo tiene criticidad cvss2.0
            cvssv3_basescore = "N/A"

    return cvssv2_basescore, cvssv3_basescore

def get_version_cvss3_api_nist(respuesta):
    """Extrae la version cvss3.0 o cvss3.1 de una respuesta a una peticion a la API de Nist.gov. Devuelve 3.0, 3.1 o N/A si no tiene cvss version 3"""
    try:
        respuesta["vulnerabilities"][0]["cve"]["metrics"]["cvssMetricV30"]
        return "3.0"
    except Exception:
        try:
            respuesta["vulnerabilities"][0]["cve"]["metrics"]["cvssMetricV31"]
            return "3.1"
        except Exception:
            return "N/A"

def get_vector_ataque_cvss3_api_nist(respuesta):
    """Extrae el vector de ataque cvss3.0 o cvss3.1 de una respuesta a una peticion a la API de Nist.gov. Devuelve el vector o N/A si no tiene"""
    try:
        return respuesta["vulnerabilities"][0]["cve"]["metrics"]["cvssMetricV30"][0]["cvssData"]["vectorString"]
    except Exception:
        try:
            return respuesta["vulnerabilities"][0]["cve"]["metrics"]["cvssMetricV31"][0]["cvssData"]["vectorString"]
        except Exception:
            return "N/A"
        

def get_fecha_publicacion_cve_api_nist(respuesta):
    """Extrae la fecha de publicacion de una respuesta a una peticion a la API de Nist.gov"""
    return respuesta["vulnerabilities"][0]["cve"]["published"]

def get_recalculo_cvssv3(vector_ataque, confidencialidad, integridad, disponibilidad):
    """Recibe un vector de ataque y devuelve el valor cvss3.0 o cvss3.1 enviromental en base a los valores de confidencialidad, integridad y disponibilidad dados"""
    vector_ataque = vector_ataque.replace("\\", "")
    vector_ataque = vector_ataque + f"/CR:{confidencialidad}/IR:{integridad}/AR:{disponibilidad}"
    calculadora = CVSS3(vector_ataque)
    return calculadora.environmental_score

