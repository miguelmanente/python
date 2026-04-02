# Función selecciona los gastos por categorias 
import pandas as pd
from tkinter import filedialog
from database import conectar
import os
from datetime import datetime
import sys


def gastos_por_categoria():
    cursor = conectar()
    cursor.execute("""
        SELECT categoria, SUM(monto)
        FROM gastos
        GROUP BY categoria
        ORDER BY SUM(monto) DESC
    """)
    datos = cursor.fetchall()
    conectar.close()

    # Agrupar categorías chicas
    resultado = []
    otros = 0

    for cat, monto in datos:
        if monto < 5000:   # podés cambiar este número
            otros += monto
        else:
            resultado.append((cat, monto))

    if otros > 0:
        resultado.append(("Otros", otros))

    return resultado

# Función que permite genera el reporte mensual con ingresos, gastos y balance
def generar_reporte():
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    
    reporte = tk.Toplevel()
    reporte.title("Reporte mensual")
    reporte.geometry("800x700")

    total_ingresos = obtener_total_ingresos()
    total_gastos = obtener_total_gastos()
    balance = total_ingresos - total_gastos

    tk.Label(reporte, text="REPORTE MENSUAL", font=("Arial", 14, "bold")).pack(pady=10)
    tk.Label(reporte, text=f"Ingresos: $ {total_ingresos:,.2f}").pack()
    tk.Label(reporte, text=f"Gastos: $ {total_gastos:,.2f}").pack()
    tk.Label(reporte, text=f"Balance: $ {balance:,.2f}").pack(pady=10)

    # ---- GRAFICO TORTA ----
    datos = gastos_por_categoria()
    categorias = [fila[0] for fila in datos]
    montos = [fila[1] for fila in datos]

    fig = Figure(figsize=(10, 10))
    ax = fig.add_subplot(111)

    ax.pie(
    montos,
    labels=categorias,
    autopct='%1.1f%%',
    startangle=90
    )
    ax.pie(
    montos,
    labels=categorias,
    autopct='%1.1f%%',
    startangle=90
)

    ax.axis('equal')  # hace el círculo perfecto
    ax.set_title("Gastos por categoría")

    canvas = FigureCanvasTkAgg(fig, master=reporte)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=10)

# Función para exportar el reporte mensual a Excel
def exportar_excel_pro(mes, anio):
    conn = conectar()

    mes = str(mes).zfill(2)
    anio = str(anio)

    # -------- RUTA BASE (sirve para exe también) --------
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    carpeta_reportes = os.path.join(base_dir, "reportes")

    if not os.path.exists(carpeta_reportes):
        os.makedirs(carpeta_reportes)

    # -------- GASTOS --------
    query_gastos = """
        SELECT fecha, descripcion, categoria, monto
        FROM gastos
        WHERE substr(fecha, 6, 2) = ?
        AND substr(fecha, 1, 4) = ?
    """
    df_gastos = pd.read_sql_query(query_gastos, conn, params=(mes, anio))

    # -------- INGRESOS --------
    query_ingresos = """
        SELECT fecha, descripcion, monto
        FROM ingresos
        WHERE substr(fecha, 6, 2) = ?
        AND substr(fecha, 1, 4) = ?
    """
    df_ingresos = pd.read_sql_query(query_ingresos, conn, params=(mes, anio))

    # -------- RESUMEN --------
    total_gastos = df_gastos["monto"].sum()
    total_ingresos = df_ingresos["monto"].sum()
    balance = total_ingresos - total_gastos

    df_resumen = pd.DataFrame({
        "Concepto": ["Total Ingresos", "Total Gastos", "Balance"],
        "Monto": [total_ingresos, total_gastos, balance]
    })

    # -------- GASTOS POR CATEGORIA --------
    query_cat = """
        SELECT categoria, SUM(monto) as total
        FROM gastos
        WHERE substr(fecha, 6, 2) = ?
        AND substr(fecha, 1, 4) = ?
        GROUP BY categoria
    """
    df_cat = pd.read_sql_query(query_cat, conn, params=(mes, anio))

    conn.close()

    # -------- NOMBRE AUTOMATICO --------
    fecha_archivo = datetime.now().strftime("%Y-%m-%d")
    archivo = os.path.join(carpeta_reportes, f"Reporte_{anio}_{mes}_{fecha_archivo}.xlsx")

    # -------- GUARDAR EXCEL --------
    with pd.ExcelWriter(archivo, engine="openpyxl") as writer:
        df_gastos.to_excel(writer, sheet_name="Gastos", index=False)
        df_ingresos.to_excel(writer, sheet_name="Ingresos", index=False)
        df_resumen.to_excel(writer, sheet_name="Resumen", index=False)
        df_cat.to_excel(writer, sheet_name="Gastos por Categoria", index=False)

    from tkinter import messagebox
    messagebox.showinfo("Reporte", f"Reporte guardado en:\n{archivo}")
