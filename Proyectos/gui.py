import tkinter as tk
from tkinter import ttk
from contacto import Contacto

contacto = Contacto()

ventana = tk.Tk()
ventana.title("Agenda Miguel")

# ---- RESPONSIVE ----
ventana.geometry("900x500")

ventana.columnconfigure(0, weight=1)
ventana.rowconfigure(0, weight=1)

contenedor = ttk.Frame(ventana)
contenedor.grid(row=0, column=0, sticky="nsew")

contenedor.columnconfigure(0, weight=1)
contenedor.rowconfigure(0, weight=1)

menu = tk.Menu(ventana)
ventana.config(menu=menu)

menu_contactos = tk.Menu(menu, tearoff=0)

menu.add_cascade(label="Contactos", menu=menu_contactos)

def ver_contactos():

    for widget in contenedor.winfo_children():
        widget.destroy()

    tabla = ttk.Treeview(contenedor)
    tabla["columns"] = ("ID", "Nombre", "Telefono")

    tabla.column("#0", width=0, stretch=False)
    tabla.column("ID", anchor="center", width=50)
    tabla.column("Nombre", anchor="center")
    tabla.column("Telefono", anchor="center")

    tabla.heading("#0", text="")
    tabla.heading("ID", text="ID")
    tabla.heading("Nombre", text="Nombre")
    tabla.heading("Telefono", text="Telefono")

    datos = contacto.leer()

    for fila in datos:
        tabla.insert("", "end", values=fila)

    tabla.grid(row=0, column=0, sticky="nsew")

    contenedor.columnconfigure(0, weight=1)
    contenedor.rowconfigure(0, weight=1)

def agregar_contacto():

    for widget in contenedor.winfo_children():
        widget.destroy()

    frame = ttk.Frame(contenedor)
    frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=2)

    ttk.Label(frame, text="Nombre:").grid(row=0, column=0, sticky="e", pady=10)
    txt_nombre = ttk.Entry(frame)
    txt_nombre.grid(row=0, column=1, sticky="ew", pady=10)

    ttk.Label(frame, text="Telefono:").grid(row=1, column=0, sticky="e", pady=10)
    txt_telefono = ttk.Entry(frame)
    txt_telefono.grid(row=1, column=1, sticky="ew", pady=10)

    def guardar():

        nombre = txt_nombre.get()
        telefono = txt_telefono.get()

        if nombre == "" or telefono == "":
            print("Complete los campos")
            return

        contacto.crear(nombre, int(telefono))
        print("Guardado!")

        txt_nombre.delete(0, tk.END)
        txt_telefono.delete(0, tk.END)

    btn_guardar = ttk.Button(frame, text="Guardar", command=guardar)
    btn_guardar.grid(row=2, column=0, columnspan=2, pady=20, sticky="ew")

menu_contactos.add_command(label="Ver", command=ver_contactos)
menu_contactos.add_command(label="Agregar", command=agregar_contacto)




ventana.mainloop()