MAX = "ZZZZ"
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



def main():
    configuracion = open("configuracion.csv", "r+")
    configuraciones = cargar_configuraciones(configuracion)
    configuracion.close()
    
main()