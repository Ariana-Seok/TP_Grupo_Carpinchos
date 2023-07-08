# Etapa 7 - Registracion de los Jugadores con Interfaz Grafica

import tkinter as tk
from tkinter import messagebox
import csv
import random

USUARIOS_CSV = "usuarios.csv"
num_inicios_sesion = 0
usuarios_iniciaron_sesion = []

def leer_archivo(archivo):
    """
    Esta función lee una línea del archivo CSV y devuelve un registro como lista.
    """
    linea = archivo.readline()
    if linea:
        registro = linea.rstrip().split(",")
    else:
        registro = []
    return registro

def validar_usuario(usuario, registro_actual=None):
    """
    El objetivo de esta función es verificar si un usuario ya está registrado en el archivo CSV de usuarios.
    """
    """
    >>> validar_usuario("usuario1")
    False
    >>> validar_usuario("usuario2", registro_actual=["usuario2", "contraseña"])
    True
    """
    result = False
    encontrado = False

    with open("archivosCSV\\usuarios.csv", "r") as archivo:
        registro = leer_archivo(archivo)
        while registro and not encontrado:
            if registro and registro[0] == usuario and registro != registro_actual:
                result = True
                encontrado = True
            registro = leer_archivo(archivo)

    return result

def comprobar_nombre_usuario(usuario, mensajes_error, errores):
    i = 0
    contrasenia_valida = True
    simbolo_valido = "-"
    cant_num = 0
    cant_letras = 0
    cant_simbolo = 0

    while(i < len(usuario)) and contrasenia_valida:
        if(usuario[i].isalpha()):
            cant_letras += 1
        elif(usuario[i].isnumeric()):
            cant_num += 1
        elif(usuario[i] == simbolo_valido):
            cant_simbolo += 1
        elif not (usuario[i].isalnum()) or (usuario[i] != simbolo_valido):
            contrasenia_valida = False
        i += 1

    if not(cant_num > 0) or not (cant_letras > 0) or not (cant_simbolo > 0) or not (contrasenia_valida):
        errores.append(mensajes_error["usuario_invalido"])
    return errores

def usuario_valido(mensajes_error, usuario, errores):
    MAX_LONG = 20
    MIN_LONG = 4
    if (len(usuario) < MIN_LONG) or (len(usuario) > MAX_LONG):
        errores.append(mensajes_error["usuario_longitud"])
    else:
        errores = comprobar_nombre_usuario(usuario, mensajes_error, errores)
    return errores

def comprobar_contrasenia_valida(mensajes_error, contrasenia, errores):
    if not any(caracter.isdigit() for caracter in contrasenia):
        errores.append(mensajes_error["contrasena_digitos"])
    elif not any(caracter.islower() for caracter in contrasenia):
        errores.append(mensajes_error["contrasena_minusculas"])
    elif not any(caracter.isupper() for caracter in contrasenia):
        errores.append(mensajes_error["contrasena_mayusculas"])
    elif not any(caracter in "#!" for caracter in contrasenia):
        errores.append(mensajes_error["contrasena_caracteres_especiales"])
    elif any(caracter in "áéíóúÁÉÍÓÚ" for caracter in contrasenia):
        errores.append(mensajes_error["contrasena_acentos"])
    return errores

def contrasenia_valida(mensajes_error, contrasenia, errores):
    MAX_LONG_CONTRASENIA = 12
    MIN_LONG_CONTRASENIA = 6
    if(len(contrasenia) < MIN_LONG_CONTRASENIA) or (len(contrasenia) > MAX_LONG_CONTRASENIA):
        errores.append(mensajes_error["contrasena_longitud"])
    else:
        errores = comprobar_contrasenia_valida(mensajes_error, contrasenia, errores)
    return errores

def verificar_ingreso_contrasenia(confirmar_contrasena, contrasena, mensajes_error, errores):
    if (contrasena != confirmar_contrasena):  
        errores.append(mensajes_error["contrasena_coincidencia"])
    return errores

