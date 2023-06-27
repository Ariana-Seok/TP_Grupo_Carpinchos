# Integracion de todas las partes 
import dato_rosco
from filtrado_dicc import palabra_sin_acento
from diccionarioArchivo import manejo_datos
from registracion_jugadores import asignar_turnos

ACIERTO = "a"
ERROR = "e"
MAX = "FIN"

ultimo = [MAX, "final"]

def leer_archivo(archivo):
    """
    La funcion se encargar de leer una linea del archivo correctamente abierto.
    PRE: Necesitara recibir por parametro un archivo correctamente abierto.
    POST: Devolvera una lista
    """
    linea = archivo.readline()
    if linea:
        registro = linea.rstrip("\n").split(";")
    else:
        registro = ultimo
    return registro

def mostrar_tablero(lista_letras, referencias, resultados, posicion, letra,
                    long_palabra, definicion, jugadores,turno_jugador,
                    palabra_correcta):
    """
    La funcion se encarga de mostrar por pantalla el tablero del juego.
    PRE: Todos sus parametros deben estar inicializados.
    POST: Muestra por pantalla el tablero del juego
    """
    print(f"""
{''.join(f'[{letra.upper()}]' for letra in lista_letras)}
{''.join(f'[{referencia}]' for referencia in referencias)}
{''.join(f'[{resultado}]' for resultado in resultados)}
{' ' * (posicion * 3 + 1)}^
""")

    for referencia, jugador in enumerate(jugadores, start=1):
        aciertos_jugador = jugadores[jugador]["aciertos"]
        errores_jugador = jugadores[jugador]["errores"]
        print(f"{referencia}. {jugador} - Aciertos: {aciertos_jugador} - Errores: {errores_jugador}")

    print(f"""
Turno {list(jugadores.keys()).index(turno_jugador) + 1}. {turno_jugador} - letra: {letra.upper()} Longitud palabra: {long_palabra}
Definicion: {definicion}
Palabra correcta: {palabra_correcta}
""")

def cargar_palabra_valida():
    """
    La funcion se encarga de cargar un dato a la variable palabra.
    PRE: La variable "palabra" solo puede almacenar algo de tipo strig
    POST: Devuelve la variable "palabra" ya cargada
    """
    palabra = input("Ingrese la palabra: ").lower()
    while not palabra.isalpha():
        print("Ingrese solo LETRAS!")
        palabra = input("Ingrese la palabra: ").lower()
    return palabra_sin_acento(palabra)

def respuesta_verificada():
    """
    La funcion se encarga de cargar valor a la variable "respuesta" la cual debe ser de tipo str.
    PRE: La variable "respuesta" solo almacenara algo de tipo str (las cuales seran "si" o "no")
    POST: Devuelve a la variable respuesta ya cargada.
    """
    respuesta = palabra_sin_acento(input("\n¿Deseas seguir jugando? (si/no): ").lower())
    while respuesta != "si" and respuesta != "no":
        print("\nPor favor, ingrese 'si' o 'no'")
        respuesta = palabra_sin_acento(input("¿Deseas seguir jugando? (si/no): ").lower())
    return respuesta
#---prueba de doctest!
def analizar_respuesta(puntajes, resultado, puntaje_acierto, puntaje_desacierto):
    """
    La funcion se encarga de sumar o restar valores a las componentes que tenga dicha lista ya inicializada.
    PRE: Se debe recibir por parametros una lista inicializada con componentes de tipo int, y una variable de tipo str.
    POST: Retorna la lista con sus componentes de tipo int.
    >>> analizar_respuesta([0, 0, 0], 'a')
    [1, 0, 10]
    >>> analizar_respuesta([0, 0, 0], 'e')
    [0, 1, -3]
    >>> analizar_respuesta([1, 2, 4], 'a')
    [2, 2, 14]
    """
    if (resultado == ACIERTO):
        puntajes[0] += 1
        puntajes[2] += puntaje_acierto
    else:
        puntajes[1] += 1
        puntajes[2] -= puntaje_desacierto
    return puntajes

