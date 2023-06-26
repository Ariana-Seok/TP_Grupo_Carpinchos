# Etapa 2 - Construccion de un Diccionario de Palabras condidatas

from datos import obtener_lista_definiciones

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

def filtrar_lista():
    """
    La funcion necesitara llamar una funcion 
    del archivo "datos", con la cual realizara 
    un filtrado de palabras.
    La funcion devuelve una lista de listas ordenada
    alfabeticamente.
    """
    lista_definiciones = obtener_lista_definiciones()
    LONG_MIN = 5
    lista_definiciones = [[palabra_sin_acento(palabra), definicion] \
            for palabra, definicion in lista_definiciones \
                    if (len(palabra) >= LONG_MIN)]
    return sorted(lista_definiciones, key=lambda x: x[0].replace("ñ", "n~"))

def cargar_datos_para_rosco():
    """
    La funcion llamara a la funcion "filtrar_lista",
    la cual devuelve una lista de lista ya cargada.
    La funcion "cargar_datos_para_rosco" devuelve un
    diccionario con clave: letra y valor: una lista de
    listas de [palabra, definicion]
    """
    diccionario_rosco = {}
    lista_definiciones = filtrar_lista()

    for palabra, definicion in lista_definiciones:
        letra = palabra[0]
        lista_palabra_definicion = [palabra, definicion]
        if (letra not in diccionario_rosco):
            diccionario_rosco[letra] = [lista_palabra_definicion]
        else:
            diccionario_rosco[letra].append(lista_palabra_definicion)

    return diccionario_rosco

def contar_palabras(diccionario_rosco):
    """
    La funcion recibe como parametro un diccionario,
    con sus respectivos clave y valores.
    La funcion devuelve un diccionario el cual tiene
    como clave una letra y como valor una variable de tipo
    int

    >>> contar_palabras({"g": [["gasto", "1.  m. Acción de gastar"] ,\
            ["generar","1.  tr. Producir causar algo"]]})
    {'g': 2}
    >>> contar_palabras({"h": [["hache","1. f. Letra "], \
        ["hojuela","1.  f. Fruta de sartén muy extendida y delgada"],\
        ["hilada","1.  f. Formación en línea"]]})
    {'h': 3}
    """
    letra_cantidad = {}
    for letra in diccionario_rosco:
        cant_palabra = len(diccionario_rosco[letra])
        letra_cantidad[letra] = cant_palabra
    return letra_cantidad

def sumar_valores(letra_cantidad):
    """
    La funcion recibe como parametro un diccionario,
    con sus respectivos clave y valor.
    La funcion devuelve el total de la suma de valores
    que contenia el diccionario recibido.

    >>> sumar_valores({"l": 20, "m": 40, "n": 2, "o" : 1})
    63
    >>> sumar_valores({"a": 2, "b": 22, "c": 5, "d": 56})
    85
    >>> sumar_valores({"a": 22, "b": 5, "c": 14, "g": 4, "h": 6})
    51
    """
    totalsuma = 0
    for cantidad in letra_cantidad.values():
        totalsuma += cantidad
    return totalsuma

def mostrar_resultado(letras_cantidad, suma_total):
    """
    La funcion recibe dos parametros: "letras_cantidad"
    es un diccionario con clave letra y valor un numero,
    "suma_total" es un int 
    La funcion muestra por pantalla los datos de los parametros
    recibidos.

    >>> mostrar_resultado({"a": 2, "b": 22, "c": 5, "d": 56}, 85)
    La letra a tiene 2
    La letra b tiene 22
    La letra c tiene 5
    La letra d tiene 56
    El total de palabras presentes en el diccionario es de: 85
    """
    for letra in letras_cantidad:
        print("La letra", letra, "tiene", letras_cantidad[letra])

    print("El total de palabras presentes en el "
        "diccionario es de:", suma_total)

# Bloque Principal
dicc_rosco = cargar_datos_para_rosco()
letras_cantidad = contar_palabras(dicc_rosco)
suma_total = sumar_valores(letras_cantidad)

#mostrar_resultado(letras_cantidad, suma_total)
#import doctest
#print(doctest.testmod())