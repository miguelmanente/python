import tkinter as tk

def vista_eliminar(frame):

    for widget in frame.winfo_children():
        widget.destroy()

    tk.Label(frame, text="Eliminar Contacto",
             font=("Arial", 20)).pack(pady=20)