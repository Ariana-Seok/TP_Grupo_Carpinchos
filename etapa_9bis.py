import dato_rosco
from filtrado_dicc import cargar_datos_para_rosco, palabra_sin_acento

ACIERTO = "a"
ERROR = "e"


MAX = "ZZZZZZ"
ultimo = [MAX, "final"]

def leer_archivo(archivo):
    """
    La funcion se encarga de leer una linea del archivo.
    PRE: El archivo debe estar abierto correctamente
    POST: Devuelve una lista con dos componentes
    """
    linea = archivo.readline()
    if (linea):
        registro = linea.rstrip("\n").split(";")
    else:
        registro = ultimo
    return registro


def mostrar_tablero(lista_letras, referencias, resultados, posicion, letra, long_palabra, definicion, jugadores, turno_jugador):
    """
    La funcion se encarga de mostrar por pantalla el tablero del juego.
    PRE: Recbe dos lista y 6 variables (4 de tipo int y 2 de tipo str)
    POST: Muestra por pantalla el estado del juego
    """
    print(f"""
{''.join(f'[{letra.upper()}]' for letra in lista_letras)}
{''.join(f'[{referencia}]' for referencia in referencias)}
{''.join(f'[{resultado}]' for resultado in resultados)}
{' ' * (posicion * 3 + 1)}^¨
""")
    for jugador in jugadores:
        referencia_jugador = jugadores[jugador][0]
        aciertos_jugador = jugadores[jugador][1]
        errores_jugador = jugadores[jugador][2]
        print(f"{referencia_jugador}. {jugador} - Aciertos: {aciertos_jugador} - Errores: {errores_jugador}")
    print(f"""
Turno {jugadores[turno_jugador][0]}. {turno_jugador} - letra: {letra.upper()} Longitud palabra: {long_palabra}
Definicion: {definicion}
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

def analizar_respuesta(resultados, resultado):
    """
    La funcion se encarga de cargar los puntos dependiendo de lo
    que haya en la variable resultado.
    PRE: Recibe dos parametros; una lista y una variable 
    POST: Retorna la lista añadiendo valor a sus componentes.
    """
    aciertos = resultados[0]
    errores = resultados[1]
    puntaje = resultados[2]

    if (resultado == ACIERTO):
        aciertos += 1
        puntaje += 10
    else:
        errores += 1
        puntaje -= 3
    return resultados

def jugar_turno(jugadores, turno_jugador, posicion, lista_letras, resultados, palabra, definicion, referencias):
    """
    La funcion recibe 7 parametros los cuales deben ser;
    3 variables de tipo int, 2 listas que sus componentes 
    sean de tipo str y dos variables que sean de tipo str
    totas inicializadas.
    La funcion devuelve 4 variables las cuales son 3 de tipo
    int y una str
    """
    letra = palabra[0]
    resultados_puntaje = [0, 0, 0]
    long_palabra = len(palabra)
    mostrar_tablero(lista_letras, referencias, resultados, posicion, letra, long_palabra, definicion, jugadores, turno_jugador)

    palabra_ingresada = cargar_palabra_valida()
    resultado = ACIERTO if (palabra_ingresada == palabra) else ERROR
    resultados[posicion] = resultado
    resultados_puntajes = analizar_respuesta(resultados_puntaje, resultado)

    datos = [resultados, resultados_puntaje[0], resultados_puntaje[1],resultados_puntaje[2], palabra_ingresada]
    #resultados, aciertos, errores, puntaje, palabra_ingresada
    return datos

def mostrar_resumen_de_juego(diccionario_rosco, jugadores, resultados):
    print("\n--- Resumen de Juego ---")
    for jugador in jugadores:
        print(f"\nJugador: {jugador['nombre']}")
        for i in range(len(diccionario_rosco)):
            #palabra_correcta = list(diccionario_rosco.keys())[i]
            palabra = list(diccionario_rosco.keys())[i]
            resultado = resultados[jugador["referencia"]][i] if i < len(resultados[jugador["referencia"]]) else ""
            definicion = diccionario_rosco[palabra]
            print(f"Palabra: {palabra} - Definición: {definicion} - Resultado: {resultado}")

def juego_inicializado(datos_rosco, lista_letras, jugadores, resultados, referencias):
    """
    La funcion recibe 3 listas inicializadas y 
    retorna los puntos totales de dicha partida
    """
    posicion = 0
    while(posicion < len(datos_rosco)):
        for jugador in jugadores.keys():
            aciertos = jugadores[jugador][1]
            errores = jugadores[jugador][2]
            puntaje = jugadores[jugador][3]
            palabras_ingresadas = []
            usuario = jugador
            respuesta = True
            while(posicion < len(datos_rosco)) and (respuesta):
                palabra = datos_rosco[posicion][0]
                definicion = datos_rosco[posicion][1]
                print(palabra)
                letra = palabra[0]
                long_palabra = len(palabra)
                datos = jugar_turno(jugadores, usuario, posicion, lista_letras, resultados, palabra, definicion, referencias)
                #[respuesta,aciertos, errores, puntaje, palabra_ingresada]
                aciertos += datos[1]
                errores += datos[2]
                puntaje += datos[3]
                palabras_ingresadas.append(datos[4])
                respuesta = datos[0]
                posicion += 1
            jugadores[jugador].append(palabras_ingresadas)
        posicion += 1
#lista_letras, referencias, resultados, posicion, letra, long_palabra, definicion, jugadores, turno_jugador
    mostrar_tablero(lista_letras, referencias, resultados, posicion, letra, long_palabra, definicion, jugadores, usuario)
    #mostrar_resumen_de_juego(lista_datos_rosco, palabras_ingresadas, resultados)

def cargar_datos_jugador(jugadores, aciertos, errores, puntaje):
    referencia = 1
    for jugador in jugadores.keys():
        jugadores[jugador].append(referencia)
        jugadores[jugador].append(aciertos)
        jugadores[jugador].append(errores)
        jugadores[jugador].append(puntaje)
        referencia += 1
    return jugadores

def cargar_jugadores(jugadores, archivo):
    datos = leer_archivo(archivo)
    while(datos != ultimo):
        jugador = datos[0]
        jugadores[jugador] = []
        datos = leer_archivo(archivo)
    return jugadores

def jugar_rosco(archivo):
    #Inicializo variables y un diccionario
    aciertos = 0
    errores = 0
    puntaje = 0
    jugadores = {}
    resultados = [" " for i in range(10)]
    referencias = [" " for i in range(10)]

    jugador = cargar_jugadores(jugadores, archivo)
    jugadores = cargar_datos_jugador(jugador, aciertos, errores, puntaje)

    diccionario_palabra_def= cargar_datos_para_rosco()
    jugar_pasapalabra = True

    print("\n--- Comienza el Juego ---")

    while jugar_pasapalabra:
        lista_letras = dato_rosco.cargar_letras()
        datos_rosco = dato_rosco.cargar_palabras_definiciones(diccionario_palabra_def, lista_letras)
        jugadores = juego_inicializado(datos_rosco, lista_letras, jugadores, resultados, referencias)

        """
        puntaje_total += puntaje_partida
        print(f"\nEl puntaje de la partida es: {puntaje_partida}")
        respuesta = respuesta_verificada()
        if (respuesta == "no"):
            continuar_jugando = False
        else:
            resultado = [" " for i in range(10)]
        
        """
        
        """
        for palabra in diccionario_rosco.keys():
            definicion = diccionario_rosco[palabra]
            puntos, palabra_ingresada = jugar_turno(jugadores, lista_letras, resultados, palabra, definicion)
            if palabra_ingresada == "fin":
                print("Juego terminado.")
                mostrar_resumen_de_juego(diccionario_rosco, jugadores, resultados)
        """
        


def jugadores_a_jugar():
    jugadores = open("usuarios.csv","r")
    jugar_rosco(jugadores)
    jugadores.close()

jugadores_a_jugar()











jugar_rosco()