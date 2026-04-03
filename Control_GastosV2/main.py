import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from database import conn
import pandas as pd
from tkinter import filedialog
from database import obtener_categorias
from database import crear_tablas, obtener_categorias
from categorias import abrir_ventana_categorias
from gastos import agregar_gasto, obtener_gastos, eliminar_gasto
from gastos import actualizar_gasto
from gastos import agregar_gasto, obtener_gastos
from ingresos import ventana_ingresos, total_ingresos, total_gastos
from estadisticas import abrir_estadisticas
from backup import hacer_backup
from database import total_ingresos_mes, total_gastos_mes
from gastos import limpiar_gastos_mes
from ingresos import ventana_ingresos, limpiar_ingresos_mes
from database import obtener_total_gastos_mes

id_gasto_seleccionado = None

# Da formato a las cifras numéricas con separadores de miles y decimales
def formatear_monto(valor):
    try:
        valor = float(valor)
        return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return valor

#  Salir de la aplicación
def salir():
    if messagebox.askyesno("Salir", "¿Desea cerrar la aplicación?"):
        ventana.destroy()

   
   
def obtener_ingresos_mes(mes, anio):
    conn = conectar()
    cursor = conn.cursor()

    mes = str(mes).zfill(2)
    anio = str(anio)

    cursor.execute("""
        SELECT id, fecha, descripcion, monto
        FROM ingresos
        WHERE substr(fecha, 6, 2)=?
        AND substr(fecha, 1, 4)=?
        ORDER BY fecha DESC
    """, (mes, anio))

    datos = cursor.fetchall()

    conn.close()
    return datos


def limpiar_mes_actual():
    respuesta = messagebox.askyesno(
        "Confirmar",
        "Se borrarán los ingresos del mes actual.\n¿Continuar?"
    )

    if not respuesta:
        return

    limpiar_ingresos_mes(mes_actual, anio_actual)

    cargar_ingresos_treeview(mes_actual, anio_actual)
    actualizar_resumen()

    messagebox.showinfo("OK", "Ingresos del mes eliminados")

def cargar_ingresos_treeview(mes_actual, anio_actual):

        for fila in tree.get_children():
            tree.delete(fila)

        ingresos = obtener_ingresos_mes(mes_actual, anio_actual)

        for ing in ingresos:
            tree.insert("", "end", values=ing)

def nuevo_mes_limpio():
    global mes_actual, anio_actual

    # Cambiar de mes
    if mes_actual == 12:
        mes_actual = 1
        anio_actual += 1
    else:
        mes_actual += 1

    # Limpiar datos del mes nuevo
    limpiar_ingresos_mes(mes_actual, anio_actual)
    limpiar_gastos_mes(mes_actual, anio_actual)

    # Recargar pantalla
    cargar_treeview(mes_actual, anio_actual)
    cargar_ingresos_treeview(mes_actual, anio_actual)
    actualizar_resumen()

    messagebox.showinfo("OK", "Ingresos del mes eliminados")

#Función que permite obtener el ingreso total mensual
def obtener_total_ingresos():
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(monto) FROM ingresos ")
    resultado = cursor.fetchone()[0]
    return resultado if resultado else 0

# Función que permite obtener el gasto total mensual
def obtener_total_gastos():
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(monto) FROM gastos ")
    resultado = cursor.fetchone()[0]
    return resultado if resultado else 0


# Función selecciona los gastos por categorias 
def gastos_por_categoria():
    cursor = conn.cursor()
    cursor.execute("""
        SELECT categoria, SUM(monto)
        FROM gastos
        GROUP BY categoria
        ORDER BY SUM(monto) DESC
    """)
    datos = cursor.fetchall()
    conn.close()

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


