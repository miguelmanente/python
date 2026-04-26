# -----------------  LIBRERÍAS ------------------------------------------------------------
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk 
from centraVent import centrar_ventana, cventana
from database import validar_usuario, registrar_usuario
from app import pPrincipal

# Variable Global
usuario_logueado = None  # Variable global

# ------------------------------  Login para validar usuario al sistema -----------------------
def ventana_login(root, barramenu):

    global usuario_logueado
    
    login = tk.Toplevel(root)
 
    login.title("Iniciar Sesión")
    login.geometry("400x300")
   
    tk.Label(login, text="Usuario").pack(pady=5)
    entry_usuario = tk.Entry(login)
    entry_usuario.pack()

    tk.Label(login, text="Contraseña").pack(pady=5)
    entry_password = tk.Entry(login, show="*")
    entry_password.pack()

    def iniciar_sesion():
        global usuario_logueado, login_correcto

        usuario = entry_usuario.get()
        password = entry_password.get()

        resultado = validar_usuario(usuario, password)

        if resultado:
            usuario_logueado = usuario
            messagebox.showinfo("Bienvenido", f"Se ha logueado al sistema {usuario}", parent=login)
          # 🔥 habilitar menú
            root.config(menu=barramenu)
            for i in range(barramenu.index("end") + 1):
                barramenu.entryconfig(i, state="normal")
            
            login.destroy()
            root.deiconify()
        else:
            messagebox.showerror("Error", "Usuario incorrecto", parent=login)
# ---------------------------------------------------------------------------------------------------------

# ------------------------------------- Abre la ventana para registrar usuario ------------------------
    def abrir_registro():
        ventana_registro()
# ------------------------------------------------------------------------------------------------------

# ---------------------------------- Salir de la Aplicación -----------------------------------------------    
    def salir():
         root.destroy()  # 🔥 cerrar toda la app
# ---------------------------------------------------------------------------------------------------------
# ----------------------------------- Botones para Loguearse y registrarse --------------------------------
    tk.Button(login, text="Ingresar", command=iniciar_sesion).pack(pady=10)
    tk.Button(login, text="Salir", command=salir).pack(pady=10)
    tk.Label(login, text="Si no se resgistro, pulse el botón Registrarse ...").pack(pady=5)
    tk.Button(login, text="Registrarse", command=abrir_registro).pack(pady=10)

    cventana(login)
#------------------------------------------------------------------------------------------

#--------------------- Registros en la tabla ususarios la loguearse -----------------------
def ventana_registro():
    registro = tk.Toplevel()
    registro.title("Registro de Usuario")
    registro.geometry("400x300")
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
# --------------------------------------------------------------------------------------------------
    
    #-------------------------------  Salir de la aplicación -------------------------------------
    def salir():
        if messagebox.askyesno("Salir", "¿Desea salir de registración?"):
            registro.destroy()
    #----------------------------------------------------------------------------------------------
    
    #botenes de la vnetana de logueo
    tk.Button(registro, text="Registrarse", command=registrar).pack(pady=10)
    tk.Button(registro, text="Salir", command=salir).pack(pady=10)
#-----------------------------------------------------------------------------------


    #Llama a la función que está en el módulo centraVent
    cventana(registro)


#-------------------------------  Salir de la aplicación -------------------------------------
  
def salir():
    if messagebox.askyesno("Salir", "¿Desea cerrar la aplicación?"):
        root.destroy()
#----------------------------------------------------------------------------------------------


#------------------------------------------- TKINTER -----------------------------------------
#-------------------------------------- VENTANA PRINCIPAL -------------------------------------
#Ventana principal 
root = tk.Tk()
root.grab_set()
root.focus_force()
root.lift()
root.attributes('-topmost', True)
root.after(100, lambda: root.attributes('-topmost', False))
root.title("SISTEMA ACADÉMICO")
root.geometry("1100x700")

root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=0)
root.columnconfigure(0, weight=1)

#-------------------------------------- BARRA DE NENÚ -----------------------------------------

#Barra de menúes
barramenu = tk.Menu(root)
root.config(menu=barramenu)

#Menú Archivo
mArchivo = tk.Menu(barramenu, tearoff=0)
barramenu.add_cascade(label="Login - Registración", menu=mArchivo)
# mArchivo.add_command(label="Registrarse", command="ventana_registro")
mArchivo.add_command(label="", command=ventana_login(root, barramenu))
mArchivo.add_separator()
mArchivo.add_command(label="Salir", command=salir)

mSistGestion = tk.Menu(barramenu, tearoff=0)
barramenu.add_cascade(label="Sistema de Gestion", menu=mSistGestion)
mSistGestion.add_command(label="Gestión Educativa", command=pPrincipal)

root.config(menu=barramenu)
#barramenu.entryconfig("Sistema de Gestion", state="disabled")
for i in range(barramenu.index("end") + 1):
    barramenu.entryconfig(i, state="disabled")



#---------------------------------- LOGO PAGINA PRINCIPAL -------------------------------------
# Crear un Frame para centrar el contenido
logoP = tk.Frame(root)
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

centrar_ventana(root)

root.mainloop()