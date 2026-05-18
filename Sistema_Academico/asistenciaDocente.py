#===========================================================
#             MÓDULO DE ASISTENCIA DOCENTE
#===========================================================

# ======================   LIBRERÍAS =======================
import tkinter as tk
from tkinter import ttk, messagebox
from database import conectar
from centraVent import centrar_ventana
from datetime import datetime


# ================== VENTANA DE ASISTENCIA ==========================
def ventana_asistencias():
    ventana = tk.Toplevel()
    ventana.title("Control de Asistencias")
    ventana.geometry("1200x700")
    ventana.rowconfigure(1, weight=1)
    ventana.columnconfigure(0, weight=1)

    # =============== VARIABLES ====================================
    profesor_var = tk.StringVar()
    desde_var = tk.StringVar()
    hasta_var = tk.StringVar()
    estado_var = tk.StringVar()
    observacion_var = tk.StringVar()
    profesores_dict = {}
    id_seleccionado = None

    # ============ FRAME SUPERIOR =================================
    frame = ttk.LabelFrame(ventana, text="Asistencia Docente")
    frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

    # ================ COMBO PROFESORES ============================
    ttk.Label(frame, text="Profesor").grid(row=0, column=0, padx=5, pady=5)
    combo_profesor = ttk.Combobox(frame, textvariable=profesor_var, width=40, state="readonly")
    combo_profesor.grid(row=0, column=1, padx=5, pady=5)

    # ====================  INGRESOS DE FECHAS ========================
    ttk.Label(
        frame,
        text="Desde"
    ).grid(row=1, column=0)

    ttk.Entry(
        frame,
        textvariable=desde_var
    ).grid(row=1, column=1)


    ttk.Label(
        frame,
        text="Hasta"
    ).grid(row=1, column=2)

    ttk.Entry(
        frame,
        textvariable=hasta_var
    ).grid(row=1, column=3)

    # ========================== ESTADO =============================
    ttk.Label(
        frame,
        text="Estado"
    ).grid(row=2, column=0)

    combo_estado = ttk.Combobox(

        frame,

        textvariable=estado_var,

        values=[

            "Presente",
            "Ausente",
            "Licencia Médica",
            "ART",
            "Particular",
            "Maternidad",
            "Estudio"

        ],

        state="readonly",

        width=30
    )

    combo_estado.grid(
        row=2,
        column=1,
        padx=5,
        pady=5
    )

    # =========================== OBSERVACIONES ==========================
    ttk.Label(
        frame,
        text="Observación"
    ).grid(row=3, column=0)

    ttk.Entry(
        frame,
        textvariable=observacion_var,
        width=80
    ).grid(
        row=3,
        column=1,
        columnspan=3,
        padx=5,
        pady=5
    )

    # ============================= TREEVIEW ============================
    columnas = (

        "id",
        "profesor",
        "desde",
        "hasta",
        "dias",
        "estado",
        "observacion"
    )

    tree = ttk.Treeview(ventana, columns=columnas, show="headings")
    tree.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

     # Encabezados
    tree.heading("id", text="ID")
    tree.heading("profesor", text="Profesor")
    tree.heading("desde", text="Desde el Día")
    tree.heading("hasta", text="Hasta el Día")
    tree.heading("dias", text="Cant.de Dias")
    tree.heading("estado", text="Estado")
    tree.heading("observacion", text="Observación")
   
    tree.column("id", width=0, stretch=False)
    tree.column("profesor", width=150, anchor="center")
    tree.column("desde", width=100, anchor="center")
    tree.column("hasta", width=100, anchor="center")
    tree.column("dias", width=50, anchor="center")
    tree.column("estado", width=100, anchor="center")
    tree.column("observacion", width=200, anchor="w")

    # ==========  RESUMEN DE INASISTENCIAS POR PROFESOR ========================
    lbl_resumen = ttk.Label(ventana, text="Resumen de inasistencias: ", font=("Arial", 11, "bold"), foreground="blue")
    lbl_resumen.grid(row=2, column=0, sticky="w", padx=10, pady=5)

    # =========== MENSAJES DE ALERTAS CUANDO SE SUPERAN LÍMITES ================
    lbl_alerta = ttk.Label(ventana, text="", font=("Arial", 11, "bold"), foreground="red")
    lbl_alerta.grid(row=3, column=0, sticky="w", padx=10, pady=5)

    # =========================  CARGA DE PROFESORES ============================
    def cargar_profesores():

        conn = conectar()

        cursor = conn.cursor()

        cursor.execute("""
            SELECT id_profesor, apenom
            FROM profesores
            ORDER BY apenom
        """)

        for id_, nombre in cursor.fetchall():

            texto = f"{id_} - {nombre}"

            profesores_dict[texto] = id_

        combo_profesor["values"] = list(
            profesores_dict.keys()
        )

        conn.close()
    
    # ====================== CÁLCULO DE DÍAS  ============================
    def calcular_dias(desde, hasta):

        fecha_desde = datetime.strptime(
            desde,
            "%d/%m/%Y"
        )

        fecha_hasta = datetime.strptime(
            hasta,
            "%d/%m/%Y"
        )

        dias = (
            fecha_hasta - fecha_desde
        ).days + 1

        return dias
    
    # ================== GUARDAR DATOS =====================================
    def guardar():

        conn = conectar()

        cursor = conn.cursor()

        cursor.execute("""

            INSERT INTO asistencias_docentes(
               
                id_profesor,
                fecha_desde,
                fecha_hasta,
                estado,
                observacion

            )

            VALUES (?, ?, ?, ?, ?)

        """, (

            profesores_dict[profesor_var.get()],
            desde_var.get(),
            hasta_var.get(),
            estado_var.get(),
            observacion_var.get()

        ))

        conn.commit()

        conn.close()

        dias = calcular_dias(
            desde_var.get(),
            hasta_var.get()
        )

        if dias >= 5:

            messagebox.showwarning(

                "ALERTA SUPLENTE",

                "El docente supera 5 días de inasistencia"

            )

        messagebox.showinfo(
            "OK",
            "Registro guardado"
        )

        cargar_tree()

        limpiar()
    
    # ===================== CARGAR TREEVIEW  =====================

    def cargar_tree(id_profesor=None):

        for item in tree.get_children():

            tree.delete(item)

        conn = conectar()

        cursor = conn.cursor()

        query = """

            SELECT

                a.id_asistencia,
                p.apenom,
                a.fecha_desde,
                a.fecha_hasta,
                a.estado,
                a.observacion

            FROM asistencias_docentes a

            JOIN profesores p
            ON a.id_profesor = p.id_profesor

        """

        parametros = []

        if id_profesor:

            query += " WHERE a.id_profesor=?"

            parametros.append(id_profesor)

        query += " ORDER BY a.fecha_desde DESC"

        cursor.execute(query, parametros)

        for fila in cursor.fetchall():

            dias = calcular_dias(
                fila[2],
                fila[3]
            )

            nueva = list(fila)

            nueva.insert(4, dias)

            tree.insert(
                "",
                "end",
                values=nueva
            )

        conn.close()




    #  ================  RESUMEN DE INASISTENCIAS ==================
    def resumen_inasistencias(id_profesor):

        conn = conectar()

        cursor = conn.cursor()

        cursor.execute("""

            SELECT
                estado,
                fecha_desde,
                fecha_hasta

            FROM asistencias_docentes

            WHERE id_profesor = ?

        """, (id_profesor,))

        resultados = cursor.fetchall()

        conn.close()

        resumen = {}

        total_general = 0

        for estado, desde, hasta in resultados:

            dias = calcular_dias(desde, hasta)

            total_general += dias

            if estado not in resumen:

                resumen[estado] = 0

            resumen[estado] += dias

        texto = ""

        for estado, total in resumen.items():

            texto += f"{estado}: {total} días\n"

        texto += f"\nTOTAL GENERAL: {total_general} días"

        lbl_resumen.config(text=texto)
    # =======================================================


    # ==================== BUSCA DOCENTES ===================
    def buscar_docente():

        if profesor_var.get() == "":

            messagebox.showwarning(
                "Atención",
                "Seleccione un profesor"
            )

            return

        id_profesor = profesores_dict[
            profesor_var.get()
        ]

        cargar_tree(id_profesor)

        resumen_inasistencias(id_profesor)

        verificar_alertas(id_profesor)
    # --------------------------------------------------------------

    # ==================  FUNCIÓN DE ALERTAS =======================
    def verificar_alertas(id_profesor):

        conn = conectar()

        cursor = conn.cursor()

        cursor.execute("""

            SELECT
                estado,
                fecha_desde,
                fecha_hasta

            FROM asistencias_docentes

            WHERE id_profesor = ?

        """, (id_profesor,))

        registros = cursor.fetchall()

        conn.close()

        licencia_medica = 0
        particular = 0
        suplente = False

        for estado, desde, hasta in registros:

            dias = calcular_dias(desde, hasta)

            # LICENCIA MÉDICA
            if estado == "Licencia Médica":

                licencia_medica += dias

            # PARTICULAR / INJUSTIFICADA
            if estado == "Particular":

                particular += dias

            # NECESITA SUPLENTE
            if dias >= 5:

                suplente = True

        alertas = ""

        if licencia_medica >= 20:

            alertas += (
                f"⚠ Supera 20 días de Licencia Médica "
                f"({licencia_medica} días)\n"
            )

        if particular >= 5:

            alertas += (
                f"⚠ Supera 5 faltas particulares "
                f"({particular} días)\n"
            )

        if suplente:

            alertas += (
                "⚠ Necesita designación de suplente\n"
            )

        if alertas == "":

            alertas = "Sin alertas"

        lbl_alerta.config(text=alertas)
    # -----------------------------------------------------------------





    # =====================  LIMPIAR ENTRYS ========================
    def limpiar():
        profesor_var.set("")
        desde_var.set("")
        hasta_var.set("")
        estado_var.set("")
        observacion_var.set("")

    
    # ======================  BOTONES =============================
    frame_btn = ttk.Frame(ventana)

    frame_btn.grid(
        row=2,
        column=0,
        pady=10
    )

    ttk.Button(

        frame_btn,

        text="💾 Guardar",

        command=guardar

    ).grid(row=0, column=0, padx=5)

    ttk.Button(

        frame_btn,

        text="🧹 Limpiar",

        command=limpiar

    ).grid(row=0, column=1, padx=5)

    ttk.Button(

        frame_btn,

        text="🔍 Buscar Docente",

        command=buscar_docente

    ).grid(row=0, column=2, padx=5)

    ttk.Button(

        frame_btn,

        text="❌ Cerrar",

        command=ventana.destroy

    ).grid(row=0, column=3, padx=5)

    cargar_profesores()

    cargar_tree()

    centrar_ventana(ventana)