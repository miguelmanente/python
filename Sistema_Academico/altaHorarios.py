import tkinter as tk
from tkinter import ttk, messagebox
from database import conectar
from centraVent import centrar_ventana

def info_horarios():
    ventana = tk.Toplevel()
    ventana.title("Información de los Horarios")
    ventana.geometry("1100x700")

    ventana.rowconfigure(1, weight=1)
    ventana.columnconfigure(0, weight=1)

    # =========================
    # FRAME CENTRAL
    # =========================
    frame = ttk.LabelFrame(ventana, text="Carga de Horarios", padding=50)
    frame.grid(row=0, column=0, padx=30, pady=100)

    # Variables
    curso_var = tk.StringVar()
    materia_var = tk.StringVar()
    dia_var = tk.StringVar()
    entrada_var = tk.StringVar()
    salida_var = tk.StringVar()

    # =========================
    # FILA 1
    # =========================
    ttk.Label(frame, text="Curso:").grid(row=0, column=0, sticky="e", padx=10, pady=8)
    combo_curso = ttk.Combobox(frame, textvariable=curso_var, width=25, state="readonly")
    combo_curso.grid(row=0, column=1, padx=5, pady=8)

    ttk.Label(frame, text="Materia:").grid(row=0, column=2, sticky="e", padx=10, pady=8)
    combo_materia = ttk.Combobox(frame, textvariable=materia_var, width=25, state="readonly")
    combo_materia.grid(row=0, column=3, padx=5, pady=8)

    # =========================
    # FILA 2
    # =========================
    ttk.Label(frame, text="Día:").grid(row=1, column=0, sticky="e", padx=10, pady=8)
    combo_dia = ttk.Combobox(
        frame,
        textvariable=dia_var,
        values=["Lunes","Martes","Miércoles","Jueves","Viernes"],
        width=22,
        state="readonly"
    )
    combo_dia.grid(row=1, column=1, padx=5, pady=8)

    ttk.Label(frame, text="Entrada:").grid(row=1, column=2, sticky="e", padx=10, pady=8)
    ttk.Entry(frame, textvariable=entrada_var, width=15).grid(row=1, column=3, padx=5, pady=8)

    # =========================
    # FILA 3
    # =========================
    ttk.Label(frame, text="Salida:").grid(row=2, column=2, sticky="e", padx=10, pady=8)
    ttk.Entry(frame, textvariable=salida_var, width=15).grid(row=2, column=3, padx=5, pady=8)

    # =========================
    # BOTÓN
    # =========================
    # ttk.Button(frame, text="💾 Guardar", width=20)\
    #     .grid(row=3, column=0, columnspan=4, pady=15)
    ttk.Button(frame, text=" Salir", command=ventana.destroy, width=20)\
        .grid(row=4, column=0, columnspan=4, pady=15)


    # =========================
    # Cargar combos
    # =========================
    def cargar_combos():
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT id_curso, nombre FROM cursos")
        combo_curso["values"] = [f"{c[0]} - {c[1]}" for c in cursor.fetchall()]

        cursor.execute("SELECT id_materia, nombre FROM materias")
        combo_materia["values"] = [f"{m[0]} - {m[1]}" for m in cursor.fetchall()]

        conn.close()

    #---------------------------------------------------------------------
    #   Control de horarios
    # --------------------------------------------------------------------
    def horario_duplicado(id_curso, id_materia, dia, entrada, salida):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM horarios
            WHERE id_curso = ?
            AND id_materia = ?
            AND dia = ?
            AND hentrada = ?
            AND hsalida = ?
        """, (id_curso, id_materia, dia, entrada, salida))

        existe = cursor.fetchone()[0]
        conn.close()

        return existe > 0

    # =========================
    # Guardar
    # =========================
    def guardar():
        try:
            id_curso = int(curso_var.get().split(" - ")[0])
            id_materia = int(materia_var.get().split(" - ")[0])
            if horario_duplicado(id_curso, id_materia, dia_var, entrada_var, salida_var):
                messagebox.showerror("Error", "Ese horario ya existe")
            else:
                conn = conectar()
                cursor = conn.cursor()

                cursor.execute("""
                    INSERT INTO horarios (id_curso, id_materia, dia, hentrada, hsalida)
                    VALUES (?, ?, ?, ?, ?)
                """, (id_curso, id_materia, dia_var.get(), entrada_var.get(), salida_var.get()))

                conn.commit()
                conn.close()

                messagebox.showinfo("OK", " El Horario ha sido guardado", parent=ventana)
            return
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=ventana)
    
    ttk.Button(frame, text="💾 Guardar", command=guardar,  width=20)\
        .grid(row=3, column=0, columnspan=4, pady=15)

    cargar_combos()

    centrar_ventana(ventana)