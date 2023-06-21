import tkinter as tk
from tkinter import messagebox
import csv

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
            if registro[0] == usuario and registro != registro_actual:
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
        num_usuarios = sum(1 for _ in archivo)
    return num_usuarios

def registrar_usuario():
    global usuario_entry, contrasenia_entry, confirmacion_contrasenia_entry

    num_usuarios_actual = contar_usuarios()

    if num_usuarios_actual >= MAX_USUARIOS:
        messagebox.showerror("Error", f"Se ha alcanzado el límite máximo de usuarios ({MAX_USUARIOS}). No se permite registrar más usuarios.")
        return
    """
    Esta función muestra una ventana de registro de usuario, permite al usuario ingresar un nombre de usuario y contraseña,
    y los guarda en el archivo CSV si cumplen con los requisitos de longitud y caracteres.
    """
    def guardar_usuario():
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
            with open(USUARIOS_CSV, "a") as archivo:
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

    registrar_button = tk.Button(registrar_window, text="Registrar", command=guardar_usuario)
    registrar_button.pack()

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
        # Limpiar los entrys después de un inicio de sesion exitoso
        usuario_entry.delete(0, tk.END)
        contrasenia_entry.delete(0, tk.END)

    return result

# Configuración de la ventana de inicio de sesion
root = tk.Tk()
root.title("Inicio de Sesión")
root.geometry("300x200")
root.resizable(False, False)

usuario_label = tk.Label(root, text="Nombre de Usuario:")
usuario_label.pack()
usuario_entry = tk.Entry(root)
usuario_entry.pack()

contrasenia_label = tk.Label(root, text="Contraseña:")
contrasenia_label.pack()
contrasenia_entry = tk.Entry(root, show="*")
contrasenia_entry.pack()

login_button = tk.Button(root, text="Iniciar Sesión", command=iniciar_sesion)
login_button.pack()

registrar_button = tk.Button(root, text="Registrarse", command=registrar_usuario)
registrar_button.pack()


root.mainloop()