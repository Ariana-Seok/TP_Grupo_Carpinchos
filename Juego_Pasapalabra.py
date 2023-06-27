# ETAPA 10 - Archivo de Configuraciones

from PasapalabraParte2 import jugar 
MAX = "fin,0"

def leer_archivo(archivo):
    """
    La funcion se encarga de leer una linea del archivo.
    PRE: El archivo debe estar abierto correctamente
    POST: Devuelve una linea del archivo
    """
    linea = archivo.readline()
    if (linea):
        registro = linea.rstrip("\n").split(",")
    else:
        registro = MAX
    return registro

def cargar_configuraciones(archivo):
    """
    La funcion recibe un archivo abierto correctamente, y se encarga
    de almacenar los datos del archivo en un diccionario.
    """
    configuraciones = {}
    configuracion = leer_archivo(archivo)
    while(configuracion != MAX):
        variable = configuracion[0]
        valor = configuracion[1]
        configuraciones[variable] = valor
        configuracion = leer_archivo(archivo)
    return configuraciones

def mostrar_configuraciones(configuraciones):
    """
    La funcion se encarga de mostrar por pantalla lo que hay en el diccionario 
    recibido por parametro.
    """
    for config, valor in configuraciones:
        print(f"{config}: {valor}")

def mostrar_menu():
    print(f"""
\nQue desea realizar ?\n
0. Ver configuracion actual
1. Modificar longitud palabra minima
2. Modificar cantidad letra rosco
3. Modificar maxima partidas
4. Modificar puntaje aciertos
5. Modificar puntaje desaciertos
6. Volver a la configuracion predeterminada
7. Volver\n
    """)

def si_no_es_numero(opcion):
    """
    La funcion se encarga de verificar que el dato recibido sea de tipo int,
    en caso contrario solicitara el dato hasta que sea valido.
    PRE: La funcion debe recibir por parametro la variable "opcion" ya cargada
    POST: La funcion devuelve la variable "opcion" con un valor valido de tipo int
    """
    while not (opcion.isdigit()):
        opcion = input("Ingrese solo NUMEROS: ")
    return int(opcion)

def si_no_es_valido(opcion, max_long, min_long):
    """
    Esta funcion se encarga solicitar al usuario un numero valido
    entre los valores que tengan los parametros max_long y min_log, los cuales 
    deben ser de tipo int
    PRE: La funcion debe recibir por parametro la variable "opcion" ya cargada, y 
    dos variables de tipo int
    POST: La funcion devuelve la variable "opcion" con un valor valido de tipo int
    """
    while(opcion < min_long) or (opcion > max_long):
        opcion = input(f"Ingrese NUMEROS entre ({min_long} - {max_long}): ")
        opcion = si_no_es_numero(opcion)
    return int(opcion)

def cargar_opcion(min_long, max_long):
    """
    Esta funcion se encarga de cargar el valor para la variable "opcion".
    """
    opcion = input(f"Ingrese un numero ({min_long} - {max_long}): ")
    opcion = si_no_es_numero(opcion)
    opcion = si_no_es_valido(opcion, max_long, min_long)
    return opcion

def modificar_long_palabra(configuraciones):
    """
    La funcion se encarga de modificar el valor de dicha clave
    correspondiente al diccionario recibido por parametros.
    PRE: La funcion debe recibir un diccionario inicializado
    POST: La funcion debe modificar el valor de la clave 
    "LONGITUD_PALABRA_MINIMA"
    """
    longitud_deseada = input("Ingrese la longitud de la palabra mínima: ")
    longitud_deseada = si_no_es_numero(longitud_deseada)
    configuraciones["LONGITUD_PALABRA_MINIMA"] = longitud_deseada
    print(f"Se modifico la LONGITUD PALABRA MINIMA a: {longitud_deseada}")

def modificar_cant_letras_rosco(configuraciones):
    """
    La funcion se encarga de modificar el valor de dicha clave
    correspondiente al diccionario recibido por parametros.
    PRE: La funcion debe recibir un diccionario inicializado
    POST: La funcion debe modificar el valor de la clave 
    "CANTIDAD_LETRAS_ROSCO"
    """
    min_num = 1
    max_num = 27
    cant_letras_deseadas = input("Ingrese la cantidad de letras para el rosco: ")
    cant_letras_deseadas = si_no_es_numero(cant_letras_deseadas)
    cant_letras_deseadas = si_no_es_valido(cant_letras_deseadas, max_num, min_num)
    configuraciones["CANTIDAD_LETRAS_ROSCO"] = cant_letras_deseadas
    print(f"Se modifico la CANTIDAD DE LETRAS ROSCO a: {cant_letras_deseadas}")

def modificar_maxima_partidas(configuraciones):
    """
    La funcion se encarga de modificar el valor de dicha clave
    correspondiente al diccionario recibido por parametros.
    PRE: La funcion debe recibir un diccionario inicializado
    POST: La funcion debe modificar el valor de la clave 
    "MAXIMO_PARTIDAS"
    """
    cant_partidas_deseadas = input("Ingrese la cantidad de maxima partidas: ")
    cant_partidas_deseadas = si_no_es_numero(cant_partidas_deseadas)
    configuraciones["MAXIMO_PARTIDAS"] = cant_partidas_deseadas
    print(f"Se modifico la CANTIDAD DE MAXIMA PARTIDAS a: {cant_partidas_deseadas}")

