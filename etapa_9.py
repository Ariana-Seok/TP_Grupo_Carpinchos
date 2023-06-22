import csv
import dato_rosco
from filtrado_dicc import cargar_datos_para_rosco, palabra_sin_acento

ACIERTO = "a"
ERROR = "e"

MAX = "ZZZZZZ"
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
    palabra = input("Ingrese la palabra: ").lower()
    while not palabra.isalpha():
        print("Ingrese solo LETRAS!")
        palabra = input("Ingrese la palabra: ").lower()
    return palabra_sin_acento(palabra)

def respuesta_verificada():
    respuesta = palabra_sin_acento(input("\n¿Deseas seguir jugando? (si/no): ").lower())
    while respuesta != "si" and respuesta != "no":
        print("\nPor favor, ingrese 'si' o 'no'")
        respuesta = palabra_sin_acento(input("¿Deseas seguir jugando? (si/no): ").lower())
    return respuesta

def analizar_respuesta(puntajes, resultado):
    if resultado == ACIERTO:
        puntajes[0] += 1
        puntajes[2] += 10
    else:
        puntajes[1] += 1
        puntajes[2] += -3
    return puntajes

def jugar_turno(jugadores, turno_jugador, posicion, lista_letras, resultados, palabra, definicion, referencias):
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
    resultados_puntaje = analizar_respuesta(resultados_puntaje, resultado)

    # Actualizar puntajes del jugador actual
    jugador_actual["aciertos"] += resultados_puntaje[0]
    jugador_actual["errores"] += resultados_puntaje[1]
    jugador_actual["puntos"] += resultados_puntaje[2]
    jugador_actual["resultados"].append(resultado)
    
    return resultado, palabra_ingresada

def mostrar_puntaje(jugadores):
    for jugador in jugadores:
        referencia = jugadores[jugador]["referencia"]
        puntos = jugadores[jugador]["puntos"]
        print(f"{referencia}. {jugador} - {puntos} puntos.")

def mostrar_resultados_actual(puntajes_ordenados, jugadores):
    print("\nPuntaje de la partida:\n")

    for jugador, puntaje in puntajes_ordenados:
        referencia = jugadores[jugador]["referencia"]
        print(f"{referencia}. {jugador} - {puntaje} puntos")

def puntaje_partida_actual(jugador, resultado_turno, puntajes):
    if (jugador not in puntajes) :
        puntajes[jugador] = 0
    if (resultado_turno == ACIERTO):
        puntajes[jugador] += 10
    elif(resultado_turno == ERROR):
        puntajes[jugador] -= 3
    puntajes_ordenados = sorted(puntajes.items(), key=lambda x: x[1], reverse=True)
    return puntajes_ordenados

def mostrar_resumen_partida(resumen_partida, jugadores):
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
        puntajes_ordenados = puntaje_partida_actual(jugador_turno, resultado_turno, puntajes)
    mostrar_resultados_actual(puntajes_ordenados, jugadores)
    print("\nPuntaje parcial:\n")
    mostrar_puntaje(jugadores)

def mostrar_reporte_final(partidas_jugadas, jugadores):
    print("\nReporte Final:")
    print(f"Partidas jugadas: {partidas_jugadas}")

    print("\nPuntaje Final:")
    mostrar_puntaje(jugadores)

def verificar_resultado(resultado):
    return resultado == ACIERTO


def continuar_partida(jugar_pasapalabra):
    respuesta = respuesta_verificada()
    if(respuesta == "no"):
        jugar_pasapalabra = False
    return jugar_pasapalabra


def juego_inicializado(datos_rosco, lista_letras, jugadores, resultados, referencias, jugar_pasapalabra): #Cargar Datos de la partida
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
        resultado, palabra_ingresada = jugar_turno(jugadores, turno_jugador, posicion, lista_letras, resultados, palabra, definicion, referencias)
        respuesta = verificar_resultado(resultado)
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

def cargar_referencia(jugadores):
    referencia = 1
    for jugador in jugadores.keys():
        jugadores[jugador]["referencia"] = referencia
        referencia += 1
    return jugadores

def cargar_jugadores(jugadores, archivo):
    """
    Esta funcion se encarga de leer un archivo correctamente y segun
    la lectura de cierta linea se van cargando a un diccionario.
    """
    datos = leer_archivo(archivo)
    while(datos != ultimo):
        jugador = datos[0]
        jugadores[jugador] = {"referencia": 0, "aciertos": 0, "errores": 0, "puntos": 0, "resultados": [], "palabras_ingresadas": []}
        datos = leer_archivo(archivo)
    return jugadores

def iniciar_jugada(jugar_pasapalabra, partidas_jugadas, jugadores, diccionario_palabra_def):
    while jugar_pasapalabra and (len(jugadores) > 0):
        resultados = [" " for i in range(10)]
        referencias = [" " for i in range(10)]
        print("\n-----  Comienza el Juego ------")
        partidas_jugadas += 1
        lista_letras = dato_rosco.cargar_letras()
        datos_rosco = dato_rosco.cargar_palabras_definiciones(diccionario_palabra_def, lista_letras)
        resumen_partida = juego_inicializado(datos_rosco, lista_letras, jugadores, resultados, referencias, jugar_pasapalabra)
        mostrar_resumen_partida(resumen_partida, jugadores)
        jugar_pasapalabra = continuar_partida(jugar_pasapalabra)
    return partidas_jugadas
    
def juego_rosco(archivo):
    jugadores = {}
    jugar_pasapalabra = True
    partidas_jugadas = 0
    
    jugadores = cargar_referencia(cargar_jugadores(jugadores, archivo))
    if not jugadores:
        print("No hay jugadores registrados. El juego no puede continuar.")

    diccionario_palabra_def= cargar_datos_para_rosco()
    partidas_jugadas = iniciar_jugada(jugar_pasapalabra, partidas_jugadas, jugadores, diccionario_palabra_def)
    mostrar_reporte_final(partidas_jugadas, jugadores)

def main():
    try:
        archivo_jugadores = open("usuarios.csv", "r")
        juego_rosco(archivo_jugadores)
        archivo_jugadores.close()
    except FileNotFoundError:
        print("El archivo 'usuarios.csv' no se encontró.")

main()