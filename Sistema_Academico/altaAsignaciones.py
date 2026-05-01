import tkinter as tk
from tkinter import ttk, messagebox
from database import conectar
from centraVent import centrar_ventana

def info_asignaciones():

    ventana = tk.Toplevel()
    ventana.title("Asignaciones Docentes")
    ventana.geometry("1100x700")

    ventana.rowconfigure(0, weight=1)
    ventana.rowconfigure(1, weight=2)
    ventana.columnconfigure(0, weight=1)

    # =========================
    # FRAME SUPERIOR
    # =========================
    frame_superior = ttk.LabelFrame(ventana, text="Asignar Profesor", padding=20)
    frame_superior.grid(row=0, column=0, sticky="nsew", padx=20, pady=10)

    frame_superior.columnconfigure(1, weight=1)
    frame_superior.columnconfigure(3, weight=1)

    # Variables
    profesor_var = tk.StringVar()
    horario_var = tk.StringVar()
    situacion_var = tk.StringVar()

    profesores_dict = {}
    horarios_dict = {}

    # =========================
    # CAMPOS
    # =========================
    ttk.Label(frame_superior, text="Profesor:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
    combo_profesor = ttk.Combobox(frame_superior, textvariable=profesor_var, state="readonly")
    combo_profesor.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

    ttk.Label(frame_superior, text="Horario:").grid(row=0, column=2, sticky="e", padx=5, pady=5)
    combo_horario = ttk.Combobox(frame_superior, textvariable=horario_var, state="readonly")
    combo_horario.grid(row=0, column=3, sticky="ew", padx=5, pady=5)

    ttk.Label(frame_superior, text="Situación:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    combo_situacion = ttk.Combobox(
        frame_superior,
        textvariable=situacion_var,
        values=["Titular", "Provisorio", "Suplente"],
        state="readonly"
    )
    combo_situacion.grid(row=1, column=1, padx=5, pady=5)

    # =========================
    # TREEVIEW
    # =========================
    frame_inferior = ttk.LabelFrame(ventana, text="Listado Asignaciones", padding=10)
    frame_inferior.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)

    frame_inferior.rowconfigure(0, weight=1)
    frame_inferior.columnconfigure(0, weight=1)

    columnas = ("id", "profesor", "curso", "materia", "dia", "entrada", "salida", "situacion")

    tree = ttk.Treeview(frame_inferior, columns=columnas, show="headings")
    tree.grid(row=0, column=0, sticky="nsew")

    for col in columnas:
        tree.heading(col, text=col.capitalize())

    tree.column("id", width=0, stretch=False)

    scrollbar_y = ttk.Scrollbar(frame_inferior, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar_y.set)
    scrollbar_y.grid(row=0, column=1, sticky="ns")

    # =========================
    # FUNCIONES
    # =========================
    def cargar_combos():
        conn = conectar()
        cursor = conn.cursor()

        profesores_dict.clear()
        horarios_dict.clear()

        # Profesores
        cursor.execute("SELECT id_profesor, apenom FROM profesores")
        for id_, nombre in cursor.fetchall():
            texto = f"{id_} - {nombre}"
            profesores_dict[texto] = id_

        combo_profesor["values"] = list(profesores_dict.keys())

        # Horarios
        cursor.execute("""
            SELECT h.id_horario, c.nombre, m.nombre, h.dia, h.hentrada, h.hsalida
            FROM horarios h
            JOIN cursos c ON h.id_curso = c.id_curso
            JOIN materias m ON h.id_materia = m.id_materia
        """)

        for fila in cursor.fetchall():
            texto = f"{fila[0]} - {fila[1]} | {fila[2]} | {fila[3]} {fila[4]}-{fila[5]}"
            horarios_dict[texto] = fila[0]

        combo_horario["values"] = list(horarios_dict.keys())

        conn.close()

    def cargar_tree():
        for item in tree.get_children():
            tree.delete(item)

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT a.id_asignacion, p.apenom, c.nombre, m.nombre,
                h.dia, h.hentrada, h.hsalida, a.srprofesor
            FROM asignaciones_docentes a
            LEFT JOIN profesores p ON a.id_profesor = p.id_profesor
            LEFT JOIN horarios h ON a.id_horario = h.id_horario
            LEFT JOIN cursos c ON h.id_curso = c.id_curso
            LEFT JOIN materias m ON h.id_materia = m.id_materia
        """)

        for fila in cursor.fetchall():
            tree.insert("", "end", values=fila)

        conn.close()

    id_seleccionado = None

    def seleccionar(event):
        nonlocal id_seleccionado

        item = tree.selection()
        if not item:
            return

        valores = tree.item(item[0], "values")
        id_seleccionado = valores[0]

        profesor_var.set(valores[1])
        situacion_var.set(valores[7])

    tree.bind("<<TreeviewSelect>>", seleccionar)

    def guardar():
        if not profesor_var.get() or not horario_var.get() or not situacion_var.get():
            messagebox.showwarning("Atención", "Complete todos los campos")
            return

        try:
            conn = conectar()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO asignaciones_docentes (id_profesor, id_horario, srprofesor)
                VALUES (?, ?, ?)
            """, (
                profesores_dict[profesor_var.get()],
                horarios_dict[horario_var.get()],
                situacion_var.get()
            ))

            conn.commit()
            conn.close()

            messagebox.showinfo("OK", "Asignación guardada")
            cargar_tree()
            limpiar()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def eliminar():
        nonlocal id_seleccionado

        if not id_seleccionado:
            messagebox.showwarning("Atención", "Seleccione un registro")
            return

        if not messagebox.askyesno("Confirmar", "¿Eliminar asignación?"):
            return

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM asignaciones_docentes WHERE id_asignacion=?", (id_seleccionado,))
        conn.commit()
        conn.close()

        cargar_tree()
        limpiar()

    def limpiar():
        nonlocal id_seleccionado
        id_seleccionado = None

        profesor_var.set("")
        horario_var.set("")
        situacion_var.set("")

    # =========================
    # BOTONES
    # =========================
    frame_botones = ttk.Frame(frame_superior)
    frame_botones.grid(row=2, column=0, columnspan=4, pady=15)

    ttk.Button(frame_botones, text="💾 Guardar", command=guardar).grid(row=0, column=0, padx=5)
    ttk.Button(frame_botones, text="Eliminar", command=eliminar).grid(row=0, column=1, padx=5)
    ttk.Button(frame_botones, text="Limpiar", command=limpiar).grid(row=0, column=2, padx=5)
    ttk.Button(frame_botones, text="Salir", command=ventana.destroy).grid(row=0, column=3, padx=5)

    # =========================
    # INICIO
    # =========================
    cargar_combos()
    cargar_tree()
    centrar_ventana(ventana)