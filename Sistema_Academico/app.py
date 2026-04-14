import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk  # Necesitas instalar Pillow
from database import crear_tablas
from registrar import ventana_registro
from loguear import ventana_login
from centraVent import centrar_ventana



#Código - Zona de funciones

crear_tablas()


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



centrar_ventana(ventana)
ventana.mainloop()