def verificar_usuario_existente(usuario, contrasena, mensajes_error, ventana_registrar, errores):
    if validar_usuario(usuario):
        errores.append(mensajes_error["usuario_existente"])
    elif errores:
        messagebox.showerror("Error", "\n".join(errores))
    else:
        with open("archivosCSV\\usuarios.csv", "a", newline="") as archivo:
            writer = csv.writer(archivo)
            writer.writerow([usuario, contrasena])
        messagebox.showinfo("Éxito", "Usuario registrado exitosamente.")
        ventana_registrar.destroy()


def registrar_usuario(usuario_entry, contrasenia_entry, confirmacion_contrasenia_entry, ventana_registrar):
    """
    Guarda el nombre de usuario y la contraseña en el archivo CSV si cumplen con los requisitos pedidos.
    Muestra mensajes de error si hay problemas con los datos ingresados.
    """
    usuario = usuario_entry.get()
    contrasena = contrasenia_entry.get()
    confirmar_contrasena = confirmacion_contrasenia_entry.get()
    mensajes_error = {
            "usuario_longitud": "El usuario debe tener entre 4 y 20 caracteres.",
            "usuario_invalido": "El nombre de usuario no cumple con los requisitos, \nTiene que esta formado por:\n- Letras\n- numeros\n- guion medio",
            "contrasena_longitud": "La contraseña debe tener entre 6 y 12 caracteres.",
            "contrasena_digitos": "La contraseña debe contener al menos un dígito.",
            "contrasena_minusculas": "La contraseña debe contener al menos una letra minúscula.",
            "contrasena_mayusculas": "La contraseña debe contener al menos una letra mayúscula.",
            "contrasena_caracteres_especiales": "La contraseña debe contener al menos uno de los caracteres especiales '#!'.",
            "contrasena_acentos": "La contraseña no puede contener letras acentuadas.",
            "contrasena_coincidencia": "Las contraseñas no coinciden.",
            "usuario_existente": "El usuario ya está registrado."
    }
    
    errores = []

    errores = usuario_valido(mensajes_error, usuario, errores)
    errores = contrasenia_valida(mensajes_error, contrasena, errores)
    errores = verificar_ingreso_contrasenia(confirmar_contrasena, contrasena, mensajes_error, errores)
    verificar_usuario_existente(usuario, contrasena, mensajes_error, ventana_registrar, errores)
    

def guardar_usuario():
    #Acá creamos la ventana para registrar usuarios
    ventana_registrar = tk.Toplevel()
    ventana_registrar.title("Registro de Usuario")
    ventana_registrar.geometry("300x200")
    ventana_registrar.resizable(False, False)
    ventana_registrar.configure(bg="#777777")
    separador = tk.Frame(ventana_registrar, height=5, bg="#777777")
    separador.pack(fill=tk.X, pady=5)
    usuario_label = tk.Label(ventana_registrar, text="Nombre de Usuario:", bg="#777777", fg="white")
    usuario_label.pack()
    usuario_entry = tk.Entry(ventana_registrar)
    usuario_entry.pack()
    contrasenia_label = tk.Label(ventana_registrar, text="Contraseña:", bg="#777777", fg="white")
    contrasenia_label.pack()
    contrasenia_entry = tk.Entry(ventana_registrar, show="*")
    contrasenia_entry.pack()
    confirmacion_contrasenia_label = tk.Label(ventana_registrar, text="Confirmar Contraseña:", bg="#777777", fg="white")
    confirmacion_contrasenia_label.pack()
    confirmacion_contrasenia_entry = tk.Entry(ventana_registrar, show="*")
    confirmacion_contrasenia_entry.pack()
    separador = tk.Frame(ventana_registrar, height=5, bg="#777777")
    separador.pack(fill=tk.X, pady=5)
    registrar_button = tk.Button(ventana_registrar, text="Registrar", command= lambda : registrar_usuario(usuario_entry, contrasenia_entry, confirmacion_contrasenia_entry, ventana_registrar))
    registrar_button.pack()
    ventana_registrar.mainloop()
    
def cerrar_ventana():
    """
    Funcion que es llamada cuando se pulsa el boton de iniciar partida, cierra la ventana de inicio de sesion.
    """
    root.destroy()

