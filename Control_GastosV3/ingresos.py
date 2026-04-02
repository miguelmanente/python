import tkinter as tk
from tkinter import ttk, messagebox
from database import conectar

id_ingreso_seleccionado = None

def ventana_ingresos():

    def cargar_ingresos():
        for fila in tree.get_children():
            tree.delete(fila)

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, fecha, descripcion, monto
            FROM ingresos
            ORDER BY fecha DESC
        """)

        resultados = cursor.fetchall()
        conn.close()

        for fila in resultados:
            tree.insert("", "end", values=fila)

    def limpiar_campos():
        entry_fecha.delete(0, tk.END)
        entry_descripcion.delete(0, tk.END)
        entry_monto.delete(0, tk.END)

    def agregar_ingreso():
        try:
            fecha = entry_fecha.get()
            descripcion = entry_descripcion.get()
            monto = float(entry_monto.get())

            conn = conectar()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO ingresos (fecha, descripcion, monto)
                VALUES (?, ?, ?)
            """, (fecha, descripcion, monto))

            conn.commit()
            conn.close()

            cargar_ingresos()
            limpiar_campos()

        except ValueError:
            messagebox.showerror("Error", "Monto inválido")

    def seleccionar_ingreso(event):
        global id_ingreso_seleccionado

        item = tree.focus()
        if not item:
            return

        valores = tree.item(item, "values")
        if not valores:
            return

        id_ingreso_seleccionado = valores[0]

        entry_fecha.delete(0, tk.END)
        entry_fecha.insert(0, valores[1])

        entry_descripcion.delete(0, tk.END)
        entry_descripcion.insert(0, valores[2])

        entry_monto.delete(0, tk.END)
        entry_monto.insert(0, valores[3])

    def actualizar_ingreso():
        global id_ingreso_seleccionado

        if id_ingreso_seleccionado is None:
            messagebox.showwarning("Atención", "Seleccione un ingreso")
            return

        try:
            fecha = entry_fecha.get()
            descripcion = entry_descripcion.get()
            monto = float(entry_monto.get())

            conn = conectar()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE ingresos
                SET fecha=?, descripcion=?, monto=?
                WHERE id=?
            """, (fecha, descripcion, monto, id_ingreso_seleccionado))

            conn.commit()
            conn.close()

            cargar_ingresos()
            limpiar_campos()

            id_ingreso_seleccionado = None

            messagebox.showinfo("OK", "Ingreso actualizado")

        except ValueError:
            messagebox.showerror("Error", "Monto inválido")

    def eliminar_ingreso():
        seleccion = tree.selection()

        if not seleccion:
            messagebox.showwarning("Aviso", "Seleccione un ingreso")
            return

        item = seleccion[0]
        valores = tree.item(item, "values")
        id_ingreso = valores[0]

        respuesta = messagebox.askyesno(
            "Eliminar",
            "¿Desea eliminar el ingreso seleccionado?"
        )

        if respuesta:
            conn = conectar()
            cursor = conn.cursor()

            cursor.execute("DELETE FROM ingresos WHERE id=?", (id_ingreso,))

            conn.commit()
            conn.close()

            cargar_ingresos()
            limpiar_campos()

    # -------- VENTANA --------
    ventana = tk.Toplevel()
    ventana.title("Ingresos")
    ventana.geometry("600x400")

    frame_form = tk.Frame(ventana)
    frame_form.pack(pady=10, padx=10, fill="x")

    tk.Label(frame_form, text="Fecha").grid(row=0, column=0, sticky="w")
    entry_fecha = tk.Entry(frame_form)
    entry_fecha.grid(row=0, column=1, sticky="ew")

    tk.Label(frame_form, text="Descripción").grid(row=1, column=0, sticky="w")
    entry_descripcion = tk.Entry(frame_form)
    entry_descripcion.grid(row=1, column=1, sticky="ew")

    tk.Label(frame_form, text="Monto").grid(row=2, column=0, sticky="w")
    entry_monto = tk.Entry(frame_form)
    entry_monto.grid(row=2, column=1, sticky="ew")

    frame_form.columnconfigure(1, weight=1)

    tk.Button(frame_form, text="Agregar", command=agregar_ingreso).grid(row=3, column=0, pady=10)
    tk.Button(frame_form, text="Actualizar", command=actualizar_ingreso).grid(row=3, column=1)
    tk.Button(frame_form, text="Eliminar", command=eliminar_ingreso).grid(row=4, column=0, columnspan=2)

    # -------- TABLA --------
    tree = ttk.Treeview(
        ventana,
        columns=("id", "fecha", "descripcion", "monto"),
        show="headings"
    )

    tree.heading("fecha", text="Fecha")
    tree.heading("descripcion", text="Descripción")
    tree.heading("monto", text="Monto")

    tree.column("id", width=0, stretch=False)
    tree.column("fecha", width=100)
    tree.column("descripcion", width=250)
    tree.column("monto", width=100, anchor="e")

    tree.pack(fill="both", expand=True, padx=10, pady=10)

    tree.bind("<<TreeviewSelect>>", seleccionar_ingreso)

    cargar_ingresos()