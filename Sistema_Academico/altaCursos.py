# ---------------------  Área de declaración de librerías --------------------------------
import tkinter as tk
from tkinter import ttk, messagebox
from database import conectar
from centraVent import centrar_ventana

def info_cursos():

    ventana = tk.Toplevel()
    ventana.title("Información de los Cursos")
    ventana.geometry("1100x700")

    # Configuración del grid de la ventana principal
    ventana.rowconfigure(0, weight=1)  # Parte superior
    ventana.rowconfigure(1, weight=2)  # Parte inferior
    ventana.columnconfigure(0, weight=1)


    # =========================
    # FRAME SUPERIOR (ENTRYS)
    # =========================
    frame_superior = ttk.LabelFrame(ventana, text="Ingreso de Cursos Secundaria y Polimodal", padding=10)
    frame_superior.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)

    # Configurar columnas del frame superior
    frame_superior.columnconfigure(1, weight=1)
    frame_superior.columnconfigure(3, weight=1)

    # -------------------------- Variables ----------------------------------------------------------------------------
    nombre = tk.StringVar()
    hentrada =tk.StringVar()
    hsalida = tk.StringVar()
    dia = tk.StringVar()
    turno = tk.StringVar()
    srprofesor = tk.StringVar()

    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------  Labels y Entrys distribuidos en dos columnas  ------------------------------------
    # Labels y entry que permite ingregar elnombre de la materia
    ttk.Label(frame_superior, text="Nbre del Curso :").grid(row=0, column=0, sticky="e", padx=5, pady=5)
    ttk.Entry(frame_superior, textvariable=nombre).grid(row=0, column=1, sticky="ew", padx=5, pady=5)

    # Labels y entry para ingresar la hora de entrada
    ttk.Label(frame_superior, text="Hor.de Entrada:").grid(row=0, column=2, sticky="e", padx=5, pady=5)
    ttk.Entry(frame_superior, textvariable=hentrada).grid(row=0, column=3, sticky="ew", padx=5, pady=5)

  # Labels y entry para ingresar la hora de entrada
    ttk.Label(frame_superior, text="Hor.de Salida:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    ttk.Entry(frame_superior, textvariable=hsalida).grid(row=1, column=1, sticky="ew", padx=5, pady=5)

    # Labels y entry para ingresar el turno del curso 
    ttk.Label(frame_superior, text="Día de la semana:").grid(row=1, column=2, sticky="e", padx=5, pady=5)
    ttk.Entry(frame_superior, textvariable=dia).grid(row=1, column=3, sticky="ew", padx=5, pady=5)

    # Labels y entry para ingresar el turno del curso 
    ttk.Label(frame_superior, text="Turno del Curso:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
    ttk.Entry(frame_superior, textvariable=turno).grid(row=2, column=1, sticky="ew", padx=5, pady=5)

    # Labels y entry para ingresar la Situación Revista del Docente
    ttk.Label(frame_superior, text="S.R.del Profesor:").grid(row=2, column=2, sticky="e", padx=5, pady=5)
    ttk.Entry(frame_superior, textvariable=srprofesor).grid(row=2, column=3, sticky="ew", padx=5, pady=5)
 
    # =========================
    # BOTONES
    # =========================
    frame_botones = ttk.Frame(frame_superior)
    frame_botones.grid(row=3, column=0, columnspan=4, pady=10)

    # =========================
    # FRAME INFERIOR (TREEVIEW)
    # =========================
    frame_inferior = ttk.LabelFrame(ventana, text="Listado de Cursos", padding=10)
    frame_inferior.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

    # Configuración del grid del frame inferior
    frame_inferior.rowconfigure(0, weight=1)
    frame_inferior.columnconfigure(0, weight=1)

    #Columnas del Treeview
    columnas = ("id_curso","nombre", "hentrada", "hsalida", "dia", "turno", "srprofesor")

    tree = ttk.Treeview(frame_inferior, columns=columnas, show="headings")
    tree.grid(row=0, column=0, sticky="nsew")

    # Encabezados
    tree.heading("id_curso", text="ID")
    tree.heading("nombre", text="Nbre del Curso")
    tree.heading("hentrada", text="Hora de Entrada")
    tree.heading("hsalida", text="Hora de Salida")
    tree.heading("dia", text="Día de la Semana")
    tree.heading("turno", text="Turno del Curso")
    tree.heading("srprofesor", text="S.R.del Profesor")

    
    tree.column("id_curso", width=0, stretch=False)
    tree.column("nombre", width=200, anchor="center")
    tree.column("hentrada", width=200, anchor="center")
    tree.column("hsalida", width=200, anchor="center")
    tree.column("dia", width=200, anchor="center")
    tree.column("turno", width=100, anchor="center")
    tree.column("srprofesor", width=200, anchor="center")
 

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
    
    # Variable global ha usar en las distintas funciones 
    id_seleccionado = None

      # ----------------- Carga y muestra los registros cargados en la BD Materias -------------
    def cargar_datos_treeview():
        for item in tree.get_children():
            tree.delete(item)

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id_curso, nombre, hentrada, hsalida, dia, turno, srprofesor
            FROM cursos
            ORDER BY nombre
        """)

        for fila in cursor.fetchall():
            tree.insert("", "end", values=fila)

        conn.close()
    # ---------------------------------------------------------------------------------------

    # ------------------------ Añade registros nuevos a la BD materias ----------------------
    def agregar_cursos():
        if not nombre.get() or not hentrada.get() or not hsalida.get() or not turno.get():
            messagebox.showwarning(
                "Campos obligatorios",
                "Nombres del curso, horario de entrada y horario de salida son obligatorios."
            )
            return
        
        try:
            conn = conectar()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO cursos (nombre, hentrada, hsalida, dia, turno, srprofesor)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                nombre.get(),
                hentrada.get(),
                hsalida.get(),
                dia.get(),
                turno.get(),
                srprofesor.get(),
            ))

            conn.commit()
            conn.close()

            messagebox.showinfo("Éxito", "Curso guardado correctamente.")

            cargar_datos_treeview()
           

        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron guardar los Cursos:\n{e}")
    # ----------------------------------------------------------------------------------

     # -------------- Limpia los Entrys de datos ingresados y/o seleccionados ------------------------------
    def limpiar_campos():
        nonlocal id_seleccionado
        nombre.set("")
        hentrada.set("")
        hsalida.set("")
        turno.set("")
        srprofesor.set("")

    #-----------------------------------------------------------------------------------------------------


    # --------------------------- Botones que permiten agregar, modificar etc. ---------------------------
    ttk.Button(frame_botones, text="Agregar", command=agregar_cursos).grid(row=0, column=0, padx=5)
    ttk.Button(frame_botones, text="Modificar", command="modificar_cursos").grid(row=0, column=1, padx=5)
    ttk.Button(frame_botones, text="Eliminar", command="eliminar_cursos").grid(row=0, column=2, padx=5)
    ttk.Button(frame_botones, text="Limpiar", command=limpiar_campos).grid(row=0, column=3, padx=5)
    ttk.Button(frame_botones, text="Cerrar", command=ventana.destroy).grid(row=0, column=4, padx=5)
    # ----------------------------------------------------------------------------------------------------

    centrar_ventana(ventana)  #centra pantalla Cursos