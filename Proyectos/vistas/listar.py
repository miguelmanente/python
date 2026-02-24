import tkinter as tk
from tkinter import ttk
from contacto import Contacto

def vista_listar(frame):

    # Limpia el contenido anterior
    for widget in frame.winfo_children():
        widget.destroy()

    tk.Label(frame, text="Lista de Contactos",
             font=("Arial", 20)).pack(pady=10)

    # TABLA
    tabla = ttk.Treeview(frame, columns=("ID","Nombre","Telefono"), show="headings")
    tabla.heading("ID", text="ID")
    tabla.heading("Nombre", text="Nombre")
    tabla.heading("Telefono", text="Telefono")

    tabla.pack(fill="both", expand=True)

    # OBTENER DATOS
    c = Contacto()
    datos = c.leer()

    # INSERTAR EN TABLA
    for fila in datos:
        tabla.insert("", tk.END, values=fila)
