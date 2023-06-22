import tkinter as tk
from tkinter import messagebox
import csv
import random

USUARIOS_CSV = "usuarios.csv"
MAX = "ZZZZ"
MAX_USUARIOS = 4 

def validar_usuario(usuario, registro_actual=None):
    """
    El objetivo de esta función es verificar si un usuario ya está registrado en el archivo CSV de usuarios.
    """
    result = False
    encontrado = False

    with open(USUARIOS_CSV, "r") as archivo:
        registro = leer_archivo(archivo)
        while registro and registro != MAX and not encontrado:
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


def contar_usuarios():
    """
    Cuenta el número de usuarios registrados en el archivo CSV, retorna un valor entero.
    """
    with open(USUARIOS_CSV, "r") as archivo:
        num_usuarios = sum(1 for linea in archivo if linea.strip())
    return num_usuarios

def guardar_usuario():
    """
    Esta función se llama cuando se hace clic en el botón "Registrarse". Verifica si se ha alcanzado el número máximo 
    de usuarios permitidos antes de continuar. Si se ha alcanzado el límite, muestra un mensaje de error. 
    De lo contrario, crea una nueva ventana de registro donde el usuario puede ingresar su nombre de usuario, 
    contraseña y confirmar la contraseña. Después de hacer clic en el botón "Registrar", se validan los datos ingresados 
    y se guardan en el archivo CSV si son válidos.
    """
    num_usuarios_actual = contar_usuarios()

    if num_usuarios_actual >= MAX_USUARIOS:
        messagebox.showerror("Error", f"Se ha alcanzado el límite máximo de usuarios ({MAX_USUARIOS}). No se permite registrar más usuarios.")
        return

    def guardar_usuario_interno():
        """
        Guarda el nombre de usuario y la contraseña en el archivo CSV si cumplen con los requisitos pedidos.
        Muestra mensajes de error si hay problemas con los datos ingresados.
        """
        usuario = usuario_entry.get()
        contrasena = contrasenia_entry.get()
        confirmar_contrasena = confirmacion_contrasenia_entry.get()

        mensaje_error = None

        # Verificar el nombre de usuario
        if len(usuario) < 4 or len(usuario) > 20 or not usuario.isalnum() or "-" in usuario:
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

        # Verificar si el usuario ya está registrado
        elif validar_usuario(usuario):
            mensaje_error = "El usuario ya está registrado."

        if mensaje_error:
            messagebox.showerror("Error", mensaje_error)
        else:
            with open(USUARIOS_CSV, "a", newline="") as archivo:
                writer = csv.writer(archivo)
                writer.writerow([usuario, contrasena])
            messagebox.showinfo("Éxito", "Usuario registrado exitosamente.")
            registrar_window.destroy()

    # En esta parte creamos la ventana de registro de usuario
    registrar_window = tk.Toplevel()
    registrar_window.title("Registro de Usuario")
    registrar_window.geometry("300x200")

    usuario_label = tk.Label(registrar_window, text="Nombre de Usuario:")
    usuario_label.pack()
    usuario_entry = tk.Entry(registrar_window)
    usuario_entry.pack()

    contrasenia_label = tk.Label(registrar_window, text="Contraseña:")
    contrasenia_label.pack()
    contrasenia_entry = tk.Entry(registrar_window, show="*")
    contrasenia_entry.pack()

    confirmacion_contrasenia_label = tk.Label(registrar_window, text="Confirmar Contraseña:")
    confirmacion_contrasenia_label.pack()
    confirmacion_contrasenia_entry = tk.Entry(registrar_window, show="*")
    confirmacion_contrasenia_entry.pack()

    registrar_button = tk.Button(registrar_window, text="Registrar", command=guardar_usuario_interno)
    registrar_button.pack()

def asignar_turnos():
    """
    Esta función se llama cuando se hace clic en el botón "Iniciar partida". 
    Lee los nombres de usuario registrados en el archivo CSV y los mezcla aleatoriamente 
    utilizando la función random.shuffle(). Luego muestra una ventana emergente con el orden de turnos generads.
    """
    usuarios = []
    with open(USUARIOS_CSV, "r") as archivo:
        registro = leer_archivo(archivo)
        while registro and registro != MAX:
            if registro:
                usuarios.append(registro[0])
            registro = leer_archivo(archivo)

    random.shuffle(usuarios)

    mensaje_turnos = "Orden de turnos:\n"
    for i, usuario in enumerate(usuarios):
        mensaje_turnos += f"Turno {i+1}: {usuario}\n"

    messagebox.showinfo("Asignación de Turnos", mensaje_turnos)

def iniciar_sesion():
    """
    Esta función verifica si el usuario ingresado existe en el archivo CSV y si la contraseña coincide.
    Muestra un mensaje de éxito si el inicio de sesión es exitoso, de lo contrario, muestra un mensaje de error.
    """
    usuario = usuario_entry.get()
    contrasena = contrasenia_entry.get()

    result = False

    if not usuario or not contrasena:
        messagebox.showerror("Error", "Por favor, ingresa el nombre de usuario y la contraseña.")
        result = False
    else:
        with open(USUARIOS_CSV, "r") as archivo:
            registro = leer_archivo(archivo)
            while registro and registro != MAX:
                if len(registro) >= 2 and registro[0] == usuario and registro[1] == contrasena:
                    messagebox.showinfo("Éxito", "Inicio de sesión exitoso.")
                    result = True
                registro = leer_archivo(archivo)

        if not result:
            messagebox.showerror("Error", "Usuario no registrado o contraseña incorrecta.")

    if result:
        # Limpiar los entrys después de un inicio de sesión exitoso
        usuario_entry.delete(0, tk.END)
        contrasenia_entry.delete(0, tk.END)

    return result

# Configuración de la ventana de inicio de sesion
root = tk.Tk()
root.title("Inicio de Sesión")
root.geometry("300x200")
root.resizable(False, False)

# Cargar las imágenes
imagen_izquierda = tk.PhotoImage(file="carpincho.png")
imagen_derecha = tk.PhotoImage(file="pasapalabra.png")

# Redimensionar las imágenes
imagen_izquierda = imagen_izquierda.subsample(6)
imagen_derecha = imagen_derecha.subsample(9)

# Labels para las imágenes
label_imagen_izquierda = tk.Label(root, image=imagen_izquierda)
label_imagen_izquierda.pack(side=tk.LEFT)

label_imagen_derecha = tk.Label(root, image=imagen_derecha)
label_imagen_derecha.pack(side=tk.RIGHT)

# Labels y Entrys para el inicio de sesion
usuario_label = tk.Label(root, text="Nombre de Usuario:")
usuario_label.pack()
usuario_entry = tk.Entry(root)
usuario_entry.pack()

contrasenia_label = tk.Label(root, text="Contraseña:")
contrasenia_label.pack()
contrasenia_entry = tk.Entry(root, show="*")
contrasenia_entry.pack()

# Botones para el inicio de sesion y registro
iniciar_sesion_button = tk.Button(root, text="Iniciar Sesión", command=iniciar_sesion, padx=8, pady=5, cursor="hand2")
iniciar_sesion_button.pack(pady=8)

registrar_button = tk.Button(root, text="Registrarse", command=guardar_usuario,cursor="hand2")
registrar_button.pack()

asignar_turnos_button = tk.Button(root, text="Iniciar partida", command=asignar_turnos, padx=8, pady=5, cursor="hand2")
asignar_turnos_button.pack(pady=8)

root.mainloop()