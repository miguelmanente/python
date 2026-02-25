import tkinter as tk
from tkinter import ttk, messagebox
from contacto import Contacto


def vista_actualizar(frame):

    for widget in frame.winfo_children():
        widget.destroy()

    form = tk.Frame(frame)
    form.pack(pady=20)

    tk.Label(form, text="Actualizar Contacto",
             font=("Arial", 20)).pack(pady=10)

    # 🔎 BUSCADOR
    tk.Label(form, text="Buscar por apellido:").pack()
    buscar_apellido = tk.Entry(form)
    buscar_apellido.pack()

    tree = ttk.Treeview(form, columns=("ID", "Nombre", "Telefono"),
                        show="headings", height=6)

    tree.heading("ID", text="ID")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Telefono", text="Telefono")

    tree.pack(pady=10)

    # 🔎 FUNCION BUSCAR
    def buscar():

        for item in tree.get_children():
            tree.delete(item)

        c = Contacto()
        resultados = c.buscar_por_apellido(buscar_apellido.get())

        for fila in resultados:
            tree.insert("", tk.END, values=fila)

    tk.Button(form, text="Buscar", command=buscar).pack()

    # 📥 ENTRIES PARA EDITAR
    tk.Label(form, text="Nombre").pack()
    entry_nombre = tk.Entry(form)
    entry_nombre.pack()

    tk.Label(form, text="Telefono").pack()
    entry_telefono = tk.Entry(form)
    entry_telefono.pack()

    selected_id = tk.StringVar()

    # 📌 CUANDO SELECCIONA EN TREEVIEW
    def seleccionar(event):
        item = tree.selection()
        if item:
            valores = tree.item(item)["values"]
            selected_id.set(valores[0])

            entry_nombre.delete(0, tk.END)
            entry_telefono.delete(0, tk.END)

            entry_nombre.insert(0, valores[1])
            entry_telefono.insert(0, valores[2])

    tree.bind("<<TreeviewSelect>>", seleccionar)

    # 💾 ACTUALIZAR
    def actualizar():

        if selected_id.get() == "":
            messagebox.showwarning("Error", "Seleccione un contacto")
            return

        c = Contacto()
        c.actualizar(selected_id.get(),
                     entry_nombre.get(),
                     entry_telefono.get())

        messagebox.showinfo("Actualizado",
                            "Contacto actualizado correctamente")

        buscar()  # refresca lista

    tk.Button(form, text="Actualizar", command=actualizar).pack(pady=10)