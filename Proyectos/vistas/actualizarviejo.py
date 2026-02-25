import tkinter as tk
from contacto import Contacto
from tkinter import messagebox


def vista_actualizar(frame):

    for widget in frame.winfo_children():
        widget.destroy()

    # GENERA FORMULARIO
    form = tk.Frame(frame)
    form.grid(row=0, column=0)
    form.grid_anchor("center")

    form.grid_columnconfigure(0, weight=1)
    form.grid_columnconfigure(1, weight=1)

    # TITULO
    tk.Label(form, text="Actualizar Contacto",
             font=("Arial", 20)).grid(row=1, column=0, columnspan=2, pady=20)

    # ID
    tk.Label(form, text="ID:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    id_contacto = tk.Entry(form)
    id_contacto.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

    # NOMBRE
    tk.Label(form, text="Nombre:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
    nombre = tk.Entry(form)
    nombre.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

    # TELEFONO
    tk.Label(form, text="Telefono:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
    telefono = tk.Entry(form)
    telefono.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

    # ACTUALIZA CONTACTO
    def actualizar(id=id_contacto, nombre=nombre, telefono=telefono):

        if id_contacto.get() == 0 or nombre.get() == "" or telefono.get() == "":
            messagebox.showwarning("Campos vacíos", "Debe completar todos los campos")
            return

        c = Contacto()
        c.actualizar(id_contacto.get(), nombre.get(), telefono.get())

        messagebox.showinfo("Actualizado", "Contacto actualizado correctamente")

        # LIMPIAR CAMPOS
        id_contacto.delete(0, tk.END)
        nombre.delete(0, tk.END)
        telefono.delete(0, tk.END)

    tk.Button(form, text="Actualizar", command=actualizar).grid(row=5, column=0, columnspan=2, pady=10)