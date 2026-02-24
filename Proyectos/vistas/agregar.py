import tkinter as tk # Agregado para usar tkinter en esta vista
from contacto import Contacto    # Agregado para usar la clase Contacto y poder crear nuevos contactos
from tkinter import messagebox    # Agregado para mostrar mensajes de advertencia e información


def vista_agregar(frame):

   
    for widget in frame.winfo_children():
            widget.destroy()
    

    #Genera Formulario Agregar
    form = tk.Frame(frame)
    form.grid(row=0, column=0)
    form.grid_rowconfigure(0, weight=1)
    form.grid_columnconfigure(0, weight=1)
    form.grid_anchor("center")
    form.grid_columnconfigure(0, weight=1)
    form.grid_columnconfigure(1, weight=1)
  
    # TITULO
    tk.Label(form, text="Agregar Contacto",
                font=("Arial", 20)).grid(row=1, column=0, columnspan=2, pady=20)

    # NOMBRE
    tk.Label(form, text="Nombre:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    nombre = tk.Entry(form)
    nombre.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

    # TELEFONO
    tk.Label(form, text="Telefono:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
    telefono = tk.Entry(form)
    telefono.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

    #Guarda Contacto en la Base de Datos
    def guardar( nombre=nombre, telefono=telefono):

        if nombre.get() == "" or telefono.get() == "":
            messagebox.showwarning("Campos vacíos", "Debe completar todos los campos")
            return  # Salir de la función si hay campos vacíos

        c = Contacto()
        c.crear(nombre.get(), telefono.get())
   
        messagebox.showinfo("Contacto agregado", "El contacto fue agregado correctamente")

        # LIMPIAR CAMPOS (opcional)
        nombre.delete(0, tk.END)
        telefono.delete(0, tk.END)

    tk.Button(form, text="Guardar",
        command=guardar).grid(row=4, column=0, columnspan=2, pady=5)

