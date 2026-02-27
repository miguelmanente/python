import tkinter as tk # Agregado para usar tkinter en esta vista
from contacto import Contacto    # Agregado para usar la clase Contacto y poder crear nuevos contactos
from tkinter import messagebox    # Agregado para mostrar mensajes de advertencia e información


def vista_agregar(frame, contacto):

   
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
  


       #FRAME AGREGAR
    frame_agregar = tk.Frame(form)
    frame_agregar.grid(row=1, column=0, columnspan=3, pady=10)

        # TITULO
    tk.Label(frame_agregar, text="Agregar Contacto",font=("Arial", 20)).grid(row=1, column=0, columnspan=2, pady=20)

    # NOMBRE
    tk.Label(frame_agregar, text="Apellido y Nombres:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    nombre = tk.Entry(frame_agregar)
    nombre.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

    # TELEFONO
    tk.Label(frame_agregar, text="Teléfono del Contacto:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
    telefono = tk.Entry(frame_agregar)
    telefono.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

    #Guarda Contacto en la Base de Datos
    def guardar( nombre=nombre, telefono=telefono):

        if nombre.get() == "" or telefono.get() == "":
            messagebox.showwarning("Campos vacíos", "Debe completar todos los campos")
            return  # Salir de la función si hay campos vacíos

        contacto.crear(nombre.get(), telefono.get())
   
        messagebox.showinfo("Contacto agregado", "El contacto fue agregado correctamente")

        # LIMPIAR CAMPOS (opcional)
        nombre.delete(0, tk.END)
        telefono.delete(0, tk.END)

    tk.Button(form, text="Guardar",
        command=guardar).grid(row=4, column=0, columnspan=2, pady=5)

