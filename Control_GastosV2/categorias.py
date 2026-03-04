import tkinter as tk
from tkinter import messagebox
from database import cursor, conn, obtener_categorias


def abrir_ventana_categorias(ventana_principal, refrescar_combobox):

    ventana_cat = tk.Toplevel(ventana_principal)
    ventana_cat.title("Administrar Categorías")
    ventana_cat.geometry("350x400")

    listbox = tk.Listbox(ventana_cat)
    listbox.pack(pady=10, fill="both", expand=True)

    entry = tk.Entry(ventana_cat)
    entry.pack(pady=5)

    def cargar():
        listbox.delete(0, tk.END)
        for c in obtener_categorias():
            listbox.insert(tk.END, c)

    def agregar():
        nombre = entry.get().strip()
        if nombre:
            try:
                cursor.execute(
                    "INSERT INTO categorias (nombre) VALUES (?)",
                    (nombre,)
                )
                conn.commit()
                cargar()
                refrescar_combobox()
                entry.delete(0, tk.END)
            except:
                messagebox.showerror("Error", "Categoría ya existe")

    def eliminar():
        seleccion = listbox.curselection()
        if seleccion:
            nombre = listbox.get(seleccion[0])
            cursor.execute(
                "DELETE FROM categorias WHERE nombre = ?",
                (nombre,)
            )
            conn.commit()
            cargar()
            refrescar_combobox()

    def modificar():
        seleccion = listbox.curselection()
        nuevo = entry.get().strip()
        if seleccion and nuevo:
            viejo = listbox.get(seleccion[0])
            try:
                cursor.execute(
                    "UPDATE categorias SET nombre = ? WHERE nombre = ?",
                    (nuevo, viejo)
                )
                conn.commit()
                cargar()
                refrescar_combobox()
                entry.delete(0, tk.END)
            except:
                messagebox.showerror("Error", "Categoría ya existe")

    tk.Button(ventana_cat, text="Agregar", command=agregar).pack(pady=3)
    tk.Button(ventana_cat, text="Modificar", command=modificar).pack(pady=3)
    tk.Button(ventana_cat, text="Eliminar", command=eliminar).pack(pady=3)

    cargar()