def gastos_por_categoria_mes(mes, anio):
    conn = conectar()
    cursor = conn.cursor()

    fecha_inicio = f"{anio}-{str(mes).zfill(2)}-01"

    if mes == 12:
        fecha_fin = f"{anio+1}-01-01"
    else:
        fecha_fin = f"{anio}-{str(mes+1).zfill(2)}-01"

    cursor.execute("""
        SELECT categoria, SUM(monto)
        FROM gastos
        WHERE fecha >= ? AND fecha < ?
        GROUP BY categoria
    """, (fecha_inicio, fecha_fin))

    datos = cursor.fetchall()
    conn.close()

    return datos



def obtener_total_ingresos_mes(mes, anio):
    conn = conectar()
    cursor = conn.cursor()

    fecha_inicio = f"{anio}-{str(mes).zfill(2)}-01"

    if mes == 12:
        fecha_fin = f"{anio+1}-01-01"
    else:
        fecha_fin = f"{anio}-{str(mes+1).zfill(2)}-01"

    cursor.execute("""
        SELECT SUM(monto)
        FROM ingresos
        WHERE fecha >= ? AND fecha < ?
    """, (fecha_inicio, fecha_fin))

    total = cursor.fetchone()[0]
    conn.close()

    return total if total else 0



# Función que permite genera el reporte mensual con ingresos, gastos y balance
def generar_reporte(mes, anio):
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import tkinter as tk

    reporte = tk.Toplevel()
    reporte.title("Reporte mensual")
    reporte.geometry("1000x700")

    total_ingresos = obtener_total_ingresos_mes(mes, anio)
    total_gastos = obtener_total_gastos_mes(mes, anio)
    balance = total_ingresos - total_gastos

    tk.Label(reporte, text="REPORTE MENSUAL", font=("Arial", 14, "bold")).pack(pady=10)
    tk.Label(reporte, text=f"Ingresos: $ {total_ingresos:,.2f}").pack()
    tk.Label(reporte, text=f"Gastos: $ {total_gastos:,.2f}").pack()
    tk.Label(reporte, text=f"Balance: $ {balance:,.2f}").pack(pady=10)

    # ---- GRAFICO TORTA ----
    datos = gastos_por_categoria_mes(mes, anio)

    categorias = [fila[0] for fila in datos]
    montos = [fila[1] for fila in datos]

    fig = Figure(figsize=(9, 6))
    ax = fig.add_subplot(111)

    ax.pie(
        montos,
        labels=categorias,
        autopct='%1.1f%%',
        startangle=90
    )

    ax.axis('equal')
    ax.set_title(f"Gastos por categoría {mes}/{anio}")

    canvas = FigureCanvasTkAgg(fig, master=reporte)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=10)


# Función para exportar el reporte mensual a Excel
import pandas as pd
from tkinter import filedialog
from database import conectar
import os
from datetime import datetime
import sys

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

# Función para hacer backup al cerrar la aplicación
def al_cerrar():
    hacer_backup()
    ventana.destroy()

    ventana.protocol("WM_DELETE_WINDOW", al_cerrar)


def cargar_categorias_filtro():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT nombre FROM categorias ORDER BY nombre")
    categorias = cursor.fetchall()
    conn.close()

    lista = ["Todas"]
    for cat in categorias:
        lista.append(cat[0])

    combo_categoria["values"] = lista
    combo_categoria.set("Todas")



def filtrar_por_categoria(event=None):
    categoria = combo_categoria.get()

    conn = conectar()
    cursor = conn.cursor()

    if categoria == "Todas":
        cursor.execute("""
            SELECT id, fecha, descripcion, categoria, monto
            FROM gastos
            ORDER BY fecha DESC
        """)
    else:
        cursor.execute("""
            SELECT id, fecha, descripcion, categoria, monto
            FROM gastos
            WHERE categoria = ?
            ORDER BY fecha DESC
        """, (categoria,))

    resultados = cursor.fetchall()
    conn.close()

    # Limpiar tabla
    for row in tree.get_children():
        tree.delete(row)

    # Cargar datos
    for fila in resultados:
        tree.insert("", "end", values=fila)

    combo_categoria.bind("<<ComboboxSelected>>", filtrar_por_categoria)
    #lbl_registros.config(text=f"Registros: {len(resultados)}")



