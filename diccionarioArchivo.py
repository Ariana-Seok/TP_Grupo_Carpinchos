# Etapa 8 - Archivos de Texto

from filtrado_dicc import palabra_sin_acento
MAX = "ZZZZ"

def leer_archivo(archivo):
    """
    La funcion se encarga de leer una linea del archivo.
    PRE: El archivo debe estar abierto correctamente
    POST: Devuelve una linea del archivo
    """
    linea = archivo.readline()
    if (linea):
        registro = linea.rstrip("\n")
    else:
        registro = MAX
    return registro

def cargar_archivo(archivo, palabra, definicion):
    """
    La funcion recibe 3 parametros, un archivo abierto correctamente,
    y dos variables.
    La funcion se encarga de escribir en el archivo recibido.
    """
    archivo.write(palabra + "," + definicion + "\n")

def cargar_palabras_definiciones(arPalabra, arDefiniciones, long_palabra):
    """
    La funcion se encarga de crear una lista auxiliar con las palabras definiciones
    candidatas para el juego.
    PRE: La funcion debe recibir dos archivos que estan abiertos correctamente.
    POST: Devuelve una lista auxiliar ordenada alfabeticamente.
    """
    palabra = leer_archivo(arPalabra)
    definicion = leer_archivo(arDefiniciones)
    lista_aux = []
    while(palabra != MAX) and (definicion != MAX):
        if(palabra.isalpha()) and (len(palabra) >= long_palabra):
            lista = [palabra_sin_acento(palabra), definicion]
            lista_aux.append(lista)
            palabra = leer_archivo(arPalabra)
            definicion = leer_archivo(arDefiniciones)
        else:
            palabra = leer_archivo(arPalabra)
            definicion = leer_archivo(arDefiniciones)
    return sorted(lista_aux, key=lambda x: x[0].replace("ñ", "n~"))

def cargar_diccionario(lista_aux):
    """
    La funcion se encarga de cargar los datos recibidos de la lista
    auxiliar en un diccionario con clave letra y valor una lista de tipo
    [palabra(str), defincion(str)]
    PRE: La funcion debe recibir una lista cargada.
    POST: La funcion devuelve un diccionario.
    """
    diccionario_datos = {}
    for palabra, definicion in lista_aux:
        letra = palabra[0]
        if (letra not in diccionario_datos):
            diccionario_datos[letra] = [[palabra, definicion]]
        else:
            diccionario_datos[letra].append([palabra, definicion])
    return diccionario_datos

def cargar_datos(diccionario_datos, archivo):
    """
    La funcion se encarga de cargar los datos del diccionario en un
    archivo csv.
    PRE: La funcion debe recibir un diccionario cargado y un archivo 
    abierto correctamente.
    POST: La funcion se encarga de subir los valores que hay en dicho diccionario
    """
    palabra = 0
    definicion = 1
    for contenido_letra in diccionario_datos.values():
        i = 0
        while(i < len(contenido_letra)):
            columna1 = contenido_letra[i][palabra]
            columna2 = contenido_letra[i][definicion]
            cargar_archivo(archivo, columna1, columna2)
            i += 1

def manejo_datos(long_palabra):
    """
    Esta funcion se encarga de abrir los archivos y cerrarlos correctamente luego de la interaccion con ellos.
    La funcion retorna un diccionario con claves ordenadas alfabeticamente
    """
    palabras = open("Archivos de Texto a Utilizar - TP Grupal-20230619\palabras.txt", "rt", encoding="utf-8", errors="ignore")
    definiciones = open("Archivos de Texto a Utilizar - TP Grupal-20230619\definiciones.txt", "rt", encoding="utf-8", errors="ignore")
    datos = open("diccionario.csv", "w", encoding="utf-8", errors="ignore")
    lista_aux = cargar_palabras_definiciones(palabras, definiciones, long_palabra)
    diccionario_rosco = cargar_diccionario(lista_aux)
    cargar_datos(diccionario_rosco, datos)
    palabras.close()
    definiciones.close()
    datos.close()
    return diccionario_rosco