def asignar_turnos():
    """
    Obtiene una lista de los usuarios que iniciaron sesion y seleccionados de manera aleatoria con el ramdom.suffle y los asigna a los turnos de juego.
    """
    global usuarios_iniciaron_sesion
    usuarios = usuarios_iniciaron_sesion

    random.shuffle(usuarios)
    turno_jugadores = []

    mensaje_turnos = "Orden de turnos:\n"
    for i, usuario in enumerate(usuarios):
        mensaje_turnos += f"Turno {i+1}: {usuario}\n"
        turno_jugadores.append(usuario)

    messagebox.showinfo("Asignación de Turnos", mensaje_turnos)

    return turno_jugadores

def iniciar_sesion():
    """
    Esta función se llama cuando se hace clic en el botón "Iniciar Sesión". Abre una ventana donde el usuario 
    puede ingresar su nombre de usuario y contraseña. Luego, se verifica si coinciden con los datos registrados.
    Si la validación es exitosa, se muestra un mensaje de éxito y se permite el inicio de sesión. Se cuenta 
    el número de inicios de sesión exitosos y cuando se alcanza el límite de 4, se muestra la ventana de turnos.
    """
    usuario = usuario_entry.get()
    contrasena = contrasenia_entry.get()
    global usuarios_iniciaron_sesion

    usuario_encontrado = False
    usuario_en_partida = False

    with open("archivosCSV\\usuarios.csv", "r") as archivo:
        registros = csv.reader(archivo)
        for registro in registros:
            if (registro) and (registro[0] == usuario) and (registro[1] == contrasena):
                usuario_encontrado = True
                if (usuario in usuarios_iniciaron_sesion):
                    usuario_en_partida = True

    if usuario_encontrado:
        if usuario_en_partida:
            messagebox.showerror("Error", "Este jugador ya se registró en la partida.")
        else:
            usuarios_iniciaron_sesion.append(usuario)
            messagebox.showinfo("Éxito", "Inicio de sesión exitoso.")
            usuario_entry.delete(0, tk.END)
            contrasenia_entry.delete(0, tk.END)
            if len(usuarios_iniciaron_sesion) == 4:
                root.destroy()
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

    if len(usuarios_iniciaron_sesion) == 4:
        root.destroy()

# Configuración de la ventana de inicio de sesion
root = tk.Tk()
root.title("Inicio de Sesión")
root.geometry("300x200")
root.resizable(False, False)

#Icono de root
icono = tk.PhotoImage(file="img/pasapalabra.PNG")
root.iconphoto(True, icono)

# Crear el canvas y establecer la imagen de fondo
canvas = tk.Canvas(root, width=300, height=200)
canvas.pack()

imagen_fondo = tk.PhotoImage(file="img\carpincho.PNG")
canvas.create_image(0, 0, anchor=tk.NW, image=imagen_fondo)

# Labels y Entrys para el inicio de sesión
usuario_label = tk.Label(root, text="Nombre de Usuario:")
usuario_label.place(x=20, y=20)

usuario_entry = tk.Entry(root)
usuario_entry.place(x=140, y=20)

contrasenia_label = tk.Label(root, text="Contraseña:")
contrasenia_label.place(x=40, y=50)

contrasenia_entry = tk.Entry(root, show="*")
contrasenia_entry.place(x=140, y=50)

# Botones para el inicio de sesión y registro
iniciar_sesion_button = tk.Button(root, text="Iniciar Sesión", command=iniciar_sesion, padx=8, pady=5, cursor="hand2")
iniciar_sesion_button.place(x=99, y=80)

registrar_button = tk.Button(root, text="Registrarse", command=guardar_usuario, cursor="hand2")
registrar_button.place(x=112, y=120)

iniciar_partida_button = tk.Button(root, text="Iniciar partida", command=cerrar_ventana, padx=8, pady=5, cursor="hand2")
iniciar_partida_button.place(x=99, y=154)

root.mainloop()

#import doctest
#doctest.testmod()