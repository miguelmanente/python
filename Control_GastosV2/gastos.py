from database import cursor, conn


def agregar_gasto(fecha, descripcion, categoria, monto):
    cursor.execute(
        "INSERT INTO gastos (fecha, descripcion, categoria, monto) VALUES (?, ?, ?, ?)",
        (fecha, descripcion, categoria, monto)
    )
    conn.commit()


def obtener_gastos():
    cursor.execute("SELECT id, fecha, descripcion, categoria, monto FROM gastos ORDER BY fecha DESC")
    return cursor.fetchall()


def calcular_total_gastos():
    cursor.execute("SELECT SUM(monto) FROM gastos")
    resultado = cursor.fetchone()[0]
    return resultado if resultado else 0