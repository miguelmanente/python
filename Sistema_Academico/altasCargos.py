# ========================================================================================
#                  MÓDULO PARA CARGAR LOS CARGOS DOCENTES
# ========================================================================================

# ----------------------------------- LIBRERÍAS ------------------------------------------
import tkinter as tk
from tkinter import ttk, messagebox
from database import conectar
from centraVent import centrar_ventana
# ----------------------------------------------------------------------------------------

# ==========================================================
#              VENTANA GESTIÓN DE CARGOS
# ==========================================================

def ventana_cargos():

    ventana = tk.Toplevel()

    ventana.title("Gestión de Cargos")

    ventana.geometry("700x500")

    # ======================================================
    # VARIABLES
    # ======================================================

    personal_var = tk.StringVar()
    cargo_var = tk.StringVar()
    dia_var = tk.StringVar()
    turno_var = tk.StringVar()
    entrada_var = tk.StringVar()
    salida_var = tk.StringVar()

    profesores_dict = {}

    cargos_dict = {}

    # ======================================================
    # FRAME
    # ======================================================

    frame = ttk.LabelFrame(
        ventana,
        text="Asignación de Cargos"
    )

    frame.pack(
        fill="x",
        padx=10,
        pady=10
    )

    # ======================================================
    # COMBO PERSONAL
    # ======================================================

    ttk.Label(
        frame,
        text="Personal"
    ).grid(row=0, column=0, padx=5, pady=5)

    combo_personal = ttk.Combobox(
        frame,
        textvariable=personal_var,
        width=40,
        state="readonly"
    )

    combo_personal.grid(
        row=0,
        column=1,
        padx=5,
        pady=5
    )

    # ======================================================
    # COMBO CARGOS
    # ======================================================

    ttk.Label(frame, text="Cargo").grid(row=1, column=0, padx=5, pady=5)
    combo_cargo = ttk.Combobox(frame, textvariable=cargo_var, width=40, state="readonly")
    combo_cargo.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(frame, text="Día").grid(row=2, column=0, padx=5, pady=5)
    combo_dia = ttk.Combobox(frame, textvariable=dia_var, values=["","Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Lunes a Viernes"],state="readonly", width=42)
    combo_dia.grid(row=2, column=1, padx=5, pady=5)

    ttk.Label(frame, text="Turno").grid(row=3, column=0, padx=5, pady=5)
    ttk.Combobox(frame, textvariable=turno_var, values=["Mañana", "Tarde", "Noche"], state="readonly", width=37).grid(row=3, column=1, padx=5, pady=5)
    
    ttk.Label(frame, text="Hora Entrada").grid(row=4, column=0, padx=5, pady=5)
    ttk.Entry(frame, textvariable=entrada_var, width=40).grid(row=4, column=1, padx=5, pady=5)
    
    ttk.Label(frame, text="Hora Salida").grid(row=5, column=0, padx=5, pady=5)
    ttk.Entry(frame, textvariable=salida_var, width=40).grid(row=5, column=1, padx=5, pady=5)


    # ======================================================
    # TREEVIEW
    # ======================================================

    columnas = (
        "id",
        "persona",
        "cargo",
        "turno",
        "entrada",
        "salida"
    )

    tree = ttk.Treeview(
        ventana,
        columns=columnas,
        show="headings"
    )

    tree.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    tree.heading("id", text="ID")
    tree.heading("persona", text="Personal")
    tree.heading("cargo", text="Cargo")
    tree.heading("turno", text="Turno")
    tree.heading("entrada", text="Entrada")
    tree.heading("salida", text="Salida")

    tree.column("id", width=50, stretch=False)
    tree.column("persona", width=250)
    tree.column("cargo", width=200)
    tree.column("turno", width=120)
    tree.column("entrada", width=100)
    tree.column("salida", width=100)

    # ======================================================
    # CARGAR PERSONAL
    # ======================================================
    id_seleccionado = None

    def cargar_personal():

        conn = conectar()

        cursor = conn.cursor()

        cursor.execute("""

            SELECT
                id_profesor,
                apenom

            FROM profesores

            ORDER BY apenom

        """)

        datos = cursor.fetchall()

        conn.close()

        lista = []

        for id_, nombre in datos:

            texto = f"{id_} - {nombre}"

            profesores_dict[texto] = id_

            lista.append(texto)

        combo_personal["values"] = lista

    # ======================================================
    # CARGAR CARGOS
    # ======================================================

    def cargar_cargos():

        conn = conectar()

        cursor = conn.cursor()

        cursor.execute("""

            SELECT
                id_cargo,
                nombre_cargo

            FROM cargos

            ORDER BY orden, nombre_cargo

        """)

        datos = cursor.fetchall()

        conn.close()

        lista = []

        for id_, nombre in datos:

            cargos_dict[nombre] = id_

            lista.append(nombre)

        combo_cargo["values"] = lista

    # ======================================================
    # GUARDAR
    # ======================================================

    def guardar():

        if personal_var.get() == "":

            messagebox.showwarning(
                "Atención",
                "Seleccione una persona", parent=ventana
            )

            return

        if cargo_var.get() == "":

            messagebox.showwarning(
                "Atención",
                "Seleccione un cargo", parent=ventana
            )

            return

        id_profesor = profesores_dict[
            personal_var.get()
        ]

        id_cargo = cargos_dict[
            cargo_var.get()
        ]

        conn = conectar()

        cursor = conn.cursor()

        # EVITAR DUPLICADOS
        cursor.execute("""

            SELECT *

            FROM personal_cargos

            WHERE id_profesor=?
            AND id_cargo=?

        """, (

            id_profesor,
            id_cargo

        ))

        existe = cursor.fetchone()

        if existe:

            messagebox.showwarning(
                "Atención",
                "Ese cargo ya está asignado"
            )

            conn.close()

            return

        cursor.execute("""

          INSERT INTO personal_cargos(
                id_profesor,
                id_cargo,
                dia,
                turno,
                hentrada,
                hsalida
            )
            VALUES (?, ?, ?, ?, ?, ?)

        """, (
            id_profesor,
            id_cargo,
            dia_var.get(),
            turno_var.get(),
            entrada_var.get(),
            salida_var.get()
        ))

        conn.commit()

        conn.close()

        messagebox.showinfo(
            "OK",
            "Cargo asignado"
        )

        cargar_tree()
    # ---------------------------------------------------------------

    # ======================================================
    # MODIFICAR
    # ======================================================

    def modificar():

        nonlocal id_seleccionado

        if not id_seleccionado:

            messagebox.showwarning(
                "Atención",
                "Seleccione un registro"
            )

            return

        id_profesor = profesores_dict[
            personal_var.get()
        ]

        id_cargo = cargos_dict[
            cargo_var.get()
        ]

        conn = conectar()

        cursor = conn.cursor()

        cursor.execute("""

            UPDATE personal_cargos

                SET
                    id_profesor=?,
                    id_cargo=?,
                    turno=?,
                    hentrada=?,
                    hsalida=?

            WHERE id_personal_cargo=?

        """, (

            id_profesor,
            id_cargo,
            turno_var.get(),
            entrada_var.get(),
            salida_var.get(),
            id_seleccionado

        ))

        conn.commit()

        conn.close()

        messagebox.showinfo(
            "OK",
            "Cargo modificado"
        )

        cargar_tree()
    # ----------------------------------------------------------------


    # ======================================================
    # ELIMINAR
    # ======================================================

    def eliminar():

        nonlocal id_seleccionado

        if not id_seleccionado:

            messagebox.showwarning(
                "Atención",
                "Seleccione un registro"
            )

            return

        confirmar = messagebox.askyesno(
            "Confirmar",
            "¿Eliminar cargo?"
        )

        if not confirmar:
            return

        conn = conectar()

        cursor = conn.cursor()

        cursor.execute("""

            DELETE FROM personal_cargos

            WHERE id_personal_cargo=?

        """, (id_seleccionado,))

        conn.commit()

        conn.close()

        messagebox.showinfo(
            "OK",
            "Cargo eliminado"
        )

        cargar_tree()
    # ----------------------------------------------------------------

    # ======================================================
    # CARGAR TREEVIEW
    # ======================================================

    def cargar_tree():

        for item in tree.get_children():

            tree.delete(item)

        conn = conectar()

        cursor = conn.cursor()

        cursor.execute("""

            SELECT

            pc.id_personal_cargo,
            p.apenom,
            c.nombre_cargo,
            pc.turno,
            pc.hentrada,
            pc.hsalida

            FROM personal_cargos pc

            JOIN profesores p
            ON pc.id_profesor = p.id_profesor

            JOIN cargos c
            ON pc.id_cargo = c.id_cargo

            ORDER BY p.apenom

        """)

        registros = cursor.fetchall()

        conn.close()

        for fila in registros:

            tree.insert(
                "",
                "end",
                values=fila
            )
    # ----------------------------------------------------------

    # ======================================================
    # SELECCIONAR
    # ======================================================

    def seleccionar(event):

        nonlocal id_seleccionado

        item = tree.selection()

        if not item:
            return

        valores = tree.item(
            item[0],
            "values"
        )

        id_seleccionado = valores[0]

        nombre_persona = valores[1]

        nombre_cargo = valores[2]

        # ==========================================
        # SETEAR COMBO PERSONA
        # ==========================================

        for texto in profesores_dict:

            if nombre_persona in texto:

                personal_var.set(texto)

                break

        # ==========================================
        # SETEAR COMBO CARGO
        # ==========================================

        cargo_var.set(nombre_cargo)
    tree.bind("<<TreeviewSelect>>", seleccionar)
    # -------------------------------------------------------------

    def limpiar():

        nonlocal id_seleccionado

        id_seleccionado = None

        personal_var.set("")

        cargo_var.set("")
    
        cargar_tree()

    # ======================================================
    # BOTONES
    # ======================================================

    frame_btn = ttk.Frame(ventana)

    frame_btn.pack(pady=10)

    ttk.Button(
        frame_btn,
        text="💾 Guardar",
        command=guardar
    ).grid(row=0, column=0, padx=5)

    ttk.Button(
        frame_btn,
        text="✏ Modificar",
        command=modificar
    ).grid(row=0, column=1, padx=5)

    ttk.Button(
        frame_btn,
        text="🗑 Eliminar",
        command=eliminar
    ).grid(row=0, column=2, padx=5)

    ttk.Button(
        frame_btn,
        text="🧹 Limpiar",
        command=limpiar
    ).grid(row=0, column=3, padx=5)

    ttk.Button(
        frame_btn,
        text="❌ Cerrar",
        command=ventana.destroy
    ).grid(row=0, column=4, padx=5)

    # ======================================================
    # INICIO
    # ======================================================

    cargar_personal()

    cargar_cargos()

    cargar_tree()

    centrar_ventana(ventana)