import tkinter as tk
from tkinter import ttk, messagebox
from database import conectar
from centraVent import centrar_ventana

def info_asignaciones():
    ventana = tk.Toplevel()
    ventana.title("Asignación Docente")
    ventana.geometry("800x400")

    ventana.rowconfigure(1, weight=1)
    ventana.columnconfigure(0, weight=1)

    frame = ttk.Frame(ventana)
    frame.grid(row=0, column=0, padx=10, pady=10)

    horario_var = tk.StringVar()
    profesor_var = tk.StringVar()
    sitrev_var = tk.StringVar()

    # Combos
    ttk.Label(frame, text="Horario").grid(row=0, column=0)
    combo_horario = ttk.Combobox(frame, textvariable=horario_var, state="readonly")
    combo_horario.grid(row=0, column=1)

    ttk.Label(frame, text="Profesor").grid(row=0, column=2)
    combo_prof = ttk.Combobox(frame, textvariable=profesor_var, state="readonly")
    combo_prof.grid(row=0, column=3)

    ttk.Label(frame, text="Situación").grid(row=1, column=0)
    combo_sit = ttk.Combobox(frame, textvariable=sitrev_var,
                             values=["Titular","Suplente","Provisorio"],
                             state="readonly")
    combo_sit.grid(row=1, column=1)

    # =========================
    # Cargar combos
    # =========================
    def cargar():
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT h.id_horario, m.nombre, c.nombre, h.dia, h.hentrada
            FROM horarios h
            JOIN materias m ON h.id_materia = m.id_materia
            JOIN cursos c ON h.id_curso = c.id_curso
        """)

        combo_horario["values"] = [
            f"{h[0]} - {h[1]} {h[2]} {h[3]} {h[4]}"
            for h in cursor.fetchall()
        ]

        cursor.execute("SELECT id_profesor, apenom FROM profesores")
        combo_prof["values"] = [
            f"{p[0]} - {p[1]}" for p in cursor.fetchall()
        ]

        conn.close()

    # =========================
    # Asignar docente
    # =========================
    def asignar():
        try:
            id_horario = int(horario_var.get().split(" - ")[0])
            id_profesor = int(profesor_var.get().split(" - ")[0])
            valor = horario_var.get()

            if not valor or valor.startswith("None"):
                messagebox.showerror("Error", "Seleccione un horario válido")
            
            else:
                conn = conectar()
                cursor = conn.cursor()

                cursor.execute("""
                    INSERT OR REPLACE INTO asignacion_docente
                    (id_horario, id_profesor, sitrev, activo)
                    VALUES (?, ?, ?, 1)
                """, (id_horario, id_profesor, sitrev_var.get()))

                conn.commit()
                conn.close()

                messagebox.showinfo("OK", "Docente asignado", parent=ventana)
            return
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=ventana)

    ttk.Button(frame, text="Asignar", command=asignar)\
        .grid(row=2, column=0, columnspan=4, pady=10)

    cargar()