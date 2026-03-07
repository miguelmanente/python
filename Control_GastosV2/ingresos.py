import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from database import insertar_ingreso, obtener_ingresos
from database import total_gastos, total_ingresos


def ventana_ingresos():

    ventana = tk.Toplevel()
    ventana.title("Gestión de Ingresos")
    ventana.geometry("900x600")

    frame_principal = tk.Frame(ventana)
    frame_principal.pack(fill="both", expand=True, padx=10, pady=10)

    frame_form = tk.Frame(frame_principal)
    frame_form.grid(row=0, column=0, sticky="nsew", padx=10)

    frame_tabla = tk.Frame(frame_principal)
    frame_tabla.grid(row=0, column=1, sticky="nsew", padx=10)

    frame_principal.columnconfigure(0, weight=1)
    frame_principal.columnconfigure(1, weight=2)

    tk.Label(frame_form, text="Fecha").grid(row=0, column=0, sticky="w")
    entry_fecha = tk.Entry(frame_form)
    entry_fecha.grid(row=0, column=1, sticky="ew")

    tk.Label(frame_form, text="Descripción").grid(row=1, column=0, sticky="w")
    entry_desc = tk.Entry(frame_form)
    entry_desc.grid(row=1, column=1, sticky="ew")

    tk.Label(frame_form, text="Monto").grid(row=2, column=0, sticky="w")
    entry_monto = tk.Entry(frame_form)
    entry_monto.grid(row=2, column=1, sticky="ew")

    tree = ttk.Treeview(
    frame_tabla,
    columns=("fecha","descripcion","monto"),
    show="headings"
    )   

    tree.heading("fecha", text="Fecha")
    tree.heading("descripcion", text="Descripción")
    tree.heading("monto", text="Monto")

    tree.column("monto", anchor="e")

    tree.grid(row=0, column=0, sticky="nsew")

    scroll = ttk.Scrollbar(frame_tabla, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scroll.set)
    scroll.grid(row=0, column=1, sticky="ns")

    def cargar_ingresos():

        for fila in tree.get_children():
            tree.delete(fila)

        for ingreso in obtener_ingresos():
            tree.insert("", "end", values=ingreso[1:])
    
    def agregar():

        fecha = entry_fecha.get()
        descripcion = entry_desc.get()
        monto = float(entry_monto.get())

        insertar_ingreso(fecha, descripcion, monto)

        cargar_ingresos()
     

        entry_desc.delete(0, tk.END)
        entry_monto.delete(0, tk.END)

    def salir():
        if messagebox.askyesno("Salir", "¿Desea la ventana Ingresos?"):
            ventana.destroy()

    tk.Button(frame_form, text="Agregar ingreso", command=agregar).grid(row=3, column=0, columnspan=2, pady=10)
    tk.Button(frame_form, text="Salir", command=salir).grid(row=4, column=0, columnspan=2, pady=20)

 

#ventana_ingresos(actualizar_resumen)
    