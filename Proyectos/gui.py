import tkinter as tk
from tkinter import ttk
from contacto import Contacto
from vistas.agregar import vista_agregar
from vistas.listar import vista_listar
from vistas.actualizar import vista_actualizar
from vistas.eliminar import vista_eliminar
from vistas.buscar import vista_buscar


contacto = Contacto()

ventana = tk.Tk()
ventana.title("AGENDA DE CONTACTOS")
menu_lateral = tk.Frame(ventana)
contenido = tk.Frame(ventana)

# ---- RESPONSIVE ----
ventana.geometry("900x500")

menu_lateral.grid(row=0, column=0, sticky="nsew")
contenido.grid(row=0, column=1, sticky="nsew")


ventana.columnconfigure(0, weight=1)
ventana.rowconfigure(0, weight=1)

menu_lateral = ttk.Frame(ventana)
menu_lateral.grid(row=0, column=0, sticky="nsew")
menu_lateral.columnconfigure(0, weight=1)
menu_lateral.columnconfigure(0, weight=1)

ventana.columnconfigure(0, weight=1)
ventana.rowconfigure(0, weight=1)

contenido = ttk.Frame(ventana)
contenido.grid(row=0, column=0, sticky="nsew")
contenido.columnconfigure(0, weight=1)
contenido.columnconfigure(0, weight=1)

menu = tk.Menu(ventana)
ventana.config(menu=menu)


def mostrar_agregar():
    vista_agregar(contenido)


def mostrar_listar():
    vista_listar(contenido)

def mostrar_actualizar():
    vista_actualizar(contenido, contacto)

def mostrar_eliminar():
    vista_eliminar(contenido, contacto)

def mostrar_buscar():
    vista_buscar(contenido)

barra_menu = tk.Menu(ventana)

menu_contactos = tk.Menu(barra_menu, tearoff=0)
menu_contactos.add_command(label="Agregar", command=mostrar_agregar)

menu_contactos.add_command(label="Listar", command=mostrar_listar)

menu_contactos.add_command(label="Actualizar", command=mostrar_actualizar)
#menu_contactos.add_command(label="Actualizar",command=lambda: vista_actualizar(frame, conexion))

menu_contactos.add_command(label="Eliminar", command=mostrar_eliminar)

barra_menu.add_cascade(label="Contactos", menu=menu_contactos)

ventana.config(menu=barra_menu)

ventana.mainloop()
