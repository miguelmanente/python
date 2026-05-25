#===========================================================
#             MÓDULO DE ASISTENCIA DOCENTE
#===========================================================

# ======================   LIBRERÍAS =======================
import tkinter as tk
from tkinter import ttk, messagebox
from database import conectar
from centraVent import centrar_ventana
from datetime import datetime, timedelta
from reportlab.platypus import (SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
import os
from backup import crear_backup

# ================== VENTANA DE INASISTENCIA ==========================
def ventana_asistencias():
    ventana = tk.Toplevel()
    ventana.title("Control de Inasistencias")
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
    frame = ttk.LabelFrame(ventana, text="Inasistencia Docente")
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
    lbl_resumen.grid(row=3, column=0, sticky="w", padx=10, pady=5)

    # =========== MENSAJES DE ALERTAS CUANDO SE SUPERAN LÍMITES ================
    lbl_alerta = ttk.Label(ventana, text="", font=("Arial", 11, "bold"), foreground="red")
    lbl_alerta.grid(row=4, column=0, sticky="w", padx=10, pady=5)

    # ============== Cantidad de días trabajados ===============================
    lbl_trabajados = ttk.Label(ventana, text="Días trabajados: 0", font=("Arial", 11, "bold"), foreground="green")
    lbl_trabajados.grid(row=5, column=0, sticky="w", padx=10, pady=5)

    # =========================  CARGA DE PROFESORES ============================
    def cargar_profesores():

        conn = conectar()

        cursor = conn.cursor()

        cursor.execute("""

            SELECT

                pc.id_personal_cargo,
                p.apenom,
                c.nombre_cargo

            FROM personal_cargos pc

            JOIN profesores p
            ON pc.id_profesor = p.id_profesor

            JOIN cargos c
            ON pc.id_cargo = c.id_cargo

            ORDER BY p.apenom

        """)

        resultados = cursor.fetchall()

        profesores_dict.clear()

        lista = []

        for id_pc, nombre, cargo in resultados:

            texto = f"{nombre} - {cargo}"

            profesores_dict[texto] = id_pc

            lista.append(texto)

        combo_profesor["values"] = lista

        conn.close()    
    # -----------------------------------------------------------

    # ======================= CALCULA LOS DÍAS DE INASISTENCIAS =====================
    def calcular_dias(id_personal_cargo, desde, hasta):

        conn = conectar()

        cursor = conn.cursor()

        # ==========================================
        # OBTENER CARGO
        # ==========================================

        cursor.execute("""

            SELECT c.nombre_cargo

            FROM personal_cargos pc

            JOIN cargos c
            ON pc.id_cargo = c.id_cargo

            WHERE pc.id_personal_cargo=?

        """, (id_personal_cargo,))

        cargo = cursor.fetchone()[0]

        # ==========================================
        # SI ES PROFESOR → USA HORARIOS
        # ==========================================

        if cargo == "Profesor":

            id_profesor = obtener_id_profesor(
                id_personal_cargo
            )

            cursor.execute("""

                SELECT DISTINCT h.dia

                FROM asignaciones_docentes a

                JOIN horarios h
                ON a.id_horario = h.id_horario

                WHERE a.id_profesor=?

            """, (id_profesor,))

            resultados = cursor.fetchall()

            dias_trabajo = [fila[0] for fila in resultados]

            mapa = {

                "Lunes": 0,
                "Martes": 1,
                "Miércoles": 2,
                "Jueves": 3,
                "Viernes": 4

            }

            dias_validos = []

            for dia in dias_trabajo:

                if dia in mapa:

                    dias_validos.append(
                        mapa[dia]
                    )

        # ==========================================
        # SI ES CARGO → LUNES A VIERNES
        # ==========================================

        else:

            dias_validos = [0, 1, 2, 3, 4]

        conn.close()

        # ==========================================
        # CONTAR DÍAS
        # ==========================================

        fecha_actual = datetime.strptime(
            desde,
            "%d/%m/%Y"
        )

        fecha_hasta = datetime.strptime(
            hasta,
            "%d/%m/%Y"
        )

        total = 0

        while fecha_actual <= fecha_hasta:

            if fecha_actual.weekday() in dias_validos:

                total += 1

            fecha_actual += timedelta(days=1)

        return total
    # ---------------------------------------------------------------------
        
    # ================= CONTAR DÍAS LABORALES ============================
    def contar_dias_laborales(id_profesor):

        conn = conectar()
        cursor = conn.cursor()

        # ============================================
        # OBTENER DÍAS DE TRABAJO DEL DOCENTE
        # ============================================

        cursor.execute("""

            SELECT DISTINCT h.dia

            FROM personal_cargos pc

            JOIN asignaciones_docentes a
            ON pc.id_profesor = a.id_profesor

            JOIN horarios h
            ON a.id_horario = h.id_horario

            WHERE pc.id_personal_cargo = ?

        """, (id_profesor,))

        resultados = cursor.fetchall()

        conn.close()

        dias_trabajo = [fila[0] for fila in resultados]

        dias_map = {

            "Lunes": 0,
            "Martes": 1,
            "Miércoles": 2,
            "Jueves": 3,
            "Viernes": 4
        }

        fecha_inicio = datetime.strptime(
            "01/03/2026",
            "%d/%m/%Y"
        )

        fecha_fin = datetime.today()

        total = 0

        while fecha_inicio <= fecha_fin:

            dias_validos = []

            for dia in dias_trabajo:

                if dia == "Lunes a Viernes":

                    dias_validos.extend([0, 1, 2, 3, 4])

                elif dia in dias_map:

                    dias_validos.append(dias_map[dia])

            if fecha_inicio.weekday() in dias_validos:

                total += 1

            fecha_inicio += timedelta(days=1)

        return total
    # -----------------------------------------------------------------------

    
    # ================== GUARDAR DATOS =====================================
    def guardar():

        conn = conectar()

        cursor = conn.cursor()

        id_personal_cargo = profesores_dict[
            profesor_var.get()
        ]

        # OBTENER EL ID DEL PROFESOR REAL
        id_profesor = obtener_id_profesor(
            id_personal_cargo
        )

        cursor.execute("""

            INSERT INTO asistencias_docentes(

                id_profesor,
                id_personal_cargo,
                fecha_desde,
                fecha_hasta,
                estado,
                observacion

            )

            VALUES (?, ?, ?, ?, ?, ?)

        """, (

            id_profesor,
            id_personal_cargo,
            desde_var.get(),
            hasta_var.get(),
            estado_var.get(),
            observacion_var.get()

        ))

        conn.commit()

        conn.close()

        dias = calcular_dias(
            id_profesor,
            desde_var.get(),
            hasta_var.get()
        )

        if dias >= 5:

            messagebox.showwarning(

                "ALERTA SUPLENTE",

                "El docente supera 5 días de inasistencia", parent=ventana

            )

        messagebox.showinfo(
            "OK",
            "Registro guardado", parent=ventana
        )

        cargar_tree()

        limpiar()
    # ------------------------------------------------------------

    # ==========================================================
    # OBTENER ID DEL PROFESOR DESDE PERSONAL_CARGO
    # ==========================================================
    def obtener_id_profesor(id_personal_cargo):

        conn = conectar()

        cursor = conn.cursor()

        cursor.execute("""

            SELECT id_profesor

            FROM personal_cargos

            WHERE id_personal_cargo=?

        """, (id_personal_cargo,))

        resultado = cursor.fetchone()

        conn.close()

        if resultado:

            return resultado[0]

        return None
    # ----------------------------------------------------------



    # ============== MODIFICAR REGISTRO ASISTENCIA ===============
    def modificar():

        nonlocal id_seleccionado

        if not id_seleccionado:

            messagebox.showwarning(
                "Atención",
                "Seleccione un registro", parent=ventana
            )

            return

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""

            UPDATE asistencias_docentes
            SET

                id_personal_cargo=?,
                fecha_desde=?,
                fecha_hasta=?,
                estado=?,
                observacion=?

            WHERE id_asistencia=?

        """, (

            profesores_dict[profesor_var.get()],
            desde_var.get(),
            hasta_var.get(),
            estado_var.get(),
            observacion_var.get(),
            id_seleccionado

        ))

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "OK",
            "Registro modificado", parent=ventana
        )

        cargar_tree()
        limpiar()
    # ------------------------------------------------------------

    # ===================== ELIMINAR =====================
    def eliminar():

        nonlocal id_seleccionado

        if not id_seleccionado:

            messagebox.showwarning(
                "Atención",
                "Seleccione un registro", parent=ventana
            )

            return

        confirmar = messagebox.askyesno(
            "Confirmar",
            "¿Eliminar registro?", parent=ventana
        )

        if not confirmar:
            return

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""

            DELETE FROM asistencias_docentes
            WHERE id_asistencia=?

        """, (id_seleccionado,))

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "OK",
            "Registro eliminado", parent=ventana
        )

        cargar_tree()
        limpiar()
    # ------------------------------------------------------------
    
    # ===================== CARGAR TREEVIEW  =====================
    def cargar_tree(id_profesor=None):

        for item in tree.get_children():

            tree.delete(item)

        conn = conectar()

        cursor = conn.cursor()

        query = """

            SELECT

                a.id_asistencia,
                a.id_personal_cargo,
                p.apenom,
                c.nombre_cargo,
                a.fecha_desde,
                a.fecha_hasta,
                a.estado,
                a.observacion

            FROM asistencias_docentes a

            JOIN personal_cargos pc
            ON a.id_personal_cargo = pc.id_personal_cargo

            JOIN profesores p
            ON pc.id_profesor = p.id_profesor

            JOIN cargos c
            ON pc.id_cargo = c.id_cargo

        """

        parametros = []

        if id_profesor:

            query += " WHERE a.id_personal_cargo=?"

            parametros.append(id_profesor)

        query += " ORDER BY a.fecha_desde DESC"

        cursor.execute(query, parametros)

        registros = cursor.fetchall()

        for fila in registros:

            dias = calcular_dias(

                fila[1],
                fila[4],
                fila[5]

            )

            nombre_completo = f"{fila[2]} - {fila[3]}"

            nueva = [

                fila[0],   # id asistencia
                nombre_completo,
                fila[4],   # desde
                fila[5],   # hasta
                dias,
                fila[6],   # estado
                fila[7]    # observacion

            ]

            tree.insert(
                "",
                "end",
                values=nueva
            )

        conn.close()
    
    #------------------------------------------------------------------

    # ============ SELECCIONAR REGISTROS DEL TREEVIEW ==============
    def seleccionar(event):

        nonlocal id_seleccionado

        item = tree.selection()

        if not item:
            return

        valores = tree.item(item[0], "values")

        id_seleccionado = valores[0]

        # ======================
        # CARGAR CAMPOS
        # ======================

        nombre_profesor = valores[1]

        # buscar texto completo del combo
        for texto in profesores_dict:

            if nombre_profesor in texto:

                profesor_var.set(texto)
                break

        desde_var.set(valores[2])
        hasta_var.set(valores[3])
        estado_var.set(valores[5])
        observacion_var.set(valores[6])

    tree.bind("<<TreeviewSelect>>", seleccionar)
    # --------------------------------------------------------------



    #  ================  RESUMEN DE INASISTENCIAS ==================
    def resumen_inasistencias(id_personal_cargo):

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id_profesor
            FROM personal_cargos
            WHERE id_personal_cargo=?
        """, (id_personal_cargo,))

        resultado = cursor.fetchone()

        if not resultado:
            conn.close()
            return

        id_profesor = resultado[0]

        cursor.execute("""
            SELECT
                a.estado,
                a.fecha_desde,
                a.fecha_hasta
            FROM asistencias_docentes a
            JOIN personal_cargos pc
                ON a.id_personal_cargo = pc.id_personal_cargo
            WHERE pc.id_profesor=?
        """, (id_profesor,))

        registros = cursor.fetchall()

        conn.close()

        resumen = {}
        dias_unicos = set()

        for estado, desde, hasta in registros:

            fecha_actual = datetime.strptime(
                desde,
                "%d/%m/%Y"
            )

            fecha_hasta = datetime.strptime(
                hasta,
                "%d/%m/%Y"
            )

            while fecha_actual <= fecha_hasta:

                fecha_txt = fecha_actual.strftime(
                    "%d/%m/%Y"
                )

                dias_unicos.add(fecha_txt)

                if estado not in resumen:
                    resumen[estado] = set()

                resumen[estado].add(fecha_txt)

                fecha_actual += timedelta(days=1)

        texto = ""

        for estado, fechas in resumen.items():

            texto += (
                f"{estado}: "
                f"{len(fechas)} días\n"
            )

        texto += (
            f"\nTOTAL GENERAL: "
            f"{len(dias_unicos)} días"
        )

        lbl_resumen.config(text=texto)
    # ------------------------------------------------------------------------------

     # ================= TOTAL INASISTENCIAS =================
    def total_inasistencias(id_personal_cargo):

        conn = conectar()
        cursor = conn.cursor()

        # obtener profesor real
        cursor.execute("""
            SELECT id_profesor
            FROM personal_cargos
            WHERE id_personal_cargo=?
        """, (id_personal_cargo,))

        resultado = cursor.fetchone()

        if not resultado:
            conn.close()
            return 0

        id_profesor = resultado[0]

        cursor.execute("""
            SELECT
                fecha_desde,
                fecha_hasta
            FROM asistencias_docentes a
            JOIN personal_cargos pc
                ON a.id_personal_cargo = pc.id_personal_cargo
            WHERE pc.id_profesor = ?
        """, (id_profesor,))

        registros = cursor.fetchall()

        conn.close()

        dias_unicos = set()

        for desde, hasta in registros:

            fecha_actual = datetime.strptime(
                desde,
                "%d/%m/%Y"
            )

            fecha_hasta = datetime.strptime(
                hasta,
                "%d/%m/%Y"
            )

            while fecha_actual <= fecha_hasta:

                dias_unicos.add(
                    fecha_actual.strftime("%d/%m/%Y")
                )

                fecha_actual += timedelta(days=1)

        return len(dias_unicos)
    # ------------------------------------------------------------ 

    # ==================== BUSCA DOCENTES ===================
    def buscar_docente():

        if profesor_var.get() == "":

            messagebox.showwarning(
                "Atención",
                "Seleccione un profesor", parent=ventana
            )

            return

        id_personal_cargo = profesores_dict[
            profesor_var.get()
        ]

        cargar_tree(id_personal_cargo)

        resumen_inasistencias(id_personal_cargo)

        verificar_alertas(id_personal_cargo)

        # =====================================
        # CALCULAR DÍAS TRABAJADOS
        # =====================================

        laborales = contar_dias_laborales(
            id_personal_cargo
        )

        faltas = total_inasistencias(
            id_personal_cargo
        )

        trabajados = laborales - faltas

        porcentaje = round(
            (trabajados / laborales) * 100,
            2
        )

        lbl_trabajados.config(

            text=(
                f"Días laborales: {laborales} | "
                f"Trabajados: {trabajados} | "
                f"Presentismo: {porcentaje}%"
            )

        )
    # --------------------------------------------------------------

    # ==================  FUNCIÓN DE ALERTAS =======================
    def verificar_alertas(id_personal_cargo):

        conn = conectar()
        cursor = conn.cursor()

        # Obtener el profesor real
        cursor.execute("""
            SELECT id_profesor
            FROM personal_cargos
            WHERE id_personal_cargo=?
        """, (id_personal_cargo,))

        resultado = cursor.fetchone()

        if not resultado:
            conn.close()
            return

        id_profesor = resultado[0]

        # Buscar TODAS las inasistencias del docente
        cursor.execute("""
            SELECT
                a.estado,
                a.fecha_desde,
                a.fecha_hasta,
                a.id_personal_cargo
            FROM asistencias_docentes a
            JOIN personal_cargos pc
                ON a.id_personal_cargo = pc.id_personal_cargo
            WHERE pc.id_profesor = ?
        """, (id_profesor,))

        registros = cursor.fetchall()

        conn.close()

        licencia_medica = 0
        particular = 0

        dias_totales = set()

        for estado, desde, hasta, id_pc in registros:

            dias = calcular_dias(
                id_pc,
                desde,
                hasta
            )

            if estado == "Licencia Médica":
                licencia_medica += dias

            if estado == "Particular":
                particular += dias

            fecha_actual = datetime.strptime(
                desde,
                "%d/%m/%Y"
            )

            fecha_hasta = datetime.strptime(
                hasta,
                "%d/%m/%Y"
            )

            while fecha_actual <= fecha_hasta:

                dias_totales.add(
                    fecha_actual.strftime("%d/%m/%Y")
                )

                fecha_actual += timedelta(days=1)

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

        if len(dias_totales) > 5:

            alertas += (
                f"⚠ Necesita suplente ({len(dias_totales)} días)\n"
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
                "Seleccione un profesor", parent = ventana
            )

            return

        id_profesor = profesores_dict[profesor]

        mes_actual = datetime.now().month
        anio_actual = datetime.now().year

        conn = conectar()

        cursor = conn.cursor()

        cursor.execute("""

            SELECT

                a.id_personal_cargo,
                p.apenom,
                c.nombre_cargo,
                a.fecha_desde,
                a.fecha_hasta,
                a.estado

            FROM asistencias_docentes a

            JOIN personal_cargos pc
            ON a.id_personal_cargo = pc.id_personal_cargo

            JOIN profesores p
            ON pc.id_profesor = p.id_profesor

            JOIN cargos c
            ON pc.id_cargo = c.id_cargo

            WHERE a.id_personal_cargo = ?

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

        nombre_docente = f"{registros[0][1]} - {registros[0][2]}"

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
                fila[0],
                fila[3],
                fila[4]
            )

            total += dias

            data.append([

                fila[3],
                fila[4],
                str(dias),
                fila[5]

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

            f"Reporte generado:\n{ruta_pdf}", parent=ventana

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

                a.id_personal_cargo,
                p.apenom,
                c.nombre_cargo,
                a.fecha_desde,
                a.fecha_hasta,
                a.estado

            FROM asistencias_docentes a

            JOIN personal_cargos pc
            ON a.id_personal_cargo = pc.id_personal_cargo

            JOIN profesores p
            ON pc.id_profesor = p.id_profesor

            JOIN cargos c
            ON pc.id_cargo = c.id_cargo

            WHERE a.id_personal_cargo = ?

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
        nombre_docente = f"{registros[0][1]} - {registros[0][2]}"
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
                fila[3],
                "%d/%m/%Y"
            )

            mes = fecha.strftime("%B")

            dias = calcular_dias(
                fila[0],
                fila[3],
                fila[4]
            )

            total += dias

            estado = fila[5]

            if estado not in resumen_estados:

                resumen_estados[estado] = 0

            resumen_estados[estado] += dias

            data.append([
                mes,
                fila[3],
                fila[4],
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
            f"PDF anual generado:\n{ruta_pdf}", parent=ventana

        )
    # --------------------------------------------------------------

    # =====================  LIMPIAR ENTRYS ========================
    def limpiar():

        nonlocal id_seleccionado

        id_seleccionado = None

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
    # Botón Modificar
    ttk.Button(frame_btn, text="✏ Modificar", command=modificar).grid(row=0, column=1, padx=5)
    # Botón Eliminar
    ttk.Button(frame_btn, text="🗑 Eliminar", command=eliminar).grid(row=0, column=2, padx=5)
    # Botón Limpiar entrys
    ttk.Button(frame_btn, text="🧹 Limpiar", command=limpiar).grid(row=0, column=3, padx=5)
    # Botón Buscar Docente
    ttk.Button(frame_btn, text="🔍 Buscar Docente", command=buscar_docente).grid(row=0, column=4, padx=5)
    # Botón PDF mensual
    ttk.Button(frame_btn, text="📄 PDF Mensual", command=pdf_mensual).grid(row=0, column=5, padx=5)
    # Botón PDF anual
    ttk.Button(frame_btn, text="📘 PDF Anual", command=pdf_anual).grid(row=0, column=6, padx=5)
    # Botón Cerrar
    ttk.Button(frame_btn, text="❌ Cerrar", command=ventana.destroy).grid(row=0, column=7, padx=5)

    cargar_profesores()

    cargar_tree()

    centrar_ventana(ventana)
    crear_backup()