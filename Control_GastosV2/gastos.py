from database import cursor, conn

from database import conn



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

def eliminar_gasto(id_gasto):

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM gastos WHERE id=?",
        (id_gasto,)
    )

    conn.commit()


def actualizar_gasto(id_gasto, fecha, descripcion, categoria, monto):

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