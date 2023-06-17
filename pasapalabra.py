"""
Etapa 4 - Integración
En esta etapa debemos integrar las funcionalidades resueltas en cada una de las etapas
anteriores, haciendo un uso adecuado de las funciones escritas.
La secuencia del juego debe ser la siguiente:
1. Se deberá comenzar con la generación del diccionario de palabras.
2. Luego se deben seleccionar las 10 letras participantes.
3. El programa elegirá al azar la lista de palabras a adivinar por el jugador.
4. Luego se armará el tablero que visualizará el usuario, y dará comienzo la partida,
implementando así, lo realizado en la etapa 1.
"""
import dato_rosco
from filtrado_dicc import cargar_datos_para_rosco, palabra_sin_acento

ACIERTO = "a"
ERROR = "e"
"""
def generar_diccionario():
    
    La funcion importa las funciones de dato_rosco.py
    y devuelve un diccionario con clave palabra y valor definicion,
    y tambien devuelve una lista_letras
    
    lista_letras, palabras, definiciones = dato_rosco.datos_rosco()
    datos_rosco = {}
    for i in range(len(lista_letras)):
        datos_rosco[palabras[i]] = definiciones[i]
    return datos_rosco, lista_letras

"""

def mostrar_tablero(lista_letras, resultados, aciertos, errores, posicion, letra, long_palabra, definicion):
    """
    Esta funcion recibe 4 parametros (2 listas y 2 variables (int)) y
    Muestra por pantalla el estado del juego.
    """
    print(f"""
{''.join(f'[{letra.upper()}]' for letra in lista_letras)}
{''.join(f'[{resultado}]' for resultado in resultados)}
{' ' * (posicion * 3 + 1)}^
Aciertos: {aciertos}
Errores: {errores}
Turno letra: {letra} Longitud palabra: {long_palabra} \nDefinicion: {definicion}
    """)

def cargar_palabra_valida():
    """
    La función recibe como parámetro una variable y retorna la variable de tipo string 
    """
    palabra = input("Ingrese la palabra: ").lower()
    while not palabra.isalpha():
        print("Ingrese solo LETRAS!")
        palabra = input("Ingrese la palabra: ").lower()
    return palabra_sin_acento(palabra)

def analizar_palabra_ingresada(palabra_ingresada, clave_palabra):
    """
    La funcion analiza el dato que haya en "palabra_ingresada",
    y en caso de que sea igual a "clave_palabra" retorna una "a"
    de ACIERTO y en caso contrario retorna una "e" de ERROR
    >>> analizar_palabra("pato", "pato")
    'a'
    >>> analizar_palabra("hecho", "hacha")
    'e'
    >>> analizar_palabra("caballo", "corbata")
    'e'
    """
    return ACIERTO if (palabra_ingresada == clave_palabra) else ERROR

def analizar_respuesta(dicc_resultados, resultado):
    if (resultado == ACIERTO):
        dicc_resultados["aciertos"] += 1
        dicc_resultados["puntos"] += 10
    else:
        dicc_resultados["errores"] += 1
        dicc_resultados["puntos"] -= 3

    return dicc_resultados

def jugar_turno(resultados_puntaje, posicion,
                lista_letras, resultados, palabra, definicion):
    """
    La funcion recibe 7 parametros los cuales deben ser;
    3 variables de tipo int, 2 listas que sus componentes 
    sean de tipo str y dos variables que sean de tipo str
    totas inicializadas.
    La funcion devuelve 4 variables las cuales son 3 de tipo
    int y una str
    """
    letra = palabra[0]
    aciertos = resultados_puntaje["aciertos"]
    errores = resultados_puntaje["errores"]
    long_palabra = len(palabra)
    mostrar_tablero(lista_letras, resultados, aciertos, errores,
                    posicion, letra, long_palabra, definicion)
    palabra_ingresada = cargar_palabra_valida()
    resultado = analizar_palabra_ingresada(palabra_ingresada, palabra)
    resultados[posicion] = resultado
    resultados_puntajes= analizar_respuesta(resultados_puntaje, resultado)

    return resultados_puntajes, palabra_ingresada