def modificar_puntaje_acierto(configuraciones):
    """
    La funcion se encarga de modificar el valor de dicha clave
    correspondiente al diccionario recibido por parametros.
    PRE: La funcion debe recibir un diccionario inicializado
    POST: La funcion debe modificar el valor de la clave 
    "PUNTAJE_ACIERTO"
    """
    puntaje_acierto_deseado = input("Ingrese el puntaje acierto: ")
    puntaje_acierto_deseado = si_no_es_numero(puntaje_acierto_deseado)
    configuraciones["PUNTAJE_ACIERTO"] = puntaje_acierto_deseado
    print(f"Se modifico el PUNTAJE ACIERTO a: {puntaje_acierto_deseado}")

def modificar_puntaje_desacierto(configuraciones):
    """
    La funcion se encarga de modificar el valor de dicha clave
    correspondiente al diccionario recibido por parametros.
    PRE: La funcion debe recibir un diccionario inicializado
    POST: La funcion debe modificar el valor de la clave 
    "PUNTAJE_DESACIERTO"
    """
    puntaje_desacierto_deseado = input("Ingrese el puntaje desacierto: ")
    puntaje_desacierto_deseado = si_no_es_numero(puntaje_desacierto_deseado)
    configuraciones["PUNTAJE_DESACIERTO"] = puntaje_desacierto_deseado
    print(f"Se modifico el PUNTAJE DESACIERTO a: {puntaje_desacierto_deseado}")

def conservar_valores_def(configuraciones, config_por_defecto):
    """
    La funcion se encarga de cargar al diccionario, los valores
    que fueron definidos por defecto, los cuales estan almacenados 
    en un diccionario.
    PRE: Recibe dos parametros de tipo dicc
    POST: La carga al diccionario "configuraciones"
    """
    for configuracion in config_por_defecto:
        if not configuracion in configuraciones:
            configuraciones[configuracion] = config_por_defecto[configuracion]

def mostrar_configuracion_actual(configuraciones):
    """
    La funcion se encarga de mostrar por pantalla las
    configuraciones 
    """
    print("\n--------- Configuracion Actual ------------\n")
    for configuracion in configuraciones:
        print(f"{configuracion} = {configuraciones[configuracion]}")

def cargar_configuracion_archivo(configuraciones):
    """
    La funcion se encarga de escribir en el archivo
    recibido por parametro.
    PRE: La funcion recibe un parametro el cual es un diccionario inicializado
    POST: La funcion se encarga de escribir todo el contenido que contenga el diccionario.
    """
    with open("archivosCSV\configuracion.csv", "w") as archivo:
        for configuracion in configuraciones:
            archivo.write(configuracion + "," + str(configuraciones[configuracion]) + "\n")

def menu_principal():
    print(f"""
-- Bienvenido al menu principal del Pasapalabra --\n
0. Iniciar Partida
1. Configuraciones
    """)

def modificar_configuraciones(configuraciones, config_por_defecto):
    """
    La funcion se encarga de mostrar por pantalla el menu de configuraciones,
    y segun el dato ingresado se realizara dicha accion.
    PRE: La funcion recibe dos parametros de tipo dicc
    POST: La funcion carga las configuraciones realizadas en el archivo csv
    """
    print("\n--------- Bienvenido a la configuracion del PASAPALABRA --------")
    modificar_config = True
    min_long = 0
    max_long = 7
    while modificar_config:
        mostrar_menu()
        opcion = cargar_opcion(min_long, max_long)
        if (opcion == 0):
            mostrar_configuracion_actual(configuraciones)
        elif (opcion == 1):
            modificar_long_palabra(configuraciones)
        elif (opcion == 2):
            modificar_cant_letras_rosco(configuraciones)
        elif (opcion == 3):
            modificar_maxima_partidas(configuraciones)
        elif (opcion == 4):
            modificar_puntaje_acierto(configuraciones)
        elif (opcion == 5):
            modificar_puntaje_desacierto(configuraciones)
        elif (opcion == 6):
            conservar_valores_def(configuraciones, config_por_defecto)
        elif (opcion == 7):
            modificar_config = False
    cargar_configuracion_archivo(configuraciones)
    jugar(configuraciones)
    return configuraciones

def mostrar_menu_principal(configuraciones, config_por_defecto):
    """
    PRE: La funcion recibe dos parametros de tipo dicc.
    POST: La funcion se encarga de ejecutar cierta funcion dependiendo
    de lo que se haya cargado en "opcion"
    """
    menu_principal()
    min_long = 0
    max_long = 1
    opcion = cargar_opcion(min_long, max_long)
    if (opcion == 0):
        jugar(configuraciones)
    elif (opcion == 1):
        configuraciones = modificar_configuraciones(configuraciones, config_por_defecto)

def main():
    """
    Función principal del programa
    
    >>> main()
    -- Bienvenido al menu principal del Pasapalabra --

    0. Iniciar Partida
    1. Configuraciones
    """
    config_por_defecto = {
        "LONGITUD_PALABRA_MINIMA": 4,
        "CANTIDAD_LETRAS_ROSCO":10,
        "MAXIMO_PARTIDAS":5,
        "PUNTAJE_ACIERTO": 10,
        "PUNTAJE_DESACIERTO": 3
        }
    with open("archivosCSV\configuracion.csv", "r+") as configuracion:    
        configuraciones = cargar_configuraciones(configuracion)
        mostrar_menu_principal(configuraciones, config_por_defecto)
    
main()

import doctest
doctest.testmod()