import sqlite3
import os
import sys

DB_NAME = "gastos.db"

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

def obtener_ruta_db():
    if getattr(sys, 'frozen', False):
        # Si está compilado con PyInstaller
        base_path = os.path.dirname(sys.executable)
    else:
        # Si estás en modo desarrollo
        base_path = os.path.dirname(__file__)

    return os.path.join(base_path, "gastos.db")


def conectar():
    ruta_db = obtener_ruta_db()
    conn = sqlite3.connect(ruta_db)
    return conn


#Se crea la base de datos y las tablas necesarias para la aplicación
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

# Función para insertar una nueva categoría
def obtener_categorias():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT nombre FROM categorias ORDER BY nombre")
    categorias = [fila[0] for fila in cursor.fetchall()]

    conn.close()
    return categorias

# Función para insertar una nueva categoría
def insertar_ingreso(fecha, descripcion, monto):
    conn = sqlite3.connect("gastos.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO ingresos (fecha, descripcion, monto) VALUES (?, ?, ?)",
        (fecha, descripcion, monto)
    )

    conn.commit()
    conn.close()

# Función para obtener los ingresos registrados
def obtener_ingresos():
    conn = sqlite3.connect("gastos.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM ingresos ORDER BY fecha DESC")
    datos = cursor.fetchall()

    conn.close()
    return datos

# Función para insertar un nuevo gasto
def total_gastos():
    conn = sqlite3.connect("gastos.db")
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(monto) FROM gastos")
    total = cursor.fetchone()[0]

    conn.close()

    if total is None:
        return 0

    return total

# Función para obtener el total de ingresos registrados
def total_ingresos():
    conn = sqlite3.connect("gastos.db")
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(monto) FROM ingresos")
    total = cursor.fetchone()[0]

    conn.close()

    if total is None:
        return 0

    return total

