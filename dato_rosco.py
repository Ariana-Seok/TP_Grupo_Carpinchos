import random
# Aca conservamos algunas funciones utilizadas en la etapa 1 del TP
def cargar_letras(cant_letras_rosco):
    """
    La funcion retorna una lista de 10 letras aleatorias 
    que estan ordenadas alfabeticamente sin repetirse entre
    ellas mismas
    """
    letras = ['a', 'b', 'c', 'd', 'e', 'f', \
            'g', 'h', 'i', 'j', 'k', 'l', 'm',\
            'n', 'ñ', 'o', 'p', 'q', 'r', 's', \
            't', 'u', 'v', 'w', 'x', 'y', 'z']
    lista_letras = random.sample(letras, k = cant_letras_rosco)
    return sorted(lista_letras, key=lambda x: x.replace("ñ", "n~"))

def cargar_palabras_definiciones(diccionario_rosco, lista_letras):
    """
    La funcion recibe dos parametros; 1 diccionario el cual
    tiene como clave letra y valores una lista de listas de tipo
    [palabra(str), definicion(str)], y el segundo parametro que recibe
    es una lista que contiene 10 letras ordenadas alfabeticamente
    La funcion una lista de listas 
    """
    palabras_definiciones = []
    for letra in lista_letras:
        if(letra in diccionario_rosco):
            palabra_definicion = random.choice(diccionario_rosco[letra])
            palabras_definiciones.append(palabra_definicion)
    return palabras_definiciones

def palabra_sin_acento(palabra):
    """
    La funcion recibe como parametro una cadena de 
    caracteres y la devuelve sin acento

    >>> palabra_sin_acento('álbum')
    'album'
    >>> palabra_sin_acento('ácido')
    'acido'
    >>> palabra_sin_acento('brócoli')
    'brocoli'
    >>> palabra_sin_acento('transformó')
    'transformo'
    >>> palabra_sin_acento('préstamelo')
    'prestamelo'
    """
    vocales = "aeiou"
    vocales_con_acento = "áéíóú"
    for letra in range(len(vocales)):
        palabra = palabra.replace(vocales_con_acento[letra], vocales[letra])
    return palabra


