import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from database import conn


def abrir_estadisticas(mes, anio):

    ventana = tk.Toplevel()
    ventana.title("Panel de Estadísticas")
    ventana.geometry("900x600")

    frame = tk.Frame(ventana)
    frame.pack(fill="both", expand=True)

    fig = Figure(figsize=(9,6), dpi=100)

    ax1 = fig.add_subplot(221)
    ax2 = fig.add_subplot(222)
    ax3 = fig.add_subplot(212)

    cursor = conn.cursor()

    # -------------------------
    # GASTOS POR CATEGORÍA
    # -------------------------
    cursor.execute("""
        SELECT categoria, SUM(monto)
        FROM gastos
        WHERE strftime('%m', fecha)=?
        AND strftime('%Y', fecha)=?
        GROUP BY categoria
    """, (f"{mes:02}", str(anio)))

    datos = cursor.fetchall()

    categorias = [d[0] for d in datos]
    montos = [d[1] for d in datos]

    if categorias:
        ax1.bar(categorias, montos)
        ax1.set_title("Gastos por categoría")
        ax1.tick_params(axis="x", rotation=90)

    # -------------------------
    # INGRESOS VS GASTOS
    # -------------------------
    cursor.execute("""
        SELECT SUM(monto)
        FROM ingresos
        WHERE strftime('%m', fecha)=?
        AND strftime('%Y', fecha)=?
    """, (f"{mes:02}", str(anio)))

    fila = cursor.fetchone()
    ingresos = fila[0] or 0

    cursor.execute("""
        SELECT SUM(monto)
        FROM gastos
        WHERE strftime('%m', fecha)=?
        AND strftime('%Y', fecha)=?
    """, (f"{mes:02}", str(anio)))

    fila = cursor.fetchone()
    gastos_mes = fila[0] or 0

    ax2.bar(
        ["Ingresos", "Gastos"],
        [ingresos, gastos_mes],
        color=["green", "red"]
    )

    ax2.set_title("Ingresos vs Gastos")

    # -------------------------
    # EVOLUCIÓN DE GASTOS DEL AÑO
    # -------------------------
    meses_sql = [
        "01","02","03","04","05","06",
        "07","08","09","10","11","12"
    ]

    nombres_meses = [
        "Ene","Feb","Mar","Abr","May","Jun",
        "Jul","Ago","Sep","Oct","Nov","Dic"
    ]

    gastos_anio = []

    for mes_num in meses_sql:

        cursor.execute("""
            SELECT SUM(monto)
            FROM gastos
            WHERE strftime('%m', fecha)=?
            AND strftime('%Y', fecha)=?
        """, (mes_num, str(anio)))

        fila = cursor.fetchone()
        total = fila[0] or 0

        gastos_anio.append(total)

    ax3.plot(nombres_meses, gastos_anio, marker="o", linewidth=2)

    ax3.set_title("Evolución de gastos del año")
    ax3.grid(True)

    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)























