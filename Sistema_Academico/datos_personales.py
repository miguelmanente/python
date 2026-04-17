# ---------------------  Área de declaración de librerías --------------------------------
import tkinter as tk
from tkinter import ttk, messagebox
import re
from database import conectar

# ----------- Función que maneja toda la ventana datos personales del profesor ------------
def info_profesor():

    ventana = tk.Toplevel()
    ventana.title("Datos personales del profesor")
    ventana.geometry("900x500")

    # Configuración del grid de la ventana principal
    ventana.rowconfigure(0, weight=1)  # Parte superior
    ventana.rowconfigure(1, weight=2)  # Parte inferior
    ventana.columnconfigure(0, weight=1)

    # =========================
    # FRAME SUPERIOR (ENTRYS)
    # =========================
    frame_superior = ttk.LabelFrame(ventana, text="Datos del Profesor", padding=10)
    frame_superior.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    # Configurar columnas del frame superior
    frame_superior.columnconfigure(1, weight=1)
    frame_superior.columnconfigure(3, weight=1)

    # Variables
    apellido_nombre = tk.StringVar()
    dni = tk.StringVar()
    telefono = tk.StringVar()
    email = tk.StringVar()
    situacion_revista = tk.StringVar()
    fecha_toma = tk.StringVar()

    # Labels y Entrys distribuidos en dos columnas
    ttk.Label(frame_superior, text="Apellido y Nombres:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
    ttk.Entry(frame_superior, textvariable=apellido_nombre).grid(row=0, column=1, sticky="ew", padx=5, pady=5)
 
    #Verificación e ingreso de número en DNI
    ttk.Label(frame_superior, text="DNI:").grid(row=0, column=2, sticky="e", padx=5, pady=5)
    #ttk.Entry(frame_superior, textvariable=dni).grid(row=0, column=3, sticky="ew", padx=5, pady=5)
    def solo_numeros(P):
        return P.isdigit() or P == ""
    vcmd = (ventana.register(solo_numeros), '%P')
    
    ttk.Entry(frame_superior, textvariable=dni, validate="key", validatecommand=vcmd).grid(row=0, column=3, sticky="ew", padx=5, pady=5)

    ttk.Label(frame_superior, text="Teléfono:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    ttk.Entry(frame_superior, textvariable=telefono).grid(row=1, column=1, sticky="ew", padx=5, pady=5)

    ttk.Label(frame_superior, text="Email:").grid(row=1, column=2, sticky="e", padx=5, pady=5)
    ttk.Entry(frame_superior, textvariable=email).grid(row=1, column=3, sticky="ew", padx=5, pady=5)

    ttk.Label(frame_superior, text="Situación de Revista:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
    ttk.Entry(frame_superior, textvariable=situacion_revista).grid(row=2, column=1, sticky="ew", padx=5, pady=5)

    ttk.Label(frame_superior, text="Fecha Toma de Posesión:").grid(row=2, column=2, sticky="e", padx=5, pady=5)
    ttk.Entry(frame_superior, textvariable=fecha_toma).grid(row=2, column=3, sticky="ew", padx=5, pady=5)

    # =========================
    # BOTONES
    # =========================
    frame_botones = ttk.Frame(frame_superior)
    frame_botones.grid(row=3, column=0, columnspan=4, pady=10)

    # =========================
    # FRAME INFERIOR (TREEVIEW)
    # =========================
    frame_inferior = ttk.LabelFrame(ventana, text="Listado de Profesores", padding=10)
    frame_inferior.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

    # Configuración del grid del frame inferior
    frame_inferior.rowconfigure(0, weight=1)
    frame_inferior.columnconfigure(0, weight=1)

    #Columnas del Treeview
    columnas = ("id_profesor","apenom", "dni", "telefono", "email", "sitrev", "fechatp")

    tree = ttk.Treeview(frame_inferior, columns=columnas, show="headings")
    tree.grid(row=0, column=0, sticky="nsew")

    # Encabezados
    tree.heading("id_profesor", text="ID")
    tree.heading("apenom", text="Apellido y Nombres")
    tree.heading("dni", text="DNI")
    tree.heading("telefono", text="Teléfono")
    tree.heading("email", text="Email")
    tree.heading("sitrev", text="Situación de Revista")
    tree.heading("fechatp", text="Fecha Toma de Posesión")
    
    tree.column("id_profesor", width=0, stretch=False)
    tree.column("apenom", width=200, anchor="w")
    tree.column("dni", width=100, anchor="center")
    tree.column("telefono", width=120, anchor="center")
    tree.column("email", width=180, anchor="w")
    tree.column("sitrev", width=150, anchor="center")
    tree.column("fechatp", width=140, anchor="center")

    # Scrollbars
    scrollbar_y = ttk.Scrollbar(frame_inferior, orient="vertical", command=tree.yview)
    scrollbar_x = ttk.Scrollbar(frame_inferior, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

    # Ubicación en el grid
    tree.grid(row=0, column=0, sticky="nsew")
    scrollbar_y.grid(row=0, column=1, sticky="ns")
    scrollbar_x.grid(row=1, column=0, sticky="ew")

   
    # ================================================================================
    #    FUNCIONES Agregar, modificar, eliminar. limpiar campos y salir de la ventana 
    # ================================================================================
  
    #--------------- Validación de dni ---------------------------------------------
    def validar_dni(dni):
        return dni.isdigit() and len(dni) in (7, 8)
    #-------------------------------------------------------------------------------
    
    # ----------------------- Validación de correo electrónico ------------------------
    def validar_email(email):
        patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(patron, email) is not None
    # --------------------------------------------------------------------------------

    
    # ---  Función que permite selecccionar un registro en el treview ------------------
    id_seleccionado = None

    def seleccionar_registro(event):
        nonlocal id_seleccionado

        item = tree.selection()
        if not item:
            return

        valores = tree.item(item[0], "values")

        id_seleccionado = valores[0]  # 👈 ESTE ES EL CLAVE

        apellido_nombre.set(valores[1])
        dni.set(valores[2])
        telefono.set(valores[3])
        email.set(valores[4])
        situacion_revista.set(valores[5])
        fecha_toma.set(valores[6])

    tree.bind("<<TreeviewSelect>>", seleccionar_registro) 
    # ---------------------------------------------------------------------------------

    # ----------------- Carga y muestra los registros carado en la BD -----------------
    def cargar_datos_treeview():
        for item in tree.get_children():
            tree.delete(item)

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id_profesor, apenom, dni, telefono, email, sitrev, fechatp
            FROM profesores
            ORDER BY apenom
        """)

        for fila in cursor.fetchall():
            tree.insert("", "end", values=fila)

        conn.close()
    # ----------------------------------------------------------------------------------

    # ------------------------ Añade registros nuevos a la BD profesores ---------------
    def agregar_datos():
        if not apellido_nombre.get() or not dni.get():
            messagebox.showwarning(
                "Campos obligatorios",
                "Apellido y Nombres y DNI son obligatorios."
            )
            return

        # ✅ VALIDAR DNI
        if not validar_dni(dni.get()):
            messagebox.showerror("Error", "DNI inválido (solo números, 7 u 8 dígitos)")
            return

        # ✅ VALIDAR EMAIL (solo si hay algo cargado)
        if email.get() and not validar_email(email.get()):
            messagebox.showerror("Error", "Email inválido")
            return

        try:
            conn = conectar()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO profesores (apenom, dni, telefono, email, sitrev, fechatp)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                apellido_nombre.get(),
                dni.get(),
                telefono.get(),
                email.get(),
                situacion_revista.get(),
                fecha_toma.get()
            ))

            conn.commit()
            conn.close()

            messagebox.showinfo("Éxito", "Datos guardados correctamente.")

            cargar_datos_treeview()
           

        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron guardar los datos:\n{e}")
    # ----------------------------------------------------------------------------------
      
    # ----------------  Modifica registro de profesores --------------------------------
    def modificar_registro():
        if not id_seleccionado:
            messagebox.showwarning("Atención", "Seleccione un registro")
            return

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE profesores
            SET apenom = ?, dni = ?, telefono = ?, email = ?, sitrev = ?, fechatp = ?
            WHERE id_profesor = ?
        """, (
            apellido_nombre.get(),
            dni.get(),
            telefono.get(),
            email.get(),
            situacion_revista.get(),
            fecha_toma.get(),
            id_seleccionado
        ))

        conn.commit()
        conn.close()

        cargar_datos_treeview()
        limpiar_campos()
        messagebox.showinfo("Éxito", "Registro actualizado")
    # -------------------------------------------------------------------------------------

    # ----------------  Elimina registros de profesores ----------------------------------
    def eliminar_registro():
        if not id_seleccionado:
            messagebox.showwarning("Atención", "Seleccione un registro")
            return

        confirmar = messagebox.askyesno("Confirmar", "¿Eliminar registro?")
        if not confirmar:
            return

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM profesores WHERE id_profesor = ?", (id_seleccionado,))

        conn.commit()
        conn.close()

        cargar_datos_treeview()
        limpiar_campos()
    #---------------------------------------------------------------------------------------

    # -------------- Limpia los Entrys de datos ingresados y/o seleccionados ----------------
    def limpiar_campos():
        nonlocal id_seleccionado
        apellido_nombre.set("")
        dni.set("")
        telefono.set("")
        email.set("")
        situacion_revista.set("")
        fecha_toma.set("")
    #------------------------------------------------------------------------------------------
    
    
    cargar_datos_treeview()
    
    # --------------------------- Botones que permiten agregar, modificar etc. ---------------------------
    ttk.Button(frame_botones, text="Agregar", command=agregar_datos).grid(row=0, column=0, padx=5)
    ttk.Button(frame_botones, text="Modificar", command=modificar_registro).grid(row=0, column=1, padx=5)
    ttk.Button(frame_botones, text="Eliminar", command=eliminar_registro).grid(row=0, column=2, padx=5)
    ttk.Button(frame_botones, text="Limpiar", command=limpiar_campos).grid(row=0, column=3, padx=5)
    ttk.Button(frame_botones, text="Cerrar", command=ventana.destroy).grid(row=0, column=4, padx=5)
    # ----------------------------------------------------------------------------------------------------
  