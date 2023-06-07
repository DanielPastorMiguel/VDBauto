import configuracion
from datetime import datetime
import csv

conf = configuracion.Configuracion()

def get_cabecera_xlsx(hoja):
    """Saca los valores de la cabecera de un archivo xlsx"""
    cabecera1 = []
    cabecera2 = []
    for celda in hoja[1]:
        cabecera1.append(celda.value)
    for celda in hoja[2]:
        cabecera2.append(celda.value)
    return cabecera1, cabecera2

def get_indice_columna_vdb(hoja, titulo):
    """Devuelve el indice de la columna que tenga el titulo introducido como cabecera. Se devuelve en formato excel, es decir, se empieza por 1"""
    return get_cabecera_xlsx(hoja)[0].index(conf.configuracion["vdb"][titulo]) + 1

def get_indice_columna_nessus(cabecera, titulo):
    """Devuelve el indice de la columna que tenga el titulo introducido como cabecera. Se devuelve en formato lista, es decir, se empieza por 0"""
    return cabecera.index(titulo)

def get_indice_a_partir_columna(columna):
    """Obtiene un indice en función de una columna de una hoja de cálculo. Ej: a->0, b->1..."""
    return ord(columna) - 97

def asignar_letra_a_numero(numero):
    """Asigna una letra en base a un numero. Ej: 0->A, 1->B..."""
    return chr(numero+65)

def get_nombre_fichero(ruta):
    """Devuelve el nombre de un fichero dado su ruta. Ej: de C:/Users/.../nessus.csv devuelve nessus"""
    indice_inicial = ruta.rfind('\\')
    indice_final = ruta.rfind('.')
    return ruta[indice_inicial+1:indice_final]

def get_nombre_y_extension_fichero(ruta):
    """Devuelve el nombre de un fichero y su extension dado su ruta. Ej: de C:/Users/.../nessus.csv devuelve nessus.csv"""
    indice_inicial = ruta.rfind('\\')
    return ruta[indice_inicial+1:]

def formatear_fecha(fecha):
    """Recibe una fecha del tipo 2020-01-28T18:06:11.456 y devuelve 28/01/2020"""
    fecha_formateada = fecha[:fecha.rfind("T")]
    return voltear_fecha(fecha_formateada.replace("-", "/"))

def voltear_fecha(fecha):
    """Recibe una fecha del tipo 2020/07/11 y devuelve 11/07/2020"""
    fecha_split = fecha.split("/")
    return fecha_split[2]+"/"+fecha_split[1]+"/"+fecha_split[0]

def get_fecha_hora_actual():
    """Devuelve la fecha y hora actual siguiendo el formato dd-MM-YYYY_Thh-mm-ss"""
    now = datetime.now()
    return now.strftime("%d-%m-%Y_T%H-%M-%S")

def formatear_ruta(ruta):
    """Recibe un string en formato C:/Users/Daniel... y devuelve con la barra inversa"""
    return ruta.replace('/', '\\')

def get_rindex(lista, valor):
    """Devuelve el indice de la primera aparicion de un item que no sea el string pasado. Ej: [a, None, b, c, None, None] Si pasamos None devuelve -> 3"""
    lista.reverse()
    for i in range(len(lista)):
        if (lista[i] != valor):
            lista.reverse()
            return len(lista) - i - 1 
    lista.reverse()
    return len(lista)

def get_cabecera_csv(ruta_csv):
    fichero = open(ruta_csv, mode ='r')
    reader = csv.reader(fichero, delimiter=',')
    return next(reader)

def get_cabecera_xlsx_combinada(hoja):
    """Devuelve una lista de una cabecera combinada en 2 filas"""
    cabecera1 = get_cabecera_xlsx(hoja)[0]
    cabecera2 = get_cabecera_xlsx(hoja)[1]
    
    ultima_cabecera_combinada = ""
    for i in range(0, len(cabecera1)-1):
        if (cabecera2[i] != None):
            if (cabecera1[i] != None): ultima_cabecera_combinada = cabecera1[i]
            cabecera1[i] = ultima_cabecera_combinada+": "+cabecera2[i]
    return cabecera1