import sqlite3
import os
import sys


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


def crear_tablas():
    conn = conectar()
    cursor = conn.cursor()

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
    conn.close()


# ---------------- INGRESOS ----------------

def insertar_ingreso(fecha, descripcion, monto):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO ingresos (fecha, descripcion, monto) VALUES (?, ?, ?)",
        (fecha, descripcion, monto)
    )

    conn.commit()
    conn.close()


def obtener_ingresos():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM ingresos ORDER BY fecha DESC")
    datos = cursor.fetchall()

    conn.close()
    return datos


def total_ingresos():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(monto) FROM ingresos")
    total = cursor.fetchone()[0]

    conn.close()

    if total is None:
        return 0

    return total


# ---------------- GASTOS ----------------

def total_gastos():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(monto) FROM gastos")
    total = cursor.fetchone()[0]

    conn.close()

    if total is None:
        return 0

    return total


# ---------------- CATEGORIAS ----------------

def obtener_categorias():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT nombre FROM categorias ORDER BY nombre")
    categorias = [fila[0] for fila in cursor.fetchall()]

    conn.close()
    return categorias

def eliminar_ingreso(id_ingreso):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM ingresos WHERE id=?", (id_ingreso,))

    conn.commit()
    conn.close()


def actualizar_ingreso(id_ingreso, fecha, descripcion, monto):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE ingresos
        SET fecha=?, descripcion=?, monto=?
        WHERE id=?
    """, (fecha, descripcion, monto, id_ingreso))

    conn.commit()
    conn.close()


def obtener_ingresos():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, fecha, descripcion, monto
        FROM ingresos
        ORDER BY fecha DESC
    """)

    datos = cursor.fetchall()
    conn.close()
    return datos


def total_ingresos():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(monto) FROM ingresos")
    total = cursor.fetchone()[0]

    conn.close()
    return total if total else 0