#===========================================================
#             MÓDULO DE ASISTENCIA DOCENTE
#===========================================================

# ======================   LIBRERÍAS =======================
import tkinter as tk
from tkinter import ttk, messagebox
from database import conectar
from centraVent import centrar_ventana
from datetime import datetime
from reportlab.platypus import (SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
import os


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

    # ================  GENERAR PDFS DE INASISTENCIAS MENSUALES ========
    def pdf_mensual():

        profesor = profesor_var.get()

        if profesor == "":

            messagebox.showwarning(
                "Atención",
                "Seleccione un profesor"
            )

            return

        id_profesor = profesores_dict[profesor]

        mes_actual = datetime.now().month
        anio_actual = datetime.now().year

        conn = conectar()

        cursor = conn.cursor()

        cursor.execute("""

            SELECT

                p.apenom,
                a.fecha_desde,
                a.fecha_hasta,
                a.estado

            FROM asistencias_docentes a

            JOIN profesores p
            ON a.id_profesor = p.id_profesor

            WHERE a.id_profesor = ?

        """, (id_profesor,))

        registros = cursor.fetchall()

        conn.close()

        nombre_pdf = (
            f"Inasist_Mens_{profesor}.pdf"
        )

        ruta_pdf = os.path.join(
            "reportes",
            "pdf",
            nombre_pdf
        )

        doc = SimpleDocTemplate(
            ruta_pdf,
            pagesize=A4
        )

        styles = getSampleStyleSheet()

        elementos = []

        titulo = Paragraph(

            f"<b>INFORME MENSUAL DE ASISTENCIAS</b>",

            styles["Title"]

        )

        elementos.append(titulo)

        elementos.append(Spacer(1, 20))

        nombre_docente = registros[0][0]

        subtitulo = Paragraph(

            f"""
            <b>Docente:</b> {nombre_docente}<br/>
            <b>Mes:</b> {mes_actual}/{anio_actual}
            """,

            styles["BodyText"]

        )

        elementos.append(subtitulo)

        elementos.append(Spacer(1, 20))

        data = [[

            "Desde",
            "Hasta",
            "Días",
            "Estado"

        ]]

        total = 0

        for fila in registros:

            dias = calcular_dias(
                fila[1],
                fila[2]
            )

            total += dias

            data.append([

                fila[1],
                fila[2],
                str(dias),
                fila[3]

            ])

        tabla = Table(data)

        tabla.setStyle(TableStyle([

            ('BACKGROUND', (0,0), (-1,0), colors.darkblue),

            ('TEXTCOLOR', (0,0), (-1,0), colors.white),

            ('GRID', (0,0), (-1,-1), 1, colors.black),

            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold')

        ]))

        elementos.append(tabla)

        elementos.append(Spacer(1, 20))

        total_parrafo = Paragraph(

            f"<b>TOTAL DE INASISTENCIAS:</b> {total} días",

            styles["Heading2"]

        )

        elementos.append(total_parrafo)

        doc.build(elementos)

        messagebox.showinfo(

            "PDF",

            f"Reporte generado:\n{ruta_pdf}"

        )
    # ----------------------------------------------------------------
    
    #=====================  PDF ANUAL ASISTENCIA DOCENTE =============
    def pdf_anual():
        profesor = profesor_var.get()
        if profesor == "":
            messagebox.showwarning(
                "Atención",
                "Seleccione un profesor"
            )
            return

        id_profesor = profesores_dict[profesor]
        anio_actual = datetime.now().year
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT
                p.apenom,
                a.fecha_desde,
                a.fecha_hasta,
                a.estado
            FROM asistencias_docentes a
            JOIN profesores p
            ON a.id_profesor = p.id_profesor
            WHERE a.id_profesor = ?
            ORDER BY a.fecha_desde
        """, (id_profesor,))

        registros = cursor.fetchall()
        conn.close()

        if not registros:
            messagebox.showwarning(
                "Atención",
                "No hay registros"
            )
            return
        nombre_docente = registros[0][0]
        nombre_pdf = (
            f"RepAnu_{nombre_docente}.pdf"
        )
        ruta_pdf = os.path.join(
            "reportes",
            "pdf",
            nombre_pdf
        )

        doc = SimpleDocTemplate(
            ruta_pdf,
            pagesize=A4
        )

        styles = getSampleStyleSheet()
        elementos = []

        # ======================================
        # TITULO
        # ======================================
        titulo = Paragraph(
            f"<b>INFORME ANUAL DE ASISTENCIAS</b>",
            styles["Title"]
        )

        elementos.append(titulo)
        elementos.append(Spacer(1, 20))
        subtitulo = Paragraph(
            f"""
            <b>Docente:</b> {nombre_docente}<br/>
            <b>Año:</b> {anio_actual}
            """,
            styles["BodyText"]
        )

        elementos.append(subtitulo)
        elementos.append(Spacer(1, 20))

        # ======================================
        # TABLA
        # ======================================

        data = [[
            "Mes",
            "Desde",
            "Hasta",
            "Días",
            "Estado"
        ]]

        total = 0
        resumen_estados = {}

        for fila in registros:
            fecha = datetime.strptime(
                fila[1],
                "%d/%m/%Y"
            )

            mes = fecha.strftime("%B")
            dias = calcular_dias(
                fila[1],
                fila[2]
            )

            total += dias
            estado = fila[3]

            if estado not in resumen_estados:
                resumen_estados[estado] = 0

            resumen_estados[estado] += dias

            data.append([
                mes,
                fila[1],
                fila[2],
                str(dias),
                estado
            ])

        tabla = Table(data)
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.darkblue),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('GRID', (0,0), (-1,-1), 1, colors.black),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold')
        ]))

        elementos.append(tabla)
        elementos.append(Spacer(1, 20))

        # ======================================
        # RESUMEN
        # ======================================

        resumen = "<b>RESUMEN ANUAL</b><br/><br/>"
        for estado, dias in resumen_estados.items():
            resumen += f"{estado}: {dias} días<br/>"
        resumen += f"<br/><b>TOTAL ANUAL:</b> {total} días"
        resumen_parrafo = Paragraph(
            resumen,
            styles["BodyText"]
        )

        elementos.append(resumen_parrafo)
        doc.build(elementos)
        messagebox.showinfo(
            "PDF",
            f"PDF anual generado:\n{ruta_pdf}"

        )
    # --------------------------------------------------------------

    

    # =====================  LIMPIAR ENTRYS ========================
    def limpiar():
        profesor_var.set("")
        desde_var.set("")
        hasta_var.set("")
        estado_var.set("")
        observacion_var.set("")

    
    # ======================  BOTONES =============================
    frame_btn = ttk.Frame(ventana)
    frame_btn.grid(row=2, column=0, pady=10)

    # Botón agregar
    ttk.Button(frame_btn, text="💾 Guardar", command=guardar).grid(row=0, column=0, padx=5)
    # Botón Limpiar entrys
    ttk.Button(frame_btn, text="🧹 Limpiar", command=limpiar).grid(row=0, column=1, padx=5)
    # Botón Buscar Docente
    ttk.Button(frame_btn, text="🔍 Buscar Docente", command=buscar_docente).grid(row=0, column=2, padx=5)
    # Botón PDF mensual
    ttk.Button(frame_btn, text="📄 PDF Mensual", command=pdf_mensual).grid(row=0, column=3, padx=5)
    # Botón PDF anual
    ttk.Button(frame_btn, text="📘 PDF Anual", command=pdf_anual).grid(row=0, column=4, padx=5)
    # Botón Cerrar
    ttk.Button(frame_btn, text="❌ Cerrar", command=ventana.destroy).grid(row=0, column=5, padx=5)

    cargar_profesores()

    cargar_tree()

    centrar_ventana(ventana)