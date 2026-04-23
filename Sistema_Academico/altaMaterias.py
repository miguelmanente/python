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
    frame_superior = ttk.LabelFrame(ventana, text="Ingreso de Materias Secundaria y Polimodal", padding=10)
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

    # =========================
    # FRAME INFERIOR (TREEVIEW)
    # =========================
    frame_inferior = ttk.LabelFrame(ventana, text="Listado de Materias", padding=10)
    frame_inferior.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

    # Configuración del grid del frame inferior
    frame_inferior.rowconfigure(0, weight=1)
    frame_inferior.columnconfigure(0, weight=1)

    #Columnas del Treeview
    columnas = ("id_materia","nombre", "descripcion")

    tree = ttk.Treeview(frame_inferior, columns=columnas, show="headings")
    tree.grid(row=0, column=0, sticky="nsew")

    # Encabezados
    tree.heading("id_materia", text="ID")
    tree.heading("nombre", text="Nombres de la Materia")
    tree.heading("descripcion", text="Descripción de Nivel de la materia")

    
    tree.column("id_materia", width=0, stretch=False)
    tree.column("nombre", width=200, anchor="w")
    tree.column("descripcion", width=100, anchor="center")
 

    # Scrollbars
    scrollbar_y = ttk.Scrollbar(frame_inferior, orient="vertical", command=tree.yview)
    scrollbar_x = ttk.Scrollbar(frame_inferior, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

    # Ubicación en el grid
    tree.grid(row=0, column=0, sticky="nsew")
    scrollbar_y.grid(row=0, column=1, sticky="ns")
    scrollbar_x.grid(row=1, column=0, sticky="ew")


   
    #========================================================================================
    #                                  MÉTODOS O FUNCIONES
    #========================================================================================
    
    #Variable global ha usar en las distintas funciones 
    id_seleccionado = None

    # ----------------- Carga y muestra los registros cargados en la BD Materias -------------
    def cargar_datos_treeview():
        for item in tree.get_children():
            tree.delete(item)

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id_materia, nombre, descripcion
            FROM materias
            ORDER BY nombre
        """)

        for fila in cursor.fetchall():
            tree.insert("", "end", values=fila)

        conn.close()
    # ---------------------------------------------------------------------------------------

    # ------------------------ Añade registros nuevos a la BD materias ----------------------
    def agregar_materias():
        if not nombre.get() or not descripcion.get():
            messagebox.showwarning(
                "Campos obligatorios",
                "Nombres de la Materia y Descripción son obligatorios."
            )
            return
        
        try:
            conn = conectar()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO materias (nombre, descripcion)
                VALUES (?, ?)
            """, (
                nombre.get(),
                descripcion.get(),
            ))

            conn.commit()
            conn.close()

            messagebox.showinfo("Éxito", "Materia guardada correctamente.")

            cargar_datos_treeview()
           

        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron guardar los datos:\n{e}")
    # ----------------------------------------------------------------------------------

    # -------------- Limpia los Entrys de datos ingresados y/o seleccionados ------------------------------
    def limpiar_campos():
        nonlocal id_seleccionado
        nombre.set("")
        descripcion.set("")
    #-----------------------------------------------------------------------------------------------------

    # ----------------------  Muestra toda la información cargada en la BD -------------------------------
    cargar_datos_treeview()
    # ----------------------------------------------------------------------------------------------------
    # --------------------------- Botones que permiten agregar, modificar etc. ---------------------------
    ttk.Button(frame_botones, text="Agregar", command=agregar_materias).grid(row=0, column=0, padx=5)
    ttk.Button(frame_botones, text="Modificar", command="").grid(row=0, column=1, padx=5)
    ttk.Button(frame_botones, text="Eliminar", command="").grid(row=0, column=2, padx=5)
    ttk.Button(frame_botones, text="Limpiar", command=limpiar_campos).grid(row=0, column=3, padx=5)
    ttk.Button(frame_botones, text="Cerrar", command=ventana.destroy).grid(row=0, column=4, padx=5)
    # ----------------------------------------------------------------------------------------------------