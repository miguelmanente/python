import tkinter as tk
import sqlite3
from tkinter import messagebox
from database import conectar, obtener_categorias


def abrir_ventana_categorias(ventana_principal, refrescar_combobox):

    ventana_cat = tk.Toplevel(ventana_principal)
    ventana_cat.title("Administrar Categorías")
    ventana_cat.geometry("350x500")

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

        if nombre == "":
            return

        try:
            conectar.execute(
                "INSERT INTO categorias (nombre) VALUES (?)",
                (nombre,)
            )
            conectar.commit()

            cargar()
            refrescar_combobox["values"] = obtener_categorias()
            entry.delete(0, tk.END)

        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "La categoría ya existe")

    def eliminar():
        seleccion = listbox.curselection()
        if seleccion:
            nombre = listbox.get(seleccion[0])
            conectar.execute(
                "DELETE FROM categorias WHERE nombre = ?",
                (nombre,)
            )
            conectar.commit()
            cargar()
            refrescar_combobox["values"] = obtener_categorias()

    def modificar():
        seleccion = listbox.curselection()
        nuevo = entry.get().strip()
        if seleccion and nuevo:
            viejo = listbox.get(seleccion[0])
            try:
                conectar.execute(
                    "UPDATE categorias SET nombre = ? WHERE nombre = ?",
                    (nuevo, viejo)
                )
                conectar.commit()
                cargar()
                refrescar_combobox["values"] = obtener_categorias()
                entry.delete(0, tk.END)
            except:
                messagebox.showerror("Error", "Categoría ya existe")
    def salir():
        if messagebox.askyesno("Salir", "¿Desea la ventana Categorias?"):
            ventana_cat.destroy()


    tk.Button(ventana_cat, text="Agregar", command=agregar).pack(pady=3)
    tk.Button(ventana_cat, text="Modificar", command=modificar).pack(pady=3)
    tk.Button(ventana_cat, text="Eliminar", command=eliminar).pack(pady=3)
    tk.Button(ventana_cat, text="Salir", command=salir).pack(pady=3)

    cargar()