from tkinter import messagebox
# Función para mostrar información sobre la aplicación
def acerca_de():
    messagebox.showinfo(
        "Acerca de",
        "Control de Gastos\n\n"
        "Versión 1.0\n"
        "Desarrollado por Miguel Manente\n"
        "Año 2026"
    )



#Ventana principal de la aplicación
ventana = tk.Tk()
ventana.title("Control de Gastos")
ventana.geometry("800x600")
ventana.minsize(700, 500)

# Menú superior
menu_bar = tk.Menu(ventana)
ventana.config(menu=menu_bar)


menu_archivo = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Archivo", menu=menu_archivo)

menu_archivo.add_command(label="Salir", command=salir)
ventana.config(menu=menu_bar)


menu_config = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Configuración", menu=menu_config)

menu_config.add_command(
    label="Administrar Categorías",
    command=lambda: abrir_ventana_categorias(ventana, combo_categoria)
)

menu_movimientos = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Movimientos", menu=menu_movimientos)

menu_movimientos.add_command(
    label="Ingresos",
    command=lambda: ventana_ingresos(mes_actual, anio_actual)
)

menu_analisis = tk.Menu(menu_bar, tearoff=0)

menu_bar.add_cascade(label="Análisis", menu=menu_analisis)

menu_analisis.add_command(
    label="Estadísticas",
    command=lambda: abrir_estadisticas(mes_actual, anio_actual)
)

menu_reportes = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Reportes", menu=menu_reportes)

#menu_reportes.add_command(label="Reporte mensual", command=generar_reporte)
menu_reportes.add_command(
    label="Reporte mensual",
    command=lambda: generar_reporte(mes_actual, anio_actual)
)

menu_reportes.add_command(
    label="Exportar reporte a Excel",
    command=lambda: exportar_excel_pro(mes_actual, anio_actual)
)


menu_archivo.add_command(label="Cambiar a mes siguiente", command=nuevo_mes_limpio)
menu_archivo.add_command(label="Limpiar ingresos del mes", command=limpiar_mes_actual)

menu_herramientas = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Herramientas", menu=menu_herramientas)



menu_herramientas.add_command(label="Crear backup", command=hacer_backup)


menu_ayuda = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Ayuda", menu=menu_ayuda)
menu_ayuda.add_command(label="Acerca de...", command=acerca_de)

# ----------- FORMULARIO GASTOS -----------
ventana.rowconfigure(0, weight=1)
#ventana.rowconfigure(1, weight=0)
ventana.columnconfigure(0, weight=1)


frame_principal = tk.Frame(ventana)
frame_principal.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

frame_principal.columnconfigure(1, weight=1)
#frame_principal.columnconfigure(1, weight=2)
frame_principal.rowconfigure(0, weight=1)


# sigue el formulario y el treeview debajo del selector de mes
frame_form = tk.Frame(frame_principal)
frame_form.grid(row=0, column=0, sticky="nsew", padx=10)

# Configurar expansión treeview a la derecha
frame_tabla = tk.Frame(frame_principal)
frame_tabla.grid(row=0, column=1, sticky="nsew", padx=10)

frame_tabla.rowconfigure(1, weight=1)
frame_tabla.columnconfigure(0, weight=1)

frame_filtros = tk.Frame(frame_tabla)
frame_filtros.grid(row=0, column=0, sticky="ew")
frame_tabla.grid_columnconfigure(0, weight=1)

lbl_filtro = tk.Label(frame_filtros, text="Categoría:")
lbl_filtro.grid(row=0, column=0, padx=5, pady=5, sticky="w")

btn_ver_todo = tk.Button(frame_filtros, text="Ver todo", command=filtrar_por_categoria)
btn_ver_todo.grid(row=0, column=2, padx=5, pady=5, sticky="w")

combo_categoria = ttk.Combobox(frame_filtros, state="readonly", width=20)
combo_categoria.grid(row=0, column=1, padx=5, pady=5, sticky="w")

