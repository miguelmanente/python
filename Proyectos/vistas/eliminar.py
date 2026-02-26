import tkinter as tk
from tkinter import ttk, messagebox
from contacto import Contacto


def vista_eliminar(frame):

    for widget in frame.winfo_children():
        widget.destroy()

    form = tk.Frame(frame)
    form.grid(row=0, column=0)

    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    # 🟢 TITULO
    tk.Label(form, text="Eliminar Contacto",
             font=("Arial", 20)).grid(row=0, column=0, columnspan=3, pady=10)

    # 🔎 BUSCADOR
    tk.Label(form, text="Buscar por apellido:").grid(row=1, column=0, padx=5)
    buscar_apellido = tk.Entry(form)
    buscar_apellido.grid(row=1, column=1, padx=5)

    # BOTON BUSCAR
    tk.Button(form, text="Buscar").grid(row=1, column=2, padx=5)

    # 🧾 TREEVIEW
    tree = ttk.Treeview(
        form,
        columns=("ID", "Nombre", "Telefono"),
        show="headings",
        height=6
    )

    tree.heading("ID", text="ID")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Telefono", text="Telefono")

    tree.column("ID", width=50, anchor="center")
    tree.column("Nombre", width=150)
    tree.column("Telefono", width=120)

    tree.grid(row=2, column=0, columnspan=2, sticky="ew", pady=10)

    # 📜 SCROLL
    scroll = ttk.Scrollbar(form, orient="vertical", command=tree.yview)
    scroll.grid(row=2, column=2, sticky="ns")

    tree.configure(yscrollcommand=scroll.set)

    selected_id = tk.StringVar()

    # 🔎 BUSCAR
    def buscar():

        for item in tree.get_children():
            tree.delete(item)

        c = Contacto()
        resultados = c.buscar_por_apellido(buscar_apellido.get())

        for fila in resultados:
            tree.insert("", tk.END, values=fila)

    # asignar comando ahora
    tk.Button(form, text="Buscar", command=buscar).grid(row=1, column=2)

    # 📌 SELECCIONAR
    def seleccionar(event):
        item = tree.selection()
        if item:
            valores = tree.item(item)["values"]
            selected_id.set(valores[0])

    tree.bind("<<TreeviewSelect>>", seleccionar)

    # 🗑 ELIMINAR
    def eliminar():

        if selected_id.get() == "":
            messagebox.showwarning("Error", "Seleccione un contacto")
            return

        confirmar = messagebox.askyesno(
            "Confirmar",
            "¿Está seguro que desea eliminar el contacto?"
        )

        if confirmar:

            c = Contacto()
            c.eliminar(selected_id.get())

            messagebox.showinfo("Eliminado",
                                "Contacto eliminado correctamente")

            selected_id.set("")
            buscar()

    tk.Button(form,
              text="Eliminar",
              bg="red",
              fg="white",
              command=eliminar).grid(row=3, column=0, columnspan=3, pady=10)