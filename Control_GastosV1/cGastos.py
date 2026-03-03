import tkinter as tk
from tkinter import ttk
import sqlite3
from datetime import datetime

def formatear_moneda(valor):
    return "{:,.2f}".format(valor).replace(",", "X").replace(".", ",").replace("X", ".")

def formatear_entry(entry):
    try:
        valor = float(entry.get().replace(".", "").replace(",", "."))
        entry.delete(0, tk.END)
        entry.insert(0, formatear_moneda(valor))
    except:
        pass

def obtener_valor(entry):
    try:
        return float(entry.get().replace(".", "").replace(",", "."))
    except:
        return 0

# =========================
# CREAR BASE DE DATOS
# =========================
def crear_bd():
    conexion = sqlite3.connect("gastos.db")
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS gastos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT,
            categoria TEXT,
            monto REAL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS configuracion_mensual (
            mes INTEGER,
            anio INTEGER,
            ingreso REAL,
            gastos_fijos REAL,
            PRIMARY KEY (mes, anio)
        )
    """)
    
    cargar_configuracion_mes()
    conexion.commit()
    conexion.close()

#==============================
# Cargar configuración mensual
#==============================
def cargar_configuracion_mes():
    mes = datetime.now().month
    anio = datetime.now().year

    conexion = sqlite3.connect("gastos.db")
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT ingreso, gastos_fijos 
        FROM configuracion_mensual 
        WHERE mes=? AND anio=?
    """, (mes, anio))

    datos = cursor.fetchone()
    conexion.close()

    if datos:
        ingreso, gastos_fijos = datos

        entry_ingreso.delete(0, tk.END)
        entry_ingreso.insert(0, formatear_moneda(ingreso))

        entry_gastos_fijos.delete(0, tk.END)
        entry_gastos_fijos.insert(0, formatear_moneda(gastos_fijos))

        calcular_gasto_total()
        calcular_saldo()

#==============================
# Guardar configuración mensual
#==============================
def guardar_configuracion_mes():
    mes = datetime.now().month
    anio = datetime.now().year

    # try:
    #     ingreso = float(entry_ingreso.get())
    # except ValueError:
    #     ingreso = 0

    # try:
    #     gastos_fijos = float(entry_gastos_fijos.get())
    # except ValueError:
    #     gastos_fijos = 0
    ingreso = obtener_valor(entry_ingreso)
    gastos_fijos = obtener_valor(entry_gastos_fijos)
    
    conexion = sqlite3.connect("gastos.db")
    cursor = conexion.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO configuracion_mensual
        (mes, anio, ingreso, gastos_fijos)
        VALUES (?, ?, ?, ?)
    """, (mes, anio, ingreso, gastos_fijos))

    conexion.commit()
    conexion.close()


# =========================
# MOSTRAR GASTOS
# =========================
def mostrar_gastos():
    for item in tree.get_children():
        tree.delete(item)

    conexion = sqlite3.connect("gastos.db")
    cursor = conexion.cursor()

    cursor.execute("SELECT fecha, categoria, monto FROM gastos")
    datos = cursor.fetchall()

    for fila in datos:
        fecha, categoria, monto = fila
        monto_formateado = formatear_moneda(monto)
        tree.insert("", tk.END, values=(fecha, categoria, monto_formateado))

    conexion.close()


# =========================
# CARGAR CATEGORIAS
# =========================
def cargar_categorias():
    categorias = []
    try:
        with open("categorias.txt", "r", encoding="utf-8") as archivo:
            for linea in archivo:
                categorias.append(linea.strip())
    except FileNotFoundError:
        print("No se encontró el archivo categorias.txt")
    return categorias

# =========================
# GASTOS DEL DIA
# =========================
def calcular_total_dia():
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")

    conexion = sqlite3.connect("gastos.db")
    cursor = conexion.cursor()

    cursor.execute("SELECT SUM(monto) FROM gastos WHERE fecha = ?", (fecha_hoy,))
    total = cursor.fetchone()[0]

    conexion.close()

    if total is None:
        total = 0

    entry_total_dia.config(state="normal")
    entry_total_dia.delete(0, tk.END)
    #entry_total_dia.insert(0, f"{total:.2f}")
    entry_total_dia.insert(0, formatear_moneda(total))
    entry_total_dia.config(state="readonly")
    calcular_gasto_total()

# =========================
# GASTOS DEL MES
# =========================
def calcular_total_mes():

    mes = datetime.now().month
    anio = datetime.now().year

    conexion = sqlite3.connect("gastos.db")
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT SUM(monto) FROM gastos
        WHERE strftime('%m', fecha) = ?
        AND strftime('%Y', fecha) = ?
    """, (f"{mes:02d}", str(anio)))

    total = cursor.fetchone()[0]
    conexion.close()

    if total is None:
        total = 0

    return total