def mostrar_resultado (resultado, letra, long_palabra, palabra_jugador, palabra_correcta):
    """
    La funcion recibe 5 parametros; dos listas y 3 variables.
    La funcion muestra por pantalla; si los datos ingresados son
    correctos muestra un respetivo mensaje sino muestra otro mensaje.
    """
    if (resultado == ERROR):
        print(f"Turno de la letra: {letra} - Palabra de {long_palabra} letras - {palabra_jugador} - La palabra correcta es: {palabra_correcta}")
    else:
        print(f"Turno de la letra: {letra} - Palabra de {long_palabra} letras - {palabra_jugador}")

def mostrar_resumen_de_juego(lista_datos_rosco, 
                                palabras_ingresadas, resultado):
    """
    La funcion recibe tres parametros; 3 listas ya inicializadas.
    La funcion muestra por pantalla el resumen de la partida
    """
    print("\n-------- Resumen de la partida -----------")
    print("-" * 90)
    posicion = 0
    for palabra_definicion in lista_datos_rosco:
        palabra_correcta = palabra_definicion[0]
        letra = palabra_correcta[0]
        long_palabra = len(palabra_correcta)
        palabra_jugador = palabras_ingresadas[posicion]
        resultado = analizar_palabra_ingresada(palabra_jugador, palabra_correcta)
        mostrar_resultado(resultado, letra, long_palabra, palabra_jugador, palabra_correcta)
        posicion += 1
    print("-" * 90)

def juego_inicializado(lista_datos_rosco, lista_letras, resultados):
    """
    La funcion recibe 3 listas inicializadas y 
    retorna los puntos de dicha partida
    """
    resultados_puntaje = {"aciertos": 0, "errores": 0, "puntos": 0 }
    palabras_ingresadas = []
    posicion = 0
    for palabra, definicion in lista_datos_rosco:
        print(palabra)
        letra = palabra[0]
        long_palabra = len(palabra)
        resultado_puntaje, palabra_ingresada = jugar_turno(
            resultados_puntaje, posicion, lista_letras, resultados, palabra, definicion)
        aciertos = resultado_puntaje["aciertos"]
        errores = resultado_puntaje["errores"]
        palabras_ingresadas.append(palabra_ingresada)
        puntos_totales = resultado_puntaje["puntos"]
        posicion += 1

    mostrar_tablero(lista_letras, resultados, aciertos, errores, posicion, letra, long_palabra, definicion)
    mostrar_resumen_de_juego(lista_datos_rosco, palabras_ingresadas, resultados)
    return puntos_totales

def verificar_respuesta():
    """
    La funcion recibe como parametro a la variable "respuesta"
    con la cual trabajara para verificar que lo hay dentro de esa
    variable sea un "si" o un "no".
    La funcion retorna la variable con una cadena de caracteres que
    puede ser "si" o "no"
    """
    respuesta = palabra_sin_acento(input("¿Camarada deseas seguir jugando? (si/no): ").lower())
    while (respuesta != "si") and (respuesta != "no"):
        print("Por favor, ingrese 'si' o 'no'")
        respuesta = palabra_sin_acento(input("¿Camarada deseas seguir jugando? (si/no): ").lower())
    return respuesta

def jugar_rosco():
    resultado = [" " for i in range(10)]
    continuar_jugando = True
    puntaje_total = 0
    lista_letras = dato_rosco.cargar_letras()
    diccionario_datos_rosco = cargar_datos_para_rosco()

    while continuar_jugando:
        palabras_definiciones = dato_rosco.cargar_palabras_definiciones(diccionario_datos_rosco, lista_letras)
        puntaje_partida = juego_inicializado(palabras_definiciones, lista_letras, resultado)
        puntaje_total += puntaje_partida
        print(f"\nEl puntaje de la partida es: {puntaje_partida}")
        respuesta = ingresar_respuesta()
        if (respuesta == "no"):
            continuar_jugando = False
        else:
            resultado = [" " for i in range(10)]
    
    print(f"\nPuntaje total: {puntaje_total}")

jugar_rosco()