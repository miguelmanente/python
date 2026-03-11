import tkinter as tk
import matplotlib.pyplot as plt
from database import conn


def abrir_estadisticas(mes, anio):

    cursor = conn.cursor()

    cursor.execute("""
        SELECT categoria, SUM(monto)
        FROM gastos
        WHERE strftime('%m', fecha)=?
        AND strftime('%Y', fecha)=?
        GROUP BY categoria
    """, (f"{mes:02}", str(anio)))

    datos = cursor.fetchall()
   
    categorias = []
    montos = []

    for c, m in datos:
        categorias.append(c)
        montos.append(m)

    plt.figure(figsize=(7,5))

    plt.bar(categorias, montos)

    plt.title("Gastos por categoría")

    plt.xlabel("Categoría")

    plt.ylabel("Monto")

    plt.show()