# =========================
# CALCULAR GASTOS TOTALES
# =========================
def calcular_gasto_total():

    gastos_fijos = obtener_valor(entry_gastos_fijos)
    total_mes = calcular_total_mes()

    total = gastos_fijos + total_mes

    entry_gasto_total.config(state="normal")
    entry_gasto_total.delete(0, tk.END)
    entry_gasto_total.insert(0, formatear_moneda(total))
    entry_gasto_total.config(state="readonly")

    calcular_saldo()

# =========================
# CALCULAR SALDO DISPONIBLE
# =========================
def calcular_saldo():
    try:
        #ingreso = float(entry_ingreso.get())
        ingreso = obtener_valor(entry_ingreso)

    except ValueError:
        ingreso = 0

    try:
        #gasto_total = float(entry_gasto_total.get())
        gasto_total = obtener_valor(entry_gasto_total)
    except ValueError:
        gasto_total = 0

    saldo = ingreso - gasto_total

    entry_saldo.config(state="normal")
    entry_saldo.delete(0, tk.END)
    #entry_saldo.insert(0, f"{saldo:.2f}")
    entry_saldo.insert(0, formatear_moneda(saldo))
    entry_saldo.config(state="readonly")

# =========================
# GUARDAR GASTO
# =========================
def guardar_gasto():
    categoria = combo_categoria.get()
    monto = entry_monto.get()

    if not monto:
        return

    try:
        monto = float(monto)
    except ValueError:
        return

    fecha = datetime.now().strftime("%Y-%m-%d")

    conexion = sqlite3.connect("gastos.db")
    cursor = conexion.cursor()

    cursor.execute("INSERT INTO gastos (fecha, categoria, monto) VALUES (?, ?, ?)",
                   (fecha, categoria, monto))

    conexion.commit()
    conexion.close()

    entry_monto.delete(0, tk.END)
    mostrar_gastos()
    calcular_total_dia()
    calcular_gasto_total()


  


# =========================
# VENTANA
# =========================
ventana = tk.Tk()
ventana.title("Control de Gastos")
ventana.geometry("900x600")

ventana.columnconfigure(0, weight=1)
ventana.rowconfigure(1, weight=1)

frame = tk.Frame(ventana)
frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=2)

# Categoría
lbl_categoria = tk.Label(frame, text="Categoría:")
lbl_categoria.grid(row=0, column=0, padx=10, pady=10, sticky="e")

combo_categoria = ttk.Combobox(frame, state="readonly", width=30)
combo_categoria.grid(row=0, column=1, padx=10, pady=10, sticky="w")

combo_categoria["values"] = cargar_categorias()

if combo_categoria["values"]:
    combo_categoria.current(0)

# Monto
lbl_monto = tk.Label(frame, text="Monto Gastado:")
lbl_monto.grid(row=1, column=0, padx=10, pady=10, sticky="e")

entry_monto = tk.Entry(frame, width=32)
entry_monto.grid(row=1, column=1, padx=10, pady=10, sticky="w")

