import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from database import conectar, obtener_categorias, crear_tablas, total_ingresos, total_gastos
from gastos import agregar_gasto, obtener_gastos, eliminar_gasto, actualizar_gasto
from ingresos import ventana_ingresos
from categorias import abrir_ventana_categorias
#from estadisticas import abrir_estadisticas
from backup import hacer_backup
import os
import sys
import calendar
from datetime import datetime
#import pandas as pd

id_gasto_seleccionado = None

# Da formato a las cifras numéricas con separadores de miles y decimales
def formatear_monto(valor):
    try:
        valor = float(valor)
        return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return valor

def limpiar_campos():
    entry_fecha.delete(0, tk.END)
    entry_descripcion.delete(0, tk.END)
    entry_monto.delete(0, tk.END)
    combo_categoria.set("")

#  Salir de la aplicación
def salir():
    if messagebox.askyesno("Salir", "¿Desea cerrar la aplicación?"):
        ventana.destroy()

#Función que permite obtener el ingreso total mensual
def obtener_total_ingresos():
    cursor = conectar.cursor()
    cursor.execute("SELECT SUM(monto) FROM ingresos ")
    resultado = cursor.fetchone()[0]
    return resultado if resultado else 0

# Función que permite obtener el gasto total mensual
def obtener_total_gastos():
    cursor = conectar.cursor()
    cursor.execute("SELECT SUM(monto) FROM gastos ")
    resultado = cursor.fetchone()[0]
    return resultado if resultado else 0



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
    command=ventana_ingresos
)

menu_analisis = tk.Menu(menu_bar, tearoff=0)

menu_bar.add_cascade(label="Análisis", menu=menu_analisis)

# menu_analisis.add_command(
#     label="Estadísticas",
#     command=lambda: abrir_estadisticas(mes_actual, anio_actual)
#)

menu_reportes = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Reportes", menu=menu_reportes)

# menu_reportes.add_command(label="Reporte mensual", command=generar_reporte)
# menu_reportes.add_command(
#     label="Exportar reporte a Excel",
#     command=lambda: exportar_excel_pro(mes_actual, anio_actual)
# )

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

combo_categoria_filtro = ttk.Combobox(frame_filtros, state="readonly", width=20)
combo_categoria_filtro.grid(row=0, column=1, padx=5, pady=5, sticky="w")

lbl_filtro = tk.Label(frame_filtros, text="Categoría:")
lbl_filtro.grid(row=0, column=0, padx=5, pady=5, sticky="w")

btn_ver_todo = tk.Button(frame_filtros, text="Ver todo", command=filtrar_por_categoria)
btn_ver_todo.grid(row=0, column=2, padx=5, pady=5, sticky="w")

combo_categoria = ttk.Combobox(frame_filtros, state="readonly", width=20)
combo_categoria.grid(row=0, column=1, padx=5, pady=5, sticky="w")
combo_categoria_form = ttk.Combobox(frame_form, state="readonly")
combo_categoria_form.grid(row=6, column=1, sticky="ew", pady=8)
combo_categoria_form["values"] = obtener_categorias()

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

    global mes_actual, anio_actual

    seleccion = combo_mes.get()
    nombre_mes = seleccion.split()[0]
    anio_actual = int(seleccion.split()[1])

    numero_mes = list(calendar.month_name).index(nombre_mes)
    mes_actual = numero_mes

    cargar_treeview(mes_actual, anio_actual)
    actualizar_resumen()


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

#Treeview de gastos
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
        id_gasto, fecha, descripcion, categoria, monto = fila
        tree.insert(
            "",
            "end",
            values=(id_gasto, fecha, descripcion, categoria, formatear_monto(monto))
        )

    lbl_registros.config(text=f"Registros: {len(resultados)}")

def agregar():
    try:
        fecha = entry_fecha.get()
        descripcion = entry_descripcion.get()
        categoria = combo_categoria.get()
        monto = float(entry_monto.get())

        agregar_gasto(fecha, descripcion, categoria, monto)

        limpiar_campos()
        cargar_treeview(mes_actual, anio_actual)
        actualizar_resumen()

    except ValueError:
        messagebox.showerror("Error", "Monto inválido")

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

    conn = conectar()
    cursor = conn.cursor()

    mes = str(mes_actual).zfill(2)
    anio = str(anio_actual)

    # Total ingresos del mes
    cursor.execute("""
        SELECT SUM(monto)
        FROM ingresos
        WHERE substr(fecha, 6, 2) = ?
        AND substr(fecha, 1, 4) = ?
    """, (mes, anio))
    ingresos = cursor.fetchone()[0] or 0

    # Total gastos del mes
    cursor.execute("""
        SELECT SUM(monto)
        FROM gastos
        WHERE substr(fecha, 6, 2) = ?
        AND substr(fecha, 1, 4) = ?
    """, (mes, anio))
    gastos = cursor.fetchone()[0] or 0

    conn.close()

    saldo = ingresos - gastos

    lbl_ingresos.config(text=f"$ {formatear_monto(ingresos)}")
    lbl_gastos.config(text=f"$ {formatear_monto(gastos)}")
    lbl_saldo.config(text=f"$ {formatear_monto(saldo)}")

    if saldo > 0:
        lbl_saldo.config(fg="green")
    elif saldo < 0:
        lbl_saldo.config(fg="red")
    else:
        lbl_saldo.config(fg="black")

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
        limpiar_campos()



def actualizar():
    global id_gasto_seleccionado

    if id_gasto_seleccionado is None:
        messagebox.showwarning("Atención", "Seleccione un gasto")
        return

    try:
        fecha = entry_fecha.get()
        descripcion = entry_descripcion.get()
        categoria = combo_categoria.get()
        monto = float(entry_monto.get())

        actualizar_gasto(
            id_gasto_seleccionado,
            fecha,
            descripcion,
            categoria,
            monto
        )

        limpiar_campos()
        cargar_treeview(mes_actual, anio_actual)
        actualizar_resumen()

        id_gasto_seleccionado = None

        messagebox.showinfo("OK", "Gasto actualizado")

    except ValueError:
        messagebox.showerror("Error", "Monto inválido")

tk.Button(frame_form, text="Agregar Gastos", command=agregar).grid(row=8, column=0, columnspan=2, pady=5)
tk.Button(frame_form, text="Eliminar", command=eliminar).grid(row=9, column=0, columnspan=2, pady=5)
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