lbl_registros = tk.Label(frame_filtros, text="Registros: 0")
lbl_registros.grid(row=0, column=3, padx=10)

frame_resumen = tk.LabelFrame(frame_tabla, text="Resumen financiero")
frame_resumen.grid(row=2, column=0, sticky="ew", pady=10)

tk.Label(frame_resumen, text="Ingresos del mes").grid(row=6, column=0, sticky="w")
#lbl_ingresos = tk.Label(frame_resumen, text="$ 0", font=("Arial", 11, "bold"))
lbl_ingresos = tk.Label(frame_resumen, text="$ 0", font=("Arial", 11, "bold"), anchor="e")
lbl_ingresos.grid(row=6, column=1, sticky="e")

tk.Label(frame_resumen, text="Gastos del mes").grid(row=7, column=0, sticky="w")
#lbl_gastos = tk.Label(frame_resumen, text="$ 0", font=("Arial", 11, "bold"))
lbl_gastos = tk.Label(frame_resumen, text="$ 0", font=("Arial", 11, "bold"), anchor="e")
lbl_gastos.grid(row=7, column=1, sticky="e")

tk.Label(frame_resumen, text="Saldo disponible").grid(row=8, column=0, sticky="w")
#lbl_saldo = tk.Label(frame_resumen, text="$ 0", font=("Arial", 13, "bold"))
lbl_saldo = tk.Label(frame_resumen, text="$ 0", font=("Arial", 13, "bold"), anchor="e")
lbl_saldo.grid(row=8, column=1, sticky="e")

#Treeview para mostrar gastos
tree = ttk.Treeview(
    frame_tabla,
    columns=("id","fecha", "descripcion", "categoria", "monto"),
    show="headings"
)

tree.heading("fecha", text="Fecha")
tree.heading("descripcion", text="Descripción")
tree.heading("categoria", text="Categoría")
tree.heading("monto", text="Monto")

tree.column("fecha", width=80)
tree.column("descripcion", width=150)
tree.column("categoria", width=100)
tree.column("monto", width=80, anchor="e")  # alineado derecha
tree.column("id", width=0, stretch=False)

#Scrollbar para el treeview
scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)

scrollbar.grid(row=1, column=1, sticky="ns")

tree.grid(row=1, column=0, sticky="nsew")
frame_form.columnconfigure(0, weight=1)




# Selector de mes y año
from datetime import datetime
import calendar

tk.Label(frame_form, text="Mes:").grid(row=0, column=0, padx=5, sticky="e")

mes_var = tk.StringVar()

combo_mes = ttk.Combobox(frame_form, textvariable=mes_var, state="readonly")

anio_actual = datetime.now().year
mes_actual = datetime.now().month

meses = [f"{calendar.month_name[i]} {anio_actual}" for i in range(1, 13)]

combo_mes["values"] = meses
combo_mes.current(mes_actual - 1)

combo_mes.grid(row=0, column=1, padx=5, sticky="w")


def cargar_categorias_filtro():
    categorias = obtener_categorias()
    combo_categoria["values"] = ["Todas"] + categorias
    combo_categoria.set("Todas")

cargar_categorias_filtro()

# btn_filtrar = tk.Button(frame_filtros, text="Filtrar", command=filtrar_por_categoria)
# btn_filtrar.grid(row=0, column=3, padx=5)


def reset_filtro():
    combo_categoria.set("Todas")
    filtrar_por_categoria()

btn_reset = tk.Button(frame_filtros, text="Resetear Gastos", command=reset_filtro)
btn_reset.grid(row=0, column=3, padx=5)

# Función para cargar gastos al cambiar el mes
def cambiar_mes(event):

    seleccion = combo_mes.get()

    nombre_mes = seleccion.split()[0]

    numero_mes = list(calendar.month_name).index(nombre_mes)

    cargar_treeview(numero_mes, anio_actual)


# Campos del formulario
tk.Label(frame_form, text="Fecha").grid(row=4, column=0, sticky="w", pady=8)
entry_fecha = tk.Entry(frame_form)
entry_fecha.grid(row=4, column=1, sticky="ew", pady=8)