# Botón Guardar
btn_guardar = tk.Button(frame, text="Guardar Gasto", command=guardar_gasto)
btn_guardar.grid(row=2, column=1, padx=10, pady=20, sticky="w")

# =========================
# TOTAL DEL DIA
# =========================
lbl_total_dia = tk.Label(frame, text="Total de todos los Días:")
lbl_total_dia.grid(row=3, column=0, padx=10, pady=10, sticky="e")

entry_total_dia = tk.Entry(frame, width=32, state="readonly")
entry_total_dia.grid(row=3, column=1, padx=10, pady=10, sticky="w")

# =========================
# GASTOS FIJOS
# =========================
lbl_gastos_fijos = tk.Label(frame, text="Gastos Fijos:")
lbl_gastos_fijos.grid(row=4, column=0, padx=10, pady=10, sticky="e")

entry_gastos_fijos = tk.Entry(frame, width=32)
entry_gastos_fijos.grid(row=4, column=1, padx=10, pady=10, sticky="w")
#entry_gastos_fijos.bind("<KeyRelease>", lambda e: calcular_gasto_total())
entry_gastos_fijos.bind(
    "<KeyRelease>", 
    lambda e: (guardar_configuracion_mes(), calcular_gasto_total())
)

entry_gastos_fijos.bind("<FocusOut>", lambda e: formatear_entry(entry_gastos_fijos))


# =========================
# GASTO TOTAL
# =========================
lbl_gasto_total = tk.Label(frame, text="Gasto Total:")
lbl_gasto_total.grid(row=5, column=0, padx=10, pady=10, sticky="e")

entry_gasto_total = tk.Entry(frame, width=32, state="readonly")
entry_gasto_total.grid(row=5, column=1, padx=10, pady=10, sticky="w")

# =========================
# INGRESO MENSUAL
# =========================
lbl_ingreso = tk.Label(frame, text="Ingreso Mensual:")
lbl_ingreso.grid(row=6, column=0, padx=10, pady=10, sticky="e")

entry_ingreso = tk.Entry(frame, width=32)
entry_ingreso.grid(row=6, column=1, padx=10, pady=10, sticky="w")
#entry_ingreso.bind("<KeyRelease>", lambda e: calcular_saldo())
entry_ingreso.bind(
    "<KeyRelease>", 
    lambda e: (guardar_configuracion_mes(), calcular_saldo()))
entry_ingreso.bind("<FocusOut>", lambda e: formatear_entry(entry_ingreso))

# =========================
# SALDO DISPONIBLE
# =========================
lbl_saldo = tk.Label(frame, text="Saldo Disponible:")
lbl_saldo.grid(row=7, column=0, padx=10, pady=10, sticky="e")

entry_saldo = tk.Entry(frame, width=32, state="readonly")
entry_saldo.grid(row=7, column=1, padx=10, pady=10, sticky="w")

# =========================
# TREEVIEW
# =========================
frame_tabla = tk.Frame(ventana)
frame_tabla.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)

frame_tabla.columnconfigure(0, weight=1)
frame_tabla.rowconfigure(0, weight=1)

tree = ttk.Treeview(frame_tabla, columns=("Fecha", "Categoria", "Monto"), show="headings")
tree.grid(row=0, column=0, sticky="nsew")

tree.heading("Fecha", text="Fecha")
tree.heading("Categoria", text="Categoría")
tree.heading("Monto", text="Monto")
tree.column("Fecha", anchor="center", width=100)
tree.column("Categoria", anchor="w", width=200)
tree.column("Monto", anchor="e", width=120)

scroll = ttk.Scrollbar(frame_tabla, orient="vertical", command=tree.yview)
scroll.grid(row=0, column=1, sticky="ns")

tree.configure(yscrollcommand=scroll.set)

# =========================
# INICIAR
# =========================
crear_bd()
mostrar_gastos()

ventana.mainloop()