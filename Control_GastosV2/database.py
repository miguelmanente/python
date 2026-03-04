import sqlite3

DB_NAME = "gastos.db"

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

def crear_tablas():

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

    # Tabla categorias
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT UNIQUE NOT NULL
    )
    """)

    conn.commit()

def obtener_categorias():
    cursor.execute("SELECT nombre FROM categorias ORDER BY nombre")
    return [fila[0] for fila in cursor.fetchall()]