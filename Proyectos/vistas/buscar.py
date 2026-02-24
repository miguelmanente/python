import tkinter as tk

def vista_buscar(frame):

    for widget in frame.winfo_children():
        widget.destroy()

    tk.Label(frame, text="Buscar Contacto",
             font=("Arial", 20)).pack(pady=20)