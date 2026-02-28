import tkinter as tk
from tkinter import ttk
from Proyectos.App_Sqlite3.contacto import Contacto

def vista_listar(frame, contacto):

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
    datos = contacto.leer()

    # INSERTAR EN TABLA
    for fila in datos:
        tabla.insert("", tk.END, values=fila)
