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
# Etapa 4 - Integracion
# Etapa 6 - Refactorizacion del Codigo de la Parte 1

from dato_rosco import cargar_letras, cargar_palabras_definiciones
from filtrado_dicc import palabra_sin_acento, cargar_datos_para_rosco
ACIERTO = "a"
ERROR = "e"

def mostrar_tablero(lista_letras, resultados, aciertos, errores, posicion, letra, long_palabra, definicion):
    """
    La funcion se encarga de mostrar por pantalla el tablero del juego.
    PRE: Recbe dos lista y 6 variables (4 de tipo int y 2 de tipo str)
    POST: Muestra por pantalla el estado del juego
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
    La función se encarga de cargar valor a la variable "palabra"
    """
    palabra = input("Ingrese la palabra: ").lower()
    while not palabra.isalpha():
        print("Ingrese solo LETRAS!")
        palabra = input("Ingrese la palabra: ").lower()
    return palabra_sin_acento(palabra)

def analizar_respuesta(dicc_resultados, resultado):
    """
    La funcion se encarga de cargar los puntos dependiendo de lo
    que haya en la variable resultado.
    PRE: Recibe dos parametros; un diccionario y una variable 
    POST: Retorna el diccionario cargando añadiendo valor a las 
    mencionadas claves.
    """
    if (resultado == ACIERTO):
        dicc_resultados["aciertos"] += 1
        dicc_resultados["puntos"] += 10
    else:
        dicc_resultados["errores"] += 1
        dicc_resultados["puntos"] -= 3

    return dicc_resultados

def jugar_turno(resultados_puntaje, posicion, lista_letras, resultados, palabra, definicion):
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
    resultado = ACIERTO if (palabra_ingresada == palabra) else ERROR
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
        resultado = ACIERTO if (palabra_jugador == palabra_correcta) else ERROR
        mostrar_resultado(resultado, letra, long_palabra, palabra_jugador, palabra_correcta)
        posicion += 1
    print("-" * 90)

def juego_inicializado(lista_datos_rosco, lista_letras, resultados):
    """
    La funcion recibe 3 listas inicializadas y 
    retorna los puntos totales de dicha partida
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

def respuesta_verificada():
    """
    La funcion se encarga de agregarle un valor a la
    variable "respuesta" la cual tiene que ser un "si" o un "no"
    """
    respuesta = palabra_sin_acento(input("¿Camarada deseas seguir jugando? (si/no): ").lower())
    while (respuesta != "si") and (respuesta != "no"):
        print("Por favor, ingrese 'si' o 'no'")
        respuesta = palabra_sin_acento(input("¿Camarada deseas seguir jugando? (si/no): ").lower())
    return respuesta

def jugar_rosco():
    long_palabra = 5
    resultado = [" " for i in range(10)]
    continuar_jugando = True
    puntaje_total = 0
    diccionario_datos_rosco = cargar_datos_para_rosco()

    while continuar_jugando:
        cant_letras = 10
        lista_letras = cargar_letras(cant_letras)
        palabras_definiciones = cargar_palabras_definiciones(diccionario_datos_rosco, lista_letras)
        puntaje_partida = juego_inicializado(palabras_definiciones, lista_letras, resultado)
        puntaje_total += puntaje_partida
        print(f"\nEl puntaje de la partida es: {puntaje_partida}")
        respuesta = respuesta_verificada()
        if (respuesta == "no"):
            continuar_jugando = False
        else:
            resultado = [" " for i in range(10)]
    
    print(f"\nPuntaje total: {puntaje_total}")

jugar_rosco()