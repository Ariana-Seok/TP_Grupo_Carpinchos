"""Importamos el diccionario que necesitamos"""
# ETAPA 1
#import diccionario_etapa1

dicc = {"casa": "lugar donde vives", "perro": "animal domestico", "gato": "animal domestico"}

def mostrar_tablero(aciertos, errores, posicion, lista, lista_2):
    """
    Esta funcion recibe 5 parametros (2 listas y 3 variables (int)) y muestra por pantalla el estado del juego.
    """
    print(f"""[{lista[0]}][{lista[1]}][{lista[2]}]\n[{lista_2[0]}][{lista_2[1]}][{lista_2[2]}]
{' ' * (posicion * 3 + 1)}^
Aciertos: {aciertos}
Errores: {errores}""")

def ingresar_palabra():
    """
    Es una funcion que no recibe parametros y devuelve la palabra ingresada por el usuario.
    """
    ingreso_usuario = input("Ingresa palabra: ").lower()
    while not ingreso_usuario.isalpha():
        print("Ingrese solo letras.")
        ingreso_usuario = input("Ingrese palabra: ").lower()
    return ingreso_usuario

def evaluar_palabra(palabra_ingresada, clave):
    """
    Esta funcion recibe 2 parametros (palabra ingresada por el usuario y la palabra correcta) y 
    devuelve "a" por acierto y "e" por error.
    """
    return "a" if palabra_ingresada == clave else "e"

def jugar_turno(aciertos, errores, posicion, lista, lista_2, clave, definicion):
    """
    Esta funcion recibe 6 parametros (cantidad de aciertos hasta el momento, cant errores hasta el momento, 
    posicion actual en el tablero, una lista con las letras a jugar,
    una 2da lista que contiene los aciertos y errores que se van cometiendo, 
    la palabra que el usuario debe adivinar, la definicion que se le da al usuario como pista).
    La función muestra el tablero, el turno actual y la longitud de la palabra a adivinar.
    Despues solicita al usuario que ingrese una palabra llamando a la funcion Ingresar_palabra()
    Despues verifica si la palabra es correcta o incorrecta llamando a la funcion 
    Evaluar_palabra(palabra_ingresada, clave).
    Dependiendo lo que devuelva la funcion Evaluar_palabra, se actualizara el tablero y los 
    contadores de aciertos y errores.
    La funcion retorna los nuevos valores de aciertos, errores y palabra_ingresada
    """
    letra = clave[0]
    longitud = len(clave)

    mostrar_tablero(aciertos, errores, posicion, lista, lista_2)
    print(f"Turno letra: {letra} Longitud palabra: {longitud}\nDefinicion: {definicion}")

    palabra_ingresada = ingresar_palabra()
    resultado = evaluar_palabra(palabra_ingresada, clave)
    lista_2[posicion] = resultado

    if resultado == "a":
        aciertos += 1
    else:
        errores += 1

    return aciertos, errores, palabra_ingresada

def mostrar_resumen(diccionario, lista_palabras_ingresadas, lista_2):
    """
    Esta funcion recibe 3 parametros (un diccionario, una lista de palabras ingresadas por el 
    usuario y una lista de aciertos y errores) y muestra por pantalla un resumen de la partida.
    """
    print("\n--- Resumen de la Partida ---")
    print("-" * 50)
    for i, clave in enumerate(diccionario.keys()):
        letra = clave[0]
        long = len(clave)
        correccion = clave
        palabra_jugador = lista_palabras_ingresadas[i]
        result = "acierto" if lista_2[i] == "a" else "error"
        if result == "error":
            print(f"Turno de la letra: {letra} - Palabra de {long} letras - {palabra_jugador} - {result} - Palabra correcta es : {correccion}")
        else:
            print(f"Turno de la letra: {letra} - Palabra de {long} letras - {palabra_jugador} - {result}")
    print("-" * 50)

def calcular_puntaje(aciertos):
    """
    En esta funcion multiplicamos la cantidad de aciertos por 10 y retornamos ese valor
    """
    return aciertos * 10
