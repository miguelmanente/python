import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk  # Necesitas instalar Pillow para el logo pag ppal
from database import crear_tablas
from registrar import ventana_registro
from loguear import ventana_login
from centraVent import centrar_ventana
from datos_personales import info_profesor
from altaMaterias import info_materias
from altaCursos import info_cursos


#Código - Zona de funciones
#Crea la tablas de la BD si no están creadas


def pPrincipal():
    crear_tablas()
    #-------------------------------  Salir de la aplicación -------------------------------------  
    def salir():
        if messagebox.askyesno("Salir", "¿Desea cerrar Sistema de Gestión Educativo?"):
            ventana.destroy()
    #----------------------------------------------------------------------------------------------
    #------ TKINTER -------------------------------------------------------------------------------
    #-------------------------------------- VENTANA PRINCIPAL -------------------------------------
    #Ventana principal 
    ventana = tk.Toplevel()
    ventana.title("SISTEMA ACADÉMICO")
    ventana.geometry("1100x700")

    ventana.rowconfigure(0, weight=1)
    ventana.rowconfigure(1, weight=0)
    ventana.columnconfigure(0, weight=1)

    #-------------------------------------- BARRA DE NENÚ -----------------------------------------

    #Barra de menúes
    barramenu = tk.Menu(ventana)
    ventana.config(menu=barramenu)

    #Menú Archivo
    mArchivo = tk.Menu(barramenu, tearoff=0)
    barramenu.add_cascade(label="Archivo", menu=mArchivo)
    mArchivo.add_command(label="Salir", command=salir)

    #Menú Profesor
    mProfesor =tk.Menu(barramenu, tearoff=0)
    barramenu.add_cascade(label="Profesor", menu=mProfesor)
    mProfesor.add_command(label="Datos Personales", command=info_profesor)

    #Menú Materias
    mMaterias = tk.Menu(barramenu, tearoff=0)
    barramenu.add_cascade(label="Materias", menu=mMaterias)
    mMaterias.add_command(label="Agregar Materias", command=info_materias)

    #Menú Cursos
    mCursos = tk.Menu(barramenu, tearoff=0)
    barramenu.add_cascade(label="Cursos", menu=mCursos)
    mCursos.add_command(label="Agregar Cursos", command=info_cursos)

    #---------------------------------- LOGO PAGINA PRINCIPAL -------------------------------------
    # Crear un Frame para centrar el contenido
    logoP = tk.Frame(ventana)
    logoP.pack(expand=True)  # Centra el contenido en la ventana

    # Cargar el logo
    try:
        logo = Image.open("logo1.png")  # Asegúrate de que el archivo esté en la misma carpeta
        logo = logo.resize((800, 400))
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
    # label_text = tk.Label(
    #     logoP,
    #     text="Sistema Educativo - Gestión Escolar",
    #     font=("Arial", 20, "bold")
    # )
    # label_text.pack(pady=(0,10))
    #-------------------------------------------------------------------------------------------

    # Footer con logo y texto

    img = Image.open("logotipo.png")
    img = img.resize((100, 100))  # tamaño exacto que quieras
    logo = ImageTk.PhotoImage(img)
    # logo = tk.PhotoImage(file="logotipo.png")
    # logo = logo.subsample(10, 10)

    # Frame footer (usar PACK porque la ventana usa pack)
    frame_footer = tk.Frame(ventana)
    frame_footer.pack(side="bottom", anchor="w", padx=10, pady=5)

    lbl_logo = tk.Label(frame_footer, image=logo)
    lbl_logo.pack(anchor="w")

    lbl_texto = tk.Label(
        frame_footer,
        text="© 2026 Miguel Manente",
        font=("Arial", 12),
        fg="gray"
    )
    lbl_texto.pack(anchor="w")

    lbl_logo.image = logo
    #--------------------------------------------------------------------------------------------

    centrar_ventana(ventana)

    ventana.mainloop()


