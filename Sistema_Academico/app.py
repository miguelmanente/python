import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk  # Necesitas instalar Pillow para el logo pag ppal
import os
from database import crear_tablas
from centraVent import centrar_ventana
from datos_personales import info_profesor
from altaMaterias import info_materias
from altaCursos import info_cursos
from altaHorarios import info_horarios
from altaAsignaciones import info_asignaciones
from listados import ventana_listado
import sesion



#Código - Zona de funciones
#Crea la tablas de la BD si no están creadas


def pPrincipal():
    crear_tablas()

    #-------------------------------  Salir de la aplicación -------------------------------------  
    def salir():
        if messagebox.askyesno("Salir", "¿Desea cerrar Sistema de Gestión Educativo?", parent=ventana):
            ventana.destroy()
    #----------------------------------------------------------------------------------------------
    #------ TKINTER -------------------------------------------------------------------------------
    #-------------------------------------- VENTANA PRINCIPAL -------------------------------------
    #Ventana principal 
    ventana = tk.Toplevel()
    ventana.tk.call('tk', 'scaling', 1.0)  # (opcional)
    ventana.title("SISTEMA ACADÉMICO")
    ventana.geometry("1100x700")

    ventana.rowconfigure(0, weight=1)
    ventana.rowconfigure(1, weight=0)
    ventana.columnconfigure(0, weight=1)

        # ---------------- TOP BAR ----------------
    frame_top = tk.Frame(ventana, bg="#2c3e50", height=30)
    frame_top.pack(fill="x")

    lbl_usuario = tk.Label(
        frame_top,
        text=f"Usuario: {sesion.usuario_actual}",
        bg="#2c3e50",
        fg="white",
        font=("Arial", 10, "bold")
    )
    lbl_usuario.pack(side="right", padx=10)
    

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

    #Menú Horarios
    mHorarios = tk.Menu(barramenu, tearoff=0)
    barramenu.add_cascade(label="Horarios", menu=mHorarios)
    mHorarios.add_command(label="Creación de Horarios", command=info_horarios)

    #Menú Asignacopnes de Profesores
    mAsignaciones = tk.Menu(barramenu, tearoff=0)
    barramenu.add_cascade(label="Asignaciones", menu=mAsignaciones)
    mAsignaciones.add_command(label="Asignaciones Profesores", command=info_asignaciones)

    #Menú Listados de profesores
    mListados = tk.Menu(barramenu, tearoff=0)
    barramenu.add_cascade(label="Listados", menu=mListados)
    mListados.add_command(label="Profesores Titulares", command=lambda: ventana_listado("Titular"))
    mListados.add_command(label="Profesores Provisorio", command=lambda: ventana_listado("Provisorio"))
    mListados.add_command(label="Profesores Suplentes",command=lambda: ventana_listado("Suplente"))


  # ---------------------------------- LOGO PRINCIPAL -------------------------------------
    logoP = tk.Frame(ventana)
    logoP.pack(expand=True)

    try:
        # img = Image.open("logo1.png")
        ruta = os.path.dirname(__file__)
        img = Image.open(os.path.join(ruta, "logos.png"))
        img = img.resize((900, 400))
        # logo_tk = ImageTk.PhotoImage(img)
        logo_tk = ImageTk.PhotoImage(img, master=ventana)

        label_logo = tk.Label(logoP, image=logo_tk)
        label_logo.image =logo_tk  # 🔥 importante
        label_logo.pack(pady=(2, 2))

    except Exception as e:
        print(f"No se pudo cargar el logo: {e}")
        tk.Label(logoP, text="[Logo no disponible]").pack()
        label_logo.pack(pady=(2,2))

    # Texto
    # label_text = tk.Label(
    #     logoP,
    #     text="",
    #     font=("Arial", 2, "bold")
    # )
    # label_text.pack(pady=(0, 10))
    # ---------------------------------------------------------------------------------------

    # ---------------------------------- FOOTER -------------------------------------
    frame_footer = tk.Frame(ventana)
    frame_footer.pack(side="bottom", anchor="w", padx=10, pady=5)

    try:
        # img_footer = Image.open("logotipo.png")
        img_footer = Image.open(os.path.join(ruta, "logo2.png"))
        img_footer = img_footer.resize((140, 100))
      
        logo_footer = ImageTk.PhotoImage(img_footer, master=ventana)

        lbl_logo = tk.Label(frame_footer, image=logo_footer)
        lbl_logo.image = logo_footer  # 🔥 importante
        lbl_logo.pack(anchor="w")

    except Exception as e:
        print(f"No se pudo cargar footer: {e}")
        tk.Label(frame_footer, text="[Sin logo]").pack()

    lbl_texto = tk.Label(
        frame_footer,
        text="© 2026 Programas MAM",
        font=("Arial", 12),
        fg="gray"
    )
    lbl_texto.pack(anchor="w")
    #-------------------------------------------------------------------------------------------
    centrar_ventana(ventana)



