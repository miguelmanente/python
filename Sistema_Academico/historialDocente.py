# =====================================================
#            MÓDULO HISTORIAL DOCENTE
# =====================================================

# ------------------   LIBRERÍAS ----------------------
import tkinter as tk
from tkinter import ttk, messagebox
from database import conectar
from centraVent import centrar_ventana
from datetime import datetime

def ventana_historial():

    ventana = tk.Toplevel()
    ventana.title("Historial Docente")
    ventana.geometry("1200x700")

    ventana.rowconfigure(1, weight=1)
    ventana.columnconfigure(0, weight=1)

    # =====================================================
    #                   VARIABLES
    # =====================================================

    profesor_var = tk.StringVar()
    materia_var = tk.StringVar()
    curso_var = tk.StringVar()
    situacion_var = tk.StringVar()
    inicio_var = tk.StringVar()
    fin_var = tk.StringVar()
    observacion_var = tk.StringVar()

    profesores_dict = {}
    materias_dict = {}
    cursos_dict = {}

    id_seleccionado = None
    buscar_var = tk.StringVar()
    filtro_situacion = tk.StringVar()

    # =====================================================
    #                 FRAME SUPERIOR
    # =====================================================

    frame = ttk.LabelFrame(ventana, text="Datos Historial")
    frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

    # PROFESOR
    ttk.Label(frame, text="Profesor").grid(row=0, column=0, padx=5, pady=5)

    combo_profesor = ttk.Combobox(frame, textvariable=profesor_var, width=40, state="readonly")
    combo_profesor.grid(row=0, column=1, padx=5, pady=5)

    # MATERIA
    ttk.Label(frame, text="Materia").grid(row=0, column=2)

    combo_materia = ttk.Combobox(frame, textvariable=materia_var, width=30, state="readonly")
    combo_materia.grid(row=0, column=3, padx=5)

    # CURSO
    ttk.Label(frame, text="Curso").grid(row=1, column=0)

    combo_curso = ttk.Combobox(frame, textvariable=curso_var, width=30, state="readonly")
    combo_curso.grid(row=1, column=1, padx=5)

    # SITUACION
    ttk.Label(frame, text="Situación").grid(row=1, column=2)

    combo_situacion = ttk.Combobox(
        frame,
        textvariable=situacion_var,
        values=["Titular", "Provisorio", "Suplente"],
        state="readonly"
    )

    combo_situacion.grid(row=1, column=3)

    # FECHA INICIO
    ttk.Label(frame, text="Fecha Inicio").grid(row=2, column=0)

    ttk.Entry(frame, textvariable=inicio_var).grid(row=2, column=1)

    # FECHA FIN
    ttk.Label(frame, text="Fecha Fin").grid(row=2, column=2)

    ttk.Entry(frame, textvariable=fin_var).grid(row=2, column=3)

    # OBSERVACIONES
    ttk.Label(frame, text="Observaciones").grid(row=3, column=0)

    ttk.Entry(frame, textvariable=observacion_var, width=80).grid(
        row=3,
        column=1,
        columnspan=3,
        padx=5,
        pady=5
    )

    # =====================================================
    # ANTIGÜEDAD TOTAL
    # =====================================================

    lbl_total = ttk.Label(
        ventana,
        text="Antigüedad Total: 0 años",
        font=("Arial", 11, "bold"),
        foreground="blue"
    )

    lbl_total.grid(
        row=3,
        column=0,
        sticky="w",
        padx=10,
        pady=5
    )

    # =====================================================
    #      FILTROS PARA SELECCIÓN DE DATOS
    # =====================================================

    frame_filtro = ttk.LabelFrame(ventana, text="Búsqueda")
    frame_filtro.grid(row=1, column=0, sticky="ew", padx=10, pady=5)

    ttk.Label(frame_filtro, text="Profesor").grid(row=0, column=0)

    entry_buscar = ttk.Entry(frame_filtro, textvariable=buscar_var)
    entry_buscar.grid(row=0, column=1, padx=5)

    ttk.Label(frame_filtro, text="Situación").grid(row=0, column=2)

    combo_filtro = ttk.Combobox(
        frame_filtro,
        textvariable=filtro_situacion,
        values=["Todos", "Titular", "Provisorio", "Suplente"],
        state="readonly"
    )

    combo_filtro.grid(row=0, column=3, padx=5)
    combo_filtro.current(0)

    ttk.Button(
        frame_filtro,
        text="Buscar",
        command=lambda: cargar_tree()
    ).grid(row=0, column=4, padx=5)

    # =====================================================
    #                 DISEÑO DEL TREEVIEW
    # =====================================================

    columnas = (
        "id_historial",
        "id_profesor",
        "profesor",
        "materia",
        "curso",
        "situacion",
        "inicio",
        "fin",
        "antiguedad"
    )

    tree = ttk.Treeview(
        ventana,
        columns=columnas,
        show="headings"
    )

    tree.grid(
        row=2,
        column=0,
        sticky="nsew",
        padx=10,
        pady=10
    )

    for col in columnas:
        tree.heading(col, text=col.capitalize())

    # ocultar IDs
    tree.column("id_historial", width=0, stretch=False)
    tree.column("id_profesor", width=0, stretch=False)

    # tamaños
    tree.column("profesor", width=220)
    tree.column("materia", width=180)
    tree.column("curso", width=120)
    tree.column("situacion", width=100)
    tree.column("inicio", width=100)
    tree.column("fin", width=100)
    tree.column("antiguedad", width=120)

    # =====================================================
    #     CARGAR COMBOS CON PROFESORES, MATERIAS Y CURSOS
    # =====================================================

    def cargar_combos():

        conn = conectar()
        cursor = conn.cursor()

        # PROFESORES
        cursor.execute("""
            SELECT id_profesor, apenom
            FROM profesores
        """)

        for id_, nombre in cursor.fetchall():

            texto = f"{id_} - {nombre}"

            profesores_dict[texto] = id_

        combo_profesor["values"] = list(
            profesores_dict.keys()
        )

        # MATERIAS
        cursor.execute("""
            SELECT id_materia, nombre
            FROM materias
        """)

        for id_, nombre in cursor.fetchall():

            texto = f"{id_} - {nombre}"

            materias_dict[texto] = id_

        combo_materia["values"] = list(
            materias_dict.keys()
        )

        # CURSOS
        cursor.execute("""
            SELECT id_curso, nombre
            FROM cursos
        """)

        for id_, nombre in cursor.fetchall():

            texto = f"{id_} - {nombre}"

            cursos_dict[texto] = id_

        combo_curso["values"] = list(
            cursos_dict.keys()
        )

        conn.close()

    # =====================================================
    #            ANTIGUEDAD INDIVIDUAL
    # =====================================================

    def calcular_antiguedad(inicio, fin):

        try:

            fecha_inicio = datetime.strptime(
                inicio,
                "%d/%m/%Y"
            )

            if fin:
                fecha_fin = datetime.strptime(
                    fin,
                    "%d/%m/%Y"
                )
            else:
                fecha_fin = datetime.now()

            dias = (fecha_fin - fecha_inicio).days

            anios = round(dias / 365, 1)

            return f"{anios} años"

        except:
            return ""

    # =====================================================
    #             CARGAR TREEVIEW
    # =====================================================

    def cargar_tree():

        for item in tree.get_children():
            tree.delete(item)

        conn = conectar()
        cursor = conn.cursor()

        query = """
            SELECT
                h.id_historial,
                h.id_profesor,
                p.apenom,
                m.nombre,
                c.nombre,
                h.situacion,
                h.fecha_inicio,
                h.fecha_fin

            FROM historial_docente h

            JOIN profesores p
                ON h.id_profesor = p.id_profesor

            JOIN materias m
                ON h.id_materia = m.id_materia

            JOIN cursos c
                ON h.id_curso = c.id_curso

            WHERE 1=1
        """

        parametros = []

        # filtro profesor
        if buscar_var.get():

            query += " AND p.apenom LIKE ?"

            parametros.append(
                f"%{buscar_var.get()}%"
            )

        # filtro situación
        if filtro_situacion.get() != "Todos":

            query += " AND h.situacion=?"

            parametros.append(
                filtro_situacion.get()
            )

        query += " ORDER BY p.apenom"

        cursor.execute(query, parametros)

        registros = cursor.fetchall()

        for fila in registros:

            antiguedad = calcular_antiguedad(
                fila[6],
                fila[7]
            )

            nueva = list(fila)

            nueva.append(antiguedad)

            tree.insert(
                "",
                "end",
                values=nueva
            )

        conn.close()

    # =====================================================
    #             ANTIGÜEDAD TOTAL DEL DOCENTE
    # =====================================================

    def antiguedad_total(id_profesor):

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT fecha_inicio, fecha_fin
            FROM historial_docente
            WHERE id_profesor=?
            ORDER BY fecha_inicio
        """, (id_profesor,))

        registros = cursor.fetchall()

        conn.close()

        periodos = []

        # ==========================================
        # CONVERTIR FECHAS
        # ==========================================

        for inicio, fin in registros:

            try:

                fecha_inicio = datetime.strptime(
                    inicio,
                    "%d/%m/%Y"
                )

                if fin == "" or fin is None:

                    fecha_fin = datetime.today()

                else:

                    fecha_fin = datetime.strptime(
                        fin,
                        "%d/%m/%Y"
                    )

                periodos.append(
                    (fecha_inicio, fecha_fin)
                )

            except Exception as e:
                print(e)

        # ==========================================
        # NO HAY DATOS
        # ==========================================

        if not periodos:
            return "0 años"

        # ==========================================
        # ORDENAR PERIODOS
        # ==========================================

        periodos.sort(key=lambda x: x[0])

        # ==========================================
        # UNIR PERIODOS SUPERPUESTOS
        # ==========================================

        unidos = []

        actual_inicio, actual_fin = periodos[0]

        for inicio, fin in periodos[1:]:

            # si se superponen
            if inicio <= actual_fin:

                if fin > actual_fin:
                    actual_fin = fin

            else:

                unidos.append(
                    (actual_inicio, actual_fin)
                )

                actual_inicio = inicio
                actual_fin = fin

        unidos.append(
            (actual_inicio, actual_fin)
        )

        # ==========================================
        # SUMAR DÍAS REALES
        # ==========================================

        total_dias = 0

        for inicio, fin in unidos:

            total_dias += (
                fin - inicio
            ).days

        anios = total_dias // 365

        meses = (
            (total_dias % 365) // 30
        )

        return f"{anios} años - {meses} meses"


    # =====================================================
    #          GUARDAR HISTORIAL DOCENTE
    # =====================================================

    def guardar():

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO historial_docente (
                id_profesor,
                id_materia,
                id_curso,
                situacion,
                fecha_inicio,
                fecha_fin,
                observaciones
            )

            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (

            profesores_dict[
                profesor_var.get()
            ],

            materias_dict[
                materia_var.get()
            ],

            cursos_dict[
                curso_var.get()
            ],

            situacion_var.get(),

            inicio_var.get(),

            fin_var.get(),

            observacion_var.get()
        ))

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "OK",
            "Historial guardado",
            parent=ventana
        )

        cargar_tree()
        limpiar()

    # =====================================================
    #          SELECCIONAR REGISTRO
    # =====================================================

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

        id_profesor = valores[1]

        # ==================================
        # ANTIGÜEDAD TOTAL
        # ==================================

        total = antiguedad_total(
            id_profesor
        )

        lbl_total.config(
            text=f"Antigüedad Total: {total}"
        )

        # ==================================
        # CARGAR COMBOS
        # ==================================

        for texto in profesores_dict:

            if valores[2] in texto:

                profesor_var.set(texto)

        for texto in materias_dict:

            if valores[3] in texto:

                materia_var.set(texto)

        for texto in cursos_dict:

            if valores[4] in texto:

                curso_var.set(texto)

        situacion_var.set(valores[5])

        inicio_var.set(valores[6])

        fin_var.set(valores[7])

    tree.bind("<<TreeviewSelect>>", seleccionar)

    # =====================================================
    #            MODIFICAR HISTORIAL
    # =====================================================

    def modificar():

        if not id_seleccionado:

            messagebox.showwarning(
                "Atención",
                "Seleccione un registro"
            )

            return

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE historial_docente
            SET
                id_profesor=?,
                id_materia=?,
                id_curso=?,
                situacion=?,
                fecha_inicio=?,
                fecha_fin=?,
                observaciones=?

            WHERE id_historial=?
        """, (

            profesores_dict[
                profesor_var.get()
            ],

            materias_dict[
                materia_var.get()
            ],

            cursos_dict[
                curso_var.get()
            ],

            situacion_var.get(),

            inicio_var.get(),

            fin_var.get(),

            observacion_var.get(),

            id_seleccionado
        ))

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "OK",
            "Registro modificado"
        )

        cargar_tree()
        limpiar()

    # =====================================================
    #               ELIMINAR HISTORIAL
    # =====================================================

    def eliminar():

        if not id_seleccionado:

            messagebox.showwarning(
                "Atención",
                "Seleccione un registro"
            )

            return

        if not messagebox.askyesno(
            "Confirmar",
            "¿Eliminar historial?"
        ):
            return

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM historial_docente
            WHERE id_historial=?
        """, (id_seleccionado,))

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "OK",
            "Registro eliminado"
        )

        cargar_tree()
        limpiar()

    # =====================================================
    #                 LIMPIAR CAMPOS
    # =====================================================

    def limpiar():

        nonlocal id_seleccionado

        id_seleccionado = None

        profesor_var.set("")
        materia_var.set("")
        curso_var.set("")
        situacion_var.set("")
        inicio_var.set("")
        fin_var.set("")
        observacion_var.set("")

        lbl_total.config(
            text="Antigüedad Total: 0 años"
        )

    # =====================================================
    # BOTONES
    # =====================================================

    frame_btn = ttk.Frame(ventana)
    frame_btn.grid(row=3, column=0, pady=10)

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

    # =====================================================

    # =====================================================
    #           LLAMADOS A MÓDULOS A EJECUTAR
    # =====================================================
    cargar_combos()
    cargar_tree()
    centrar_ventana(ventana)