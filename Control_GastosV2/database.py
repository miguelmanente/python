import sqlite3

DB_NAME = "gastos.db"

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

def crear_tablas():
    
    id_gasto_seleccionado = None

    # Tabla categorias
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categorias  (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE
        )
    """)


    # Tabla ingresos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ingresos(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT,
            descripcion TEXT,
            monto REAL
        )
    """)

    # Tabla gastos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS gastos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT,
        descripcion TEXT,
        categoria TEXT,
        monto REAL
    )
    """)

    # Tabla configuracion mensual
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS configuracion_mensual (
        mes TEXT PRIMARY KEY,
        ingreso REAL,
        gastos_fijos REAL
    )
    """)

    conn.commit()

def obtener_categorias():
    conn = sqlite3.connect("gastos.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nombre FROM categorias ORDER BY nombre")
    return [fila[0] for fila in cursor.fetchall()]

def insertar_ingreso(fecha, descripcion, monto):
    conn = sqlite3.connect("gastos.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO ingresos (fecha, descripcion, monto) VALUES (?, ?, ?)",
        (fecha, descripcion, monto)
    )

    conn.commit()
    conn.close()


def obtener_ingresos():
    conn = sqlite3.connect("gastos.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM ingresos ORDER BY fecha DESC")
    datos = cursor.fetchall()

    conn.close()
    return datos

def total_gastos():
    conn = sqlite3.connect("gastos.db")
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(monto) FROM gastos")
    total = cursor.fetchone()[0]

    conn.close()

    if total is None:
        return 0

    return total

def total_ingresos():
    conn = sqlite3.connect("gastos.db")
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(monto) FROM ingresos")
    total = cursor.fetchone()[0]

    conn.close()

    if total is None:
        return 0

    return total

