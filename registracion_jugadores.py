# Etapa 7 - Registracion de los Jugadores con Interfaz Grafica

import tkinter as tk
from tkinter import messagebox
import csv
import random

USUARIOS_CSV = "usuarios.csv"
num_inicios_sesion = 0
usuarios_iniciaron_sesion = []

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


def guardar_usuario():
    """
    Esta función se llama cuando se hace clic en el botón "Registrarse". Verifica si se ha alcanzado el número máximo 
    de usuarios permitidos antes de continuar. Si se ha alcanzado el límite, muestra un mensaje de error. 
    De lo contrario, crea una nueva ventana de registro donde el usuario puede ingresar su nombre de usuario, 
    contraseña y confirmar la contraseña. Después de hacer clic en el botón "Registrar", se validan los datos ingresados 
    y se guardan en el archivo CSV si son válidos.
    """

    def registrar_usuario():
        """
        Guarda el nombre de usuario y la contraseña en el archivo CSV si cumplen con los requisitos pedidos.
        Muestra mensajes de error si hay problemas con los datos ingresados.
        """
        usuario = usuario_entry.get()
        contrasena = contrasenia_entry.get()
        confirmar_contrasena = confirmacion_contrasenia_entry.get()

        mensaje_error = None

        # Verificar el nombre de usuario
        if len(usuario) < 4 or len(usuario) > 20 or not all(caracter.isalnum() or caracter == "-" for caracter in usuario):
            mensaje_error = "El nombre de usuario no cumple con los requisitos."

        # Verificar la contraseña
        elif len(contrasena) < 6 or len(contrasena) > 12:
            mensaje_error = "La contraseña debe tener entre 6 y 12 caracteres."
        elif not any(caracter.isdigit() for caracter in contrasena):
            mensaje_error = "La contraseña debe contener al menos un dígito."
        elif not any(caracter.islower() for caracter in contrasena):
            mensaje_error = "La contraseña debe contener al menos una letra minúscula."
        elif not any(caracter.isupper() for caracter in contrasena):
            mensaje_error = "La contraseña debe contener al menos una letra mayúscula."
        elif not any(caracter in "#!" for caracter in contrasena):
            mensaje_error = "La contraseña debe contener al menos uno de los caracteres especiales '#!'."
        elif any(caracter in "áéíóúÁÉÍÓÚ" for caracter in contrasena):
            mensaje_error = "La contraseña no puede contener letras acentuadas."
        if contrasena != confirmar_contrasena:  
            mensaje_error = "Las contraseñas no coinciden."

        # Verificar si el usuario ya está registrado
        elif validar_usuario(usuario):
            mensaje_error = "El usuario ya está registrado."

        if mensaje_error:
            messagebox.showerror("Error", mensaje_error)
        else:
            with open("archivosCSV\\usuarios.csv", "a", newline="") as archivo:
                writer = csv.writer(archivo)
                writer.writerow([usuario, contrasena])
            messagebox.showinfo("Éxito", "Usuario registrado exitosamente.")
            ventana_registrar.destroy()

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
    registrar_button = tk.Button(ventana_registrar, text="Registrar", command=registrar_usuario)
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

    with open("archivosCSV\\usuarios.csv", "r") as archivo:
        registros = csv.reader(archivo)
        for registro in registros:
            if registro and registro[0] == usuario and registro[1] == contrasena:
                usuario_encontrado = True
                usuarios_iniciaron_sesion.append(registro[0])

    if usuario_encontrado:
        messagebox.showinfo("Éxito", "Inicio de sesión exitoso.")
        usuario_entry.delete(0, tk.END)
        contrasenia_entry.delete(0, tk.END)
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
icono = tk.PhotoImage(file="img\pasapalabra.PNG")
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


import doctest
doctest.testmod()