from database import conectar, cursor,conn




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

def limpiar_gastos_mes(mes, anio):
    conn = conectar()
    cursor = conn.cursor()

    mes = str(mes).zfill(2)
    anio = str(anio)

    cursor.execute("""
        DELETE FROM gastos
        WHERE substr(fecha, 6, 2)=?
        AND substr(fecha, 1, 4)=?
    """, (mes, anio))

    conn.commit()
    conn.close()

def total_gastos_mes(mes, anio):
    conn = conectar()
    cursor = conn.cursor()

    fecha_inicio = f"{anio}-{str(mes).zfill(2)}-01"

    if mes == 12:
        fecha_fin = f"{anio+1}-01-01"
    else:
        fecha_fin = f"{anio}-{str(mes+1).zfill(2)}-01"

    cursor.execute("""
        SELECT SUM(monto) FROM gastos
        WHERE fecha >= ? AND fecha < ?
    """, (fecha_inicio, fecha_fin))

    total = cursor.fetchone()[0]
    conn.close()

    return total if total else 0