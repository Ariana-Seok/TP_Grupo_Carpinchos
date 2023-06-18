import dato_rosco
from filtrado_dicc import cargar_datos_para_rosco, palabra_sin_acento

ACIERTO = "a"
ERROR = "e"

def mostrar_casillas_jugadores(jugadores):
    casillas_jugadores = ''.join(f'[{jugador["referencia"]}][{jugador["referencia"] + 1}]' if jugador["errores"] > 0 else '  ' for jugador in jugadores)
    return casillas_jugadores

def mostrar_tablero(lista_letras, resultados, aciertos, errores, letra, long_palabra, definicion, jugadores, palabra_correcta):
    jugador_actual = jugadores[0]
    referencia_jugadores = '\n'.join(f'{i+1}. {jugador["nombre"]} - Aciertos: {jugador["aciertos"]} - Errores: {jugador["errores"]}' for i, jugador in enumerate(jugadores))
    historial_resultados = [ ]
    for i in range(len(resultados[0])):
        turno_resultados = [ ]
        for j in range(len(jugadores)):
            turno_resultados.append(resultados[j][i] if i < len(resultados[j]) else ' ')
        historial_resultados.append(turno_resultados)
    historial_tablero = ''.join(f'[{"".join(resultado)}]' for resultado in historial_resultados)
    casillas_vacias = ''.join(f'[{jugador_actual["referencia"]}]' if i == lista_letras.index(letra.lower()) else '[ ]' for i in range(len(lista_letras)))
    print(f"""
{''.join(f'[{letra.upper()}]' for letra in lista_letras)}
{casillas_vacias}
{historial_tablero}

Jugadores:
{referencia_jugadores}
Turno letra: {letra} Longitud palabra: {long_palabra}
Definicion: {definicion}
Palabra correcta: {palabra_correcta}
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
    return ACIERTO if (palabra_ingresada == clave_palabra) else ERROR

def contar_puntos(resultado, jugador):
    if resultado == ACIERTO:
        jugador["aciertos"] += 1
        puntos = 10
    else:
        jugador["errores"] += 1
        puntos = -3
    return puntos

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

def cambiar_turno(jugadores):
    jugadores.append(jugadores.pop(0))

def jugar_turno(jugadores, lista_letras, resultados, palabra, definicion):
    jugador_actual = jugadores[0]
    letra = palabra[0].upper()
    long_palabra = len(palabra)

    mostrar_tablero(lista_letras, resultados, jugador_actual["aciertos"], 
                    jugador_actual["errores"], letra, long_palabra, definicion, jugadores, palabra)

    palabra_ingresada = cargar_palabra_valida()
    resultado = analizar_palabra_ingresada(palabra_ingresada, palabra)
    indice_resultado = lista_letras.index(letra.lower())
    resultados_jugador = resultados[jugador_actual["referencia"] - 1]
    if len(resultados_jugador) <= indice_resultado:
        resultados_jugador.extend([''] * (indice_resultado - len(resultados_jugador) + 1))
    resultados_jugador[indice_resultado] = resultado
    puntos = contar_puntos(resultado, jugador_actual)
    if resultado == ACIERTO:
        cambiar_turno(jugadores)
    return puntos, palabra_ingresada

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

def cargar_nombre_usuario():
    """
    La funcion se encarga de guardar el nombre del usuario en una variable
    """
    usuario = input("Ingrese el nombre del jugador: ")
    while(usuario == " "):
        print("ERROR! debe ingresar un nombre de jugador valido.")
        usuario = input("Ingrese el nombre del jugador: ")
    return usuario

def calcular_cantidad_jugadores(jugadores):
    """
    La funcion se encarga de devolver un numero de referencia del jugador.
    """
    if (len(jugadores) == 0):
        cantidad = 1
    else:
        cantidad = len(jugadores) + 1
    return cantidad

def datos_juego_usuario(jugador, jugadores):
    jugador["nombre"] = cargar_nombre_usuario()
    jugador["referencia"] = calcular_cantidad_jugadores(jugadores)
    jugador["aciertos"] = 0
    jugador["errores"] = 0
    return jugador

def consultar_cantidad_jugadores():
    cantidad_jugadores = input("Ingrese la cantidad de jugadores a jugar: ")
    while(not cantidad_jugadores.isnumeric()):
        print("ERROR! INGRESE SOLO NUMEROS!")
        cantidad_jugadores = input("Ingrese la cantidad de jugadores a jugar: ")
    return cantidad_jugadores

def jugar_rosco():
    diccionario_palabra_def= cargar_datos_para_rosco()
    jugar_pasapalabra = True
    #diccionario_rosco, lista_letras = generar_diccionario()
    jugadores = []
    cantidad_jugadores = consultar_cantidad_jugadores()

    i = 0
    while i < len(cantidad_jugadores):
        jugador = {}
        jugador = datos_juego_usuario(jugador, jugadores)
        jugadores.append(jugador)

    resultados = [["" for _ in range(len(diccionario_rosco))] for _ in range(len(jugadores))]

    print("\n--- Comienza el Juego ---")

    while jugar_pasapalabra:
        lista_letras = dato_rosco.cargar_letras()
        diccionario_rosco = dato_rosco.cargar_palabras_definiciones(diccionario_palabra_def, lista_letras)
        for palabra in diccionario_rosco.keys():
            definicion = diccionario_rosco[palabra]
            puntos, palabra_ingresada = jugar_turno(jugadores, lista_letras, resultados, palabra, definicion)
            if palabra_ingresada == "fin":
                print("Juego terminado.")
                mostrar_resumen_de_juego(diccionario_rosco, jugadores, resultados)

jugar_rosco()