def turno_del_jugador(jugadores, turno_jugador, posicion, lista_letras, 
                    resultados, palabra, definicion, referencias, puntaje_acierto, puntaje_desacierto):
    """
    La funcion se encarga de cargar los datos del jugador que tiene el turno de jugar.
    PRE: Recibe por parametros variables ya inicializadas.
    POST: Devuelve dos variables de tipo str.
    """
    jugador_actual = jugadores[turno_jugador]
    letra = palabra[0]
    resultados_puntaje = [0, 0, 0]
    long_palabra = len(palabra)
    mostrar_tablero(lista_letras, referencias, resultados, posicion, letra, long_palabra, definicion, jugadores,
                    turno_jugador, palabra)

    palabra_ingresada = cargar_palabra_valida()
    resultado = ACIERTO if palabra_ingresada == palabra else ERROR
    resultados[posicion] = resultado
    referencias[posicion] = str(list(jugadores.keys()).index(turno_jugador) + 1)
    resultados_puntaje = analizar_respuesta(resultados_puntaje, resultado, puntaje_acierto, puntaje_desacierto)

    # Actualizar puntajes del jugador actual
    jugador_actual["aciertos"] += resultados_puntaje[0]
    jugador_actual["errores"] += resultados_puntaje[1]
    jugador_actual["puntos"] += resultados_puntaje[2]
    jugador_actual["resultados"].append(resultado)
    
    return resultado, palabra_ingresada

def mostrar_puntaje_jugadores(jugadores):
    """
    La funcion se encarga de mostrar los puntajes de los jugadores.
    PRE: La funcion recibe un diccionario con clave <nombre_jugador> y valor <datos_jugador> de tipo dict.
    POST: Muestra por pantalla los puntajes de los jugadores.
    """
    for jugador in jugadores:
        referencia = jugadores[jugador]["referencia"]
        puntos = jugadores[jugador]["puntos"]
        print(f"{referencia}. {jugador} - {puntos} puntos.")

def mostrar_resultados_partida_actual(puntajes_ordenados, jugadores):
    """
    La funcion se encarga de mostrar los puntajes de la partida actual.
    PRE: Recibe por parametros una lista y un diccionario
    POST: Muestra por pantalla los puntajes de la partida actual.
    """
    print("\nPuntaje de la partida:\n")
    for jugador, puntaje in puntajes_ordenados:
        referencia = jugadores[jugador]["referencia"]
        print(f"{referencia}. {jugador} - {puntaje} puntos")

def puntaje_partida_actual(jugador, resultado_turno, puntajes, puntaje_acierto, puntaje_desacierto):
    """
    La funcion se encarga verificar los resultados obtenidos de la ronda completada y cargar sus respectivos valores.
    PRE: Recibe por parametros dos variables de tipo str y una variable de tipo dict.
    POST: Devuelve una lista ordenada dependiendo de su puntaje
    >>> puntaje_partida_actual("jugador1", "a", {"jugador1": 0}, 10, 5)
    [('jugador1', 10)]

    >>> puntaje_partida_actual("jugador2", "e", {"jugador1": 10, "jugador2": 5}, 10, 5)
    [('jugador1', 10), ('jugador2', 0)]

    >>> puntaje_partida_actual("jugador3", "a", {"jugador1": 10, "jugador2": 0, "jugador3": 0}, 10, 5)
    [('jugador1', 10), ('jugador2', 0), ('jugador3', 10)]
    """
    if (jugador not in puntajes) :
        puntajes[jugador] = 0
    if (resultado_turno == ACIERTO):
        puntajes[jugador] += puntaje_acierto
    elif(resultado_turno == ERROR):
        puntajes[jugador] -= puntaje_desacierto
    puntajes_ordenados = sorted(puntajes.items(), key=lambda x: x[0], reverse=False)
    return puntajes_ordenados

def mostrar_resumen_partida(resumen_partida, jugadores, puntaje_acierto, puntaje_desacierto):
    """
    La funcion se encarga de mostrar el resumen de la partida: Indica que palabras ingreso el usuario,
    y si fueron incorrectas muestra que palabra se esperaba, en caso contrario solo muestra la palabra.
    Asimismo tambiem se muestra los puntajes de la partida actual y el puntaje parcial del total de partidas
    que se jugaron.
    """
    print("--- Resumen de la partida ---\n")
    palabras_ingresadas = {}
    puntajes = {}
    #letra.upper(), turno_jugador, palabra_ingresada, resultado, palabra
    for letra_turno, jugador_turno, palabra_ingresada_turno, resultado_turno, palabra_correcta_turno in resumen_partida:
        if jugador_turno not in palabras_ingresadas:
            palabras_ingresadas[jugador_turno] = 0
        if resultado_turno == ACIERTO:
            print(f"Turno letra {letra_turno} - Jugador {jugador_turno} Palabra de {len(palabra_correcta_turno)} letras - {palabra_ingresada_turno} - acierto ")
        elif resultado_turno == ERROR:
            palabras_ingresadas[jugador_turno] += len(palabra_correcta_turno)
            print(f"Turno letra {letra_turno} - Jugador {jugador_turno} Palabra de {len(palabra_correcta_turno)} letras - {palabra_ingresada_turno} - error - Palabra correcta: {palabra_correcta_turno}")
        puntajes_ordenados = puntaje_partida_actual(jugador_turno, resultado_turno, puntajes, puntaje_acierto, puntaje_desacierto)
    mostrar_resultados_partida_actual(puntajes_ordenados, jugadores)
    print("\nPuntaje parcial:\n")
    mostrar_puntaje_jugadores(jugadores)

def mostrar_reporte_final(partidas_jugadas, jugadores):
    """
    La funcion se encarga de mostrar por pantalla el reporte del estado
    de los puntos de los jugadores respecto a sus partidas totales.
    PRE: La funcion recibe una variable de tipo int y un diccionario ya cargado.
    POST: Muestra por pantalla los puntajes finales.
    """
    """
    >>> jugadores = {'Juan': 10, 'María': 15, 'Pedro': 8}
    >>> mostrar_reporte_final(5, jugadores)
    Reporte Final:
    Partidas jugadas: 5

    Puntaje Final:
    Jugador: Juan - Puntos: 10
    Jugador: María - Puntos: 15
    Jugador: Pedro - Puntos: 8
    """

    print("\nReporte Final:")
    print(f"Partidas jugadas: {partidas_jugadas}")

    print("\nPuntaje Final:")
    mostrar_puntaje_jugadores(jugadores)

def continuar_partida(jugar_pasapalabra):
    """
    La funcion se encarga de dar valor a la variable "jugar_pasapalabra",
    dependiendo de la respuesta que tenga almacenada la variabel "respuesta".
    PRE: La funcion recibe una variable con un valor booleano.
    POST: La funcion retorna la variable
    """
    respuesta = respuesta_verificada()
    if(respuesta == "no"):
        jugar_pasapalabra = False
    return jugar_pasapalabra

def cargar_datos_de_la_partida(datos_rosco, lista_letras, jugadores,
                                resultados, referencias, jugar_pasapalabra, puntaje_acierto, puntaje_desacierto):
    """
    Esta funcion se encarga de realizar la partida, y cargar los datos de la partida en la lista "resumen_partida".
    Esta funcion dejara de iterar siempre y cuando la variable "jugar_pasapalabra" almacene "False" o si se sobre pasa
    la cantidad de palabras presentes para el rosco.
    """
    resumen_partida = []
    
    posicion = 0
    jugadores_keys = list(jugadores.keys())
    num_jugadores = len(jugadores_keys)
    turno_jugador = jugadores_keys[0]

    while posicion < len(datos_rosco) and jugar_pasapalabra:
        palabra = datos_rosco[posicion][0]
        definicion = datos_rosco[posicion][1]
        letra = palabra[0]
        long_palabra = len(palabra)
        resultado, palabra_ingresada = turno_del_jugador(jugadores, turno_jugador, posicion, lista_letras, resultados, palabra, definicion, referencias, puntaje_acierto, puntaje_desacierto)
        respuesta = (resultado == ACIERTO)
        resumen_partida.append((letra.upper(), turno_jugador, palabra_ingresada, resultado, palabra))
        referencias[posicion] = str(list(jugadores.keys()).index(turno_jugador) + 1)  # Actualizar la referencia en cada turno
        resultados[posicion] = resultado
        posicion += 1
        if respuesta or posicion == len(datos_rosco):
            mostrar_tablero(lista_letras, referencias, resultados, posicion, letra, long_palabra, definicion, jugadores, turno_jugador, palabra_ingresada)
            if resultado != ACIERTO:
                turno_jugador = jugadores_keys[(jugadores_keys.index(turno_jugador) + 1) % num_jugadores]
        else:
            turno_jugador = jugadores_keys[(jugadores_keys.index(turno_jugador) + 1) % num_jugadores]
        
    return resumen_partida
#---prueba de doctest!
def cargar_referencia(jugadores):
    """
    La funcion se encarga de agregarle un valor a cada clave que 
    contenga el diccionario "jugadores".
    >>> cargar_referencia({'Laura12!': {'aciertos': 0, 'errores': 1},
    'Carlozan9!': {'aciertos': 2, 'errores': 1}})
    {'Laura12!': {'aciertos': 0, 'errores': 1, 'referencia': 1},
    'Carlozan9!': {'aciertos': 2, 'errores': 1, 'referencia': 2}}
    >>> cargar_referencia({'Xande312!': {'aciertos': 5, 'errores': 10},
    'Marcoz10!!9!': {'aciertos': 6, 'errores': 0}})
    {'Xande312!': {'aciertos': 5, 'errores': 10, 'referencia': 1},
    'Marcoz10!!9!': {'aciertos': 6, 'errores': 0, 'referencia': 2}}
    """
    referencia = 1
    for jugador in jugadores.keys():
        jugadores[jugador]["referencia"] = referencia
        referencia += 1
    return jugadores

def cargar_jugadores(lista_jugadores, jugadores):
    for jugador in lista_jugadores:
        jugadores[jugador] = {"referencia": 0, "aciertos": 0, "errores": 0, "puntos": 0, "resultados": [], "palabras_ingresadas": []}
    return jugadores

def iniciar_juego(jugar_pasapalabra, partidas_jugadas, jugadores, diccionario_palabra_def, max_partidas, puntaje_acierto, puntaje_desacierto, cant_letras_rosco):
    """
    La funcion se encarga interactiva con todos los datos de la partida, desde el cargado de letras,
    para el rosco, las palabras y definiciones para el rosco, mostrar el resumen, siempre y cuando 
    "jugar_pasapalabra" tenga almacenano "True", en caso contrario el juego no seguira.
    Otro de los requisitos para que inicie el juego es que debe tener almenos un jugador.
    """
    while (partidas_jugadas < max_partidas)and jugar_pasapalabra and (len(jugadores) > 0):
        resultados = [" " for i in range(cant_letras_rosco)]
        referencias = [" " for i in range(cant_letras_rosco)]
        print("\n-----  Comienza el Juego ------")
        partidas_jugadas += 1
        lista_letras = dato_rosco.cargar_letras(cant_letras_rosco)
        datos_rosco = dato_rosco.cargar_palabras_definiciones(diccionario_palabra_def, lista_letras)
        resumen_partida = cargar_datos_de_la_partida(datos_rosco, lista_letras, jugadores, resultados, referencias, jugar_pasapalabra, puntaje_acierto, puntaje_desacierto)
        mostrar_resumen_partida(resumen_partida, jugadores, puntaje_acierto, puntaje_desacierto)
        if not(partidas_jugadas == max_partidas):
            jugar_pasapalabra = continuar_partida(jugar_pasapalabra)
        
    return partidas_jugadas

def juego_pasapalabra(lista_jugadores, max_partidas, puntaje_acierto, puntaje_desacierto, max_long_palabra, cant_letras_rosco):
    """
    Esta funcion se encarga de cargar a los jugadores que jugaran al pasapalabra, 
    asimismo tambien se encarga de llamar a la funcion iniciar_juego para pasarle los datos de
    partidas_jugadas, el diccionario de palabras, y en caso de que el juego no continue mostrara
    un reporte final de las partidas que se hayan jugado.
    """
    jugadores = {}
    jugar_pasapalabra = True
    partidas_jugadas = 0
    
    jugadores = cargar_referencia(cargar_jugadores(lista_jugadores, jugadores))
    if not jugadores:
        print("No hay jugadores registrados. El juego no puede continuar.")

    diccionario_palabra_def= manejo_datos(max_long_palabra)
    partidas_jugadas = iniciar_juego(jugar_pasapalabra, partidas_jugadas, jugadores, diccionario_palabra_def, max_partidas, puntaje_acierto, puntaje_desacierto, cant_letras_rosco)

    mostrar_reporte_final(partidas_jugadas, jugadores)

def jugar(configuraciones):
    jugadores = asignar_turnos()
    configuracion = [configuracion for configuracion in configuraciones.items()]
    max_long_palabra = int(configuracion[0][1])
    cant_letras_rosco = int(configuracion[1][1])
    max_partidas = int(configuracion[2][1])
    puntaje_acierto = int(configuracion[3][1])
    puntaje_desacierto = int(configuracion[4][1])
    juego_pasapalabra(jugadores, max_partidas, puntaje_acierto, puntaje_desacierto, max_long_palabra, cant_letras_rosco)

import doctest
doctest.testmod()