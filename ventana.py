import tkinter as tk

def crearVentana():
    #Crear una nueva ventana 
    ventanaTop = tk.Toplevel(ventana)
    ventanaTop.title = "Ventana top_level"
    ventanaTop.geometry("400x200")

#Crear ventana Principal
ventana =tk.Tk()
ventana.title("Ventana Principal")
ventana.configure(bg="#C6D9E3")
ventana.geometry("600x400")

#Crear un boton que abra la ventana secundaria
boton = tk.Button(ventana, text="Abrir Ventana", command=crearVentana)
boton.pack()
boton.place(x=50, y=200)  # Se usa para ubicar el elemento boton en la ventana

#Iniciar el buble principal de la aplicación
ventana.mainloop()