tk.Label(frame_form, text="Descripción").grid(row=5, column=0, sticky="w", pady=8)
entry_descripcion = tk.Entry(frame_form)
entry_descripcion.grid(row=5, column=1, sticky="ew", pady=8)

# Configurar expansión
frame_form.columnconfigure(1, weight=1)

# Categoría
tk.Label(frame_form, text="Categoría").grid(row=6, column=0, sticky="w", pady=8)

combo_categoria = ttk.Combobox(frame_form, state="readonly")
combo_categoria.grid(row=6, column=1, sticky="ew", pady=8)

combo_categoria["values"] = obtener_categorias()

tk.Label(frame_form, text="Monto").grid(row=7, column=0, sticky="w", pady=8)
entry_monto = tk.Entry(frame_form)
entry_monto.grid(row=7, column=1, sticky="ew", pady=8)

#print("Total gastos:", calcular_total_gastos())

# def cargar_treeview(mes_actual, anio_actual):

#     for fila in tree.get_children():
#         tree.delete(fila)

#     for gasto in obtener_gastos():

#         id_gasto, fecha, descripcion, categoria, monto = gasto

#         tree.insert(
#             "",
#             "end",
#             values=(id_gasto, fecha, descripcion, categoria, formatear_monto(monto))
 #       )

def cargar_treeview(mes, anio):

    for fila in tree.get_children():
        tree.delete(fila)

    conn = conectar()
    cursor = conn.cursor()

    mes = str(mes).zfill(2)
    anio = str(anio)

    cursor.execute("""
        SELECT id, fecha, descripcion, categoria, monto
        FROM gastos
        WHERE substr(fecha, 6, 2) = ?
        AND substr(fecha, 1, 4) = ?
        ORDER BY fecha DESC
    """, (mes, anio))

    resultados = cursor.fetchall()
    conn.close()

    for fila in resultados:
        tree.insert("", "end", values=fila)




from gastos import agregar_gasto, calcular_total_gastos

def agregar():
    try:
        fecha = entry_fecha.get()
        descripcion = entry_descripcion.get()
        categoria = combo_categoria.get()
        monto = float(entry_monto.get())

        agregar_gasto(fecha, descripcion, categoria, monto)

        cargar_treeview(mes_actual, anio_actual)

        actualizar_resumen()

        entry_descripcion.delete(0, tk.END)
        entry_monto.delete(0, tk.END)

    except ValueError:
        messagebox.showerror("Error", "Monto inválido")

    except ValueError:
        messagebox.showerror("Error", "Monto inválido")

tk.Button(frame_form, text="Agregar Gasto", command=agregar)\
    .grid(row=8, column=0, columnspan=2, pady=20)

# def seleccionar_gasto(event):

#     global id_gasto_seleccionado

#     item = tree.selection()

#     if not item:
#         return

#     valores = tree.item(item[0], "values")

#     id_gasto_seleccionado = valores[0]

#     entry_fecha.delete(0, tk.END)
#     entry_fecha.insert(0, valores[0])

#     entry_descripcion.delete(0, tk.END)
#     entry_descripcion.insert(0, valores[1])

#     combo_categoria.set(valores[2])

#     entry_monto.delete(0, tk.END)
#     entry_monto.insert(0, valores[3].replace(".", "").replace(",", "."))

def seleccionar_gasto(event):
    global id_gasto_seleccionado

    item = tree.focus()
    if not item:
        return

    valores = tree.item(item, "values")
    if not valores:
        return

    id_gasto_seleccionado = valores[0]  # ← GUARDAMOS EL ID

    entry_fecha.delete(0, tk.END)
    entry_fecha.insert(0, valores[1])

    entry_descripcion.delete(0, tk.END)
    entry_descripcion.insert(0, valores[2])

    combo_categoria.set(valores[3])

    entry_monto.delete(0, tk.END)
    entry_monto.insert(0, valores[4])

