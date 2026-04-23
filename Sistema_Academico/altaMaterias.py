# ---------------------  Área de declaración de librerías --------------------------------
import tkinter as tk
from tkinter import ttk, messagebox
from database import conectar

def info_materias():

    ventana = tk.Toplevel()
    ventana.title("Información de las Materias")
    ventana.geometry("900x500")

      # Configuración del grid de la ventana principal
    ventana.rowconfigure(0, weight=1)  # Parte superior
    ventana.rowconfigure(1, weight=2)  # Parte inferior
    ventana.columnconfigure(0, weight=1)


    # =========================
    # FRAME SUPERIOR (ENTRYS)
    # =========================
    frame_superior = ttk.LabelFrame(ventana, text="Datos de las Materias", padding=10)
    frame_superior.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)

    # Configurar columnas del frame superior
    frame_superior.columnconfigure(1, weight=1)
    frame_superior.columnconfigure(3, weight=1)

    # -------------------------- Variables ----------------------------------------------------------------------------
    nombre = tk.StringVar()
    descripcion = tk.StringVar()
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------  Labels y Entrys distribuidos en dos columnas  ------------------------------------
    # Labels y entry que permite ingregar elnombre de la materia
    ttk.Label(frame_superior, text="Nombre completo de la Materia :").grid(row=0, column=0, sticky="e", padx=5, pady=5)
    ttk.Entry(frame_superior, textvariable=nombre).grid(row=0, column=1, sticky="ew", padx=5, pady=5)

    # Labels y entry para describir la materia
    ttk.Label(frame_superior, text="Descripción (Educ.Secundaria/Pol. Adultos):").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    ttk.Entry(frame_superior, textvariable=descripcion).grid(row=1, column=1, sticky="ew", padx=5, pady=5)
 
    # =========================
    # BOTONES
    # =========================
    frame_botones = ttk.Frame(frame_superior)
    frame_botones.grid(row=3, column=0, columnspan=4, pady=10)


    # --------------------------- Botones que permiten agregar, modificar etc. ---------------------------
    ttk.Button(frame_botones, text="Agregar", command=agregar_datos).grid(row=0, column=0, padx=5)
    ttk.Button(frame_botones, text="Modificar", command=modificar_registro).grid(row=0, column=1, padx=5)
    ttk.Button(frame_botones, text="Eliminar", command=eliminar_registro).grid(row=0, column=2, padx=5)
    ttk.Button(frame_botones, text="Limpiar", command=limpiar_campos).grid(row=0, column=3, padx=5)
    ttk.Button(frame_botones, text="Cerrar", command=ventana.destroy).grid(row=0, column=4, padx=5)
    # ----------------------------------------------------------------------------------------------------