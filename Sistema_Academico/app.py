import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk  # Necesitas instalar Pillow
from database import crear_tablas
from database import registrar_usuario
from database import validar_usuario


#Código - Zona de funciones
# def verificar_login():
#     global usuario_logueado
#     if usuario_logueado is None:
#         messagebox.showwarning(
#             "Acceso restringido",
#             "Debe iniciar sesión primero"
#         )
#         return False
#     return True

# Crear las tablas al iniciar la aplicación
crear_tablas()

#--------------------- Registros en la tabla ususarios la loguearse ----------------
def ventana_registro():
    registro = tk.Toplevel()
    registro.title("Registro de Usuario")
    registro.geometry("300x200")
    registro.grab_set()

    tk.Label(registro, text="Usuario").pack(pady=5)
    entry_usuario = tk.Entry(registro)
    entry_usuario.pack()

    tk.Label(registro, text="Contraseña").pack(pady=5)
    entry_password = tk.Entry(registro, show="*")
    entry_password.pack()

    def registrar():
        usuario = entry_usuario.get()
        password = entry_password.get()

        if not usuario or not password:
            messagebox.showwarning("Advertencia", "Complete todos los campos")
            return

        if registrar_usuario(usuario, password):
            messagebox.showinfo("Éxito", "Usuario registrado correctamente")
            registro.destroy()
        else:
            messagebox.showerror("Error", "El usuario ya existe")

    tk.Button(registro, text="Registrarse", command=registrar).pack(pady=10)
#-----------------------------------------------------------------------------------

#----------------------------- Ventana para que el usuario se loguee ----------------------

usuario_logueado = None  # Variable global

def ventana_login():
    global usuario_logueado

    login = tk.Toplevel()
    login.title("Iniciar Sesión")
    login.geometry("300x200")
    login.grab_set()

    tk.Label(login, text="Usuario").pack(pady=5)
    entry_usuario = tk.Entry(login)
    entry_usuario.pack()

    tk.Label(login, text="Contraseña").pack(pady=5)
    entry_password = tk.Entry(login, show="*")
    entry_password.pack()

    def iniciar_sesion():
        global usuario_logueado
        usuario = entry_usuario.get()
        password = entry_password.get()

        resultado = validar_usuario(usuario, password)

        if resultado:
            usuario_logueado = usuario
            messagebox.showinfo("Bienvenido", f"Hola {usuario}")
            login.destroy()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    tk.Button(login, text="Ingresar", command=iniciar_sesion).pack(pady=10)
#--------------------------------------------------------------------------------------------

#-------------------------------  Salir de la aplicación -------------------------------------
def salir():
    if messagebox.askyesno("Salir", "¿Desea cerrar la aplicación?"):
        ventana.destroy()
#----------------------------------------------------------------------------------------------

#------ TKINTER --------
#-------------------------------------- VENTANA PRINCIPAL -------------------------------------
#Ventana principal 
ventana = tk.Tk()
ventana.title("SISTEMA ACADÉMICO")
ventana.geometry("1100x700")

#-------------------------------------- BARRA DE NENÚ -----------------------------------------

#Barra de menúes
barramenu = tk.Menu(ventana)
ventana.config(menu=barramenu)

#Menú Archivo opción Salir
mArchivo = tk.Menu(barramenu, tearoff=0)
barramenu.add_cascade(label="Archivo", menu=mArchivo)
mArchivo.add_command(label="Registrarse", command=ventana_registro)
mArchivo.add_command(label="Loguearse", command=ventana_login)
mArchivo.add_separator()
mArchivo.add_command(label="Salir", command=salir)

#---------------------------------- LOGO PAGINA PRINCIPAL -------------------------------------
# Crear un Frame para centrar el contenido
logoP = tk.Frame(ventana)
logoP.pack(expand=True)  # Centra el contenido en la ventana

# Cargar el logo
try:
    logo = Image.open("logo.png")  # Asegúrate de que el archivo esté en la misma carpeta
    logo = logo.resize((600, 500))
    logo_tk = ImageTk.PhotoImage(logo)

    # Mostrar el logo
    label_logo = tk.Label(logoP, image=logo_tk)
    label_logo.image = logo_tk  # Mantener referencia para evitar que se elimine
    label_logo.pack(pady=(10,5))

except Exception as e:
    print(f"No se pudo cargar el logo: {e}")
    label_logo = tk.Label(logoP, text="[Logo no disponible]")
    label_logo.pack(pady=(10,5))

# Texto debajo del logo
label_text = tk.Label(
    logoP,
    text="Sistema Educativo - Gestión Escolar",
    font=("Arial", 20, "bold")
)
label_text.pack(pady=(0,10))
#-------------------------------------------------------------------------------------------



ventana.mainloop()