tree.bind("<<TreeviewSelect>>", seleccionar_gasto)


def actualizar_resumen():

    ingresos = total_ingresos_mes(mes_actual, anio_actual)
    gastos = total_gastos_mes(mes_actual, anio_actual)
    saldo = ingresos - gastos

    lbl_ingresos.config(text=f"$ {formatear_monto(ingresos)}")
    lbl_gastos.config(text=f"$ {formatear_monto(gastos)}")
    lbl_saldo.config(text=f"$ {formatear_monto(saldo)}")

      # Colores automáticos del saldo
    if saldo > 0:
        lbl_saldo.config(fg="green")
    elif saldo < 0:
        lbl_saldo.config(fg="red")
    else:
        lbl_saldo.config(fg="black")

    cargar_treeview(mes_actual, anio_actual)


def eliminar():

    seleccion = tree.selection()

    if not seleccion:
        messagebox.showwarning("Aviso", "Seleccione un gasto")
        return

    item = seleccion[0]

    valores = tree.item(item, "values")

    id_gasto = valores[0]

    respuesta = messagebox.askyesno(
        "Eliminar",
        "¿Desea eliminar el gasto seleccionado?"
    )

    if respuesta:

        eliminar_gasto(id_gasto)

        cargar_treeview(mes_actual, anio_actual)

        actualizar_resumen()

tk.Button(frame_form, text="Eliminar", command=eliminar).grid(row=9, column=0, columnspan=2, pady=5)

# def actualizar():

#     global id_gasto_seleccionado

#     if id_gasto_seleccionado is None:
#         messagebox.showwarning("Aviso", "Seleccione un gasto")
#         return

#     try:

#         fecha = entry_fecha.get()
#         descripcion = entry_descripcion.get()
#         categoria = combo_categoria.get()
#         monto = float(entry_monto.get())

#         actualizar_gasto(
#             id_gasto_seleccionado,
#             fecha,
#             descripcion,
#             categoria,
#             monto
#         )

#         cargar_treeview(mes_actual, anio_actual)
#         actualizar_resumen()

#         entry_descripcion.delete(0, tk.END)
#         entry_monto.delete(0, tk.END)

#         id_gasto_seleccionado = None

#     except ValueError:
#         messagebox.showerror("Error", "Monto inválido")

def actualizar():
    global id_gasto_seleccionado

    if id_gasto_seleccionado is None:
        messagebox.showwarning("Atención", "Seleccione un gasto")
        return

    fecha = entry_fecha.get()
    descripcion = entry_descripcion.get()
    categoria = combo_categoria.get()
    monto = entry_monto.get()

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE gastos
        SET fecha=?, descripcion=?, categoria=?, monto=?
        WHERE id=?
    """, (fecha, descripcion, categoria, monto, id_gasto_seleccionado))

    
    conn.commit()
    conn.close()

    messagebox.showinfo("OK", "Gasto actualizado")
cargar_treeview(mes_actual, anio_actual)
actualizar_resumen()

tk.Button(frame_form, text="Actualizar", command=actualizar).grid(row=10, column=0, columnspan=2, pady=5)


# Footer con logo y texto
logo = tk.PhotoImage(file="logo_mam.png")

# achicar el logo (2 = mitad, 3 = un tercio, etc.)
logo = logo.subsample(2, 2)

frame_footer = tk.Frame(ventana)
frame_footer.grid(row=1, column=0, sticky="sw", padx=10, pady=5)

lbl_logo = tk.Label(frame_footer, image=logo)
lbl_logo.pack(anchor="w")

lbl_texto = tk.Label(
    frame_footer,
    text="© 2026 Miguel Manente",
    font=("Arial", 8),
    fg="gray"
)
lbl_texto.pack(anchor="w")

lbl_logo.image = logo

# Cargar gastos al iniciar la aplicación
cargar_treeview(mes_actual, anio_actual)
actualizar_resumen()
cargar_categorias_filtro()

ventana.mainloop()