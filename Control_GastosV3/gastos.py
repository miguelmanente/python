from database import conectar


def agregar_gasto(fecha, descripcion, categoria, monto):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO gastos (fecha, descripcion, categoria, monto) VALUES (?, ?, ?, ?)",
        (fecha, descripcion, categoria, monto)
    )

    conn.commit()
    conn.close()


def obtener_gastos():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, fecha, descripcion, categoria, monto FROM gastos ORDER BY fecha DESC"
    )

    datos = cursor.fetchall()
    conn.close()
    return datos


def calcular_total_gastos():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(monto) FROM gastos")
    resultado = cursor.fetchone()[0]

    conn.close()
    return resultado if resultado else 0


def eliminar_gasto(id_gasto):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM gastos WHERE id=?", (id_gasto,))

    conn.commit()
    conn.close()


def actualizar_gasto(id_gasto, fecha, descripcion, categoria, monto):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE gastos
        SET fecha=?, descripcion=?, categoria=?, monto=?
        WHERE id=?
        """,
        (fecha, descripcion, categoria, monto, id_gasto)
    )

    conn.commit()
    conn.close()