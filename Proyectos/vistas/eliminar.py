import tkinter as tk
from tkinter import ttk, messagebox
from contacto import Contacto


def vista_eliminar(frame):

    for widget in frame.winfo_children():
        widget.destroy()

    form = tk.Frame(frame)
    form.pack(pady=20)

    tk.Label(form, text="Eliminar Contacto",
             font=("Arial", 20)).pack(pady=10)

    # 🔎 BUSCADOR
    tk.Label(form, text="Buscar por apellido:").pack()
    buscar_apellido = tk.Entry(form)
    buscar_apellido.pack()

    tree = ttk.Treeview(form,
                        columns=("ID", "Nombre", "Telefono"),
                        show="headings",
                        height=6)

    tree.heading("ID", text="ID")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Telefono", text="Telefono")

    tree.pack(pady=10)

  

    selected_id = tk.StringVar()

    # 🔎 BUSCAR
    def buscar():

        for item in tree.get_children():
            tree.delete(item)

        c = Contacto()
        resultados = c.buscar_por_apellido(buscar_apellido.get())

        for fila in resultados:
            tree.insert("", tk.END, values=fila)

    tk.Button(form, text="Buscar", command=buscar).pack()

    # 📌 SELECCIONAR FILA
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
            buscar()  # refresca lista

    tk.Button(form,
              text="Eliminar",
              bg="red",
              fg="white",
              command=eliminar).pack(pady=10)