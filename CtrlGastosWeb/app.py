from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def conectar():
    conn = sqlite3.connect("gastos.db", timeout=10)
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn

@app.route("/")
def index():
    conn = conectar()
    cursor = conn.cursor()

    # Gastos
    cursor.execute("""
        SELECT id, fecha, descripcion, categoria, monto
        FROM gastos
        ORDER BY fecha DESC
    """)
    gastos = cursor.fetchall()

    # Categorías
    cursor.execute("SELECT nombre FROM categorias ORDER BY nombre")
    categorias = [fila[0] for fila in cursor.fetchall()]

    # Total ingresos del mes
    cursor.execute("""
        SELECT SUM(monto) FROM ingresos
        WHERE strftime('%m', fecha) = strftime('%m', 'now')
        AND strftime('%Y', fecha) = strftime('%Y', 'now')
    """)
    total_ingresos = cursor.fetchone()[0] or 0

    # Total gastos del mes
    cursor.execute("""
        SELECT SUM(monto) FROM gastos
        WHERE strftime('%m', fecha) = strftime('%m', 'now')
        AND strftime('%Y', fecha) = strftime('%Y', 'now')
    """)
    total_gastos = cursor.fetchone()[0] or 0

    conn.close()

    return render_template("index.html",
                           gastos=gastos,
                           categorias=categorias,
                           total_ingresos=total_ingresos,
                           total_gastos=total_gastos)


@app.route("/agregar", methods=["POST"])
def agregar():
    fecha = request.form["fecha"]
    descripcion = request.form["descripcion"]
    categoria = request.form["categoria"]
    monto = float(request.form["monto"])

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO gastos (fecha, descripcion, categoria, monto)
        VALUES (?, ?, ?, ?)
    """, (fecha, descripcion, categoria, monto))

    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/agregar_ingreso", methods=["POST"])
def agregar_ingreso():
    fecha = request.form["fecha"]
    descripcion = request.form["descripcion"]
    monto = float(request.form["monto"])

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO ingresos (fecha, descripcion, monto)
        VALUES (?, ?, ?)
    """, (fecha, descripcion, monto))

    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/agregar_categoria", methods=["POST"])
def agregar_categoria():
    nombre = request.form["nombre"]

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO categorias (nombre) VALUES (?)", (nombre,))

    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/eliminar/<int:id>")
def eliminar(id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM gastos WHERE id = ?", (id,))

    conn.commit()
    conn.close()

    return redirect("/")

if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host="0.0.0.0", port=5000, debug=True)