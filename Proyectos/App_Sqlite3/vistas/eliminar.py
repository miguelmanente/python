import tkinter as tk
from tkinter import ttk, messagebox
from Proyectos.App_Sqlite3.contacto import Contacto


def vista_eliminar(frame, contacto):

    for widget in frame.winfo_children():
        widget.destroy()

    form = tk.Frame(frame)
    form.grid(row=0, column=0)

    form.grid_columnconfigure(0, weight=1)
    form.grid_columnconfigure(1, weight=1)

    # 🟢 TITULO
    tk.Label(form, text="Eliminar Contacto",
             font=("Arial", 20)).grid(row=0, column=0, columnspan=3, pady=10)
    
    #FRAME BUSCADOR
    frame_buscar = tk.Frame(form)
    frame_buscar.grid(row=1, column=0, columnspan=3, pady=10)

    # 🔎 BUSCADOR
    tk.Label(frame_buscar, text="Buscar por apellido:").grid(row=1, column=0, padx=5)
    buscar_apellido = tk.Entry(frame_buscar)
    buscar_apellido.grid(row=1, column=1, padx=5)

    # 🧾 FRAME TREEVIEW + SCROLL
    frame_tree = ttk.Frame(form)
    frame_tree.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=10)

    frame_tree.grid_columnconfigure(0, weight=1)
    frame_tree.grid_rowconfigure(0, weight=1)

    # 🧾 TREEVIEW
    tree = ttk.Treeview(
        frame_tree,   # ✅ AHORA SI
        columns=("ID", "Nombre", "Telefono"),
        show="headings",
        height=8
    )

    tree.heading("ID", text="ID")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Telefono", text="Telefono")

    tree.column("ID", width=80, anchor="center")
    tree.column("Nombre", width=300, anchor="center")
    tree.column("Telefono", width=250, anchor="center")

    tree.grid(row=0, column=0, sticky="nsew")

    # 📜 SCROLLBAR
    scroll = ttk.Scrollbar(frame_tree, orient="vertical", command=tree.yview)
    scroll.grid(row=0, column=1, sticky="ns")

    tree.configure(yscrollcommand=scroll.set)

    selected_id = tk.StringVar()

    # 🔎 BUSCAR
    def buscar():

        for item in tree.get_children():
            tree.delete(item)

        
        resultados = contacto.buscar_por_apellido(buscar_apellido.get())

        for fila in resultados:
            tree.insert("", tk.END, values=fila)

    
    # BOTON BUSCAR
    tk.Button(frame_buscar, text="Buscar", command=buscar).grid(row=1, column=3, padx=5)

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
            contacto.eliminar(selected_id.get())

            messagebox.showinfo("Eliminado",
                                "Contacto eliminado correctamente")

            selected_id.set("")
            buscar()

    tk.Button(form,
              text="Eliminar",
              bg="red",
              fg="white",
              command=eliminar).grid(row=3, column=0, columnspan=3, pady=10)