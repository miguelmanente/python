import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from database import registrar_usuario
from centraVent import cventana

#--------------------- Registros en la tabla ususarios la loguearse ----------------
def ventana_registro():
    registro = tk.Toplevel()
    registro.title("Registro de Usuario")
    registro.geometry("400x300")
    registro.grab_set()

    tk.Label(registro, text="Usuario").pack(pady=5)
    entry_usuario = tk.Entry(registro)
    entry_usuario.pack()

    tk.Label(registro, text="Contraseña").pack(pady=5)
    entry_password = tk.Entry(registro, show="*")
    entry_password.pack()

    def registrar():
        usuario = entry_usuario.get()
        password = entry_password.get()

        if not usuario or not password:
            messagebox.showwarning("Advertencia", "Complete todos los campos")
            return

        if registrar_usuario(usuario, password):
            messagebox.showinfo("Éxito", "Usuario registrado correctamente")
            registro.destroy()
        else:
            messagebox.showerror("Error", "El usuario ya existe")

    
    #-------------------------------  Salir de la aplicación -------------------------------------
    def salir():
        if messagebox.askyesno("Salir", "¿Desea salir de registración?"):
            registro.destroy()
    #----------------------------------------------------------------------------------------------
    
    #botenes de la vnetana de logueo
    tk.Button(registro, text="Registrarse", command=registrar).pack(pady=10)
    tk.Button(registro, text="Salir", command=salir).pack(pady=10)
#-----------------------------------------------------------------------------------


    #Llama a la función que está en el módulo centraVent
    cventana(registro)