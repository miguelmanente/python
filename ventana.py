'''import tkinter as tk

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

#Iniciar el bucle principal de la aplicación
ventana.mainloop()'''

from tkinter import *

def mensaje():
    print("Mensaje del boton ")

ventana = Tk()
ventana.geometry("420x280")
ventana.title("Ventana Hola Mundo")

#Ventana con controles en posiciones absolutas

'''lbl1 = Label(ventana, text='Primer numero', bg='yellow')
lbl1.place(x=10, y=10, width=100, height=30)
text1 = Entry(ventana, bg='pink')
text1.place(x=120, y=10, width=100, height=30)

def fnSuma():
    n1 = text1.get()
    n2 = text2.get()
    r = float(n1) + float(n2)
    text3.delete(0, 'end')
    text3.insert(0,r)

lbl2 = Label(ventana, text='Segundo numero', bg='yellow')
lbl2.place(x=10, y=50, width=100, height=30)
text2 = Entry(ventana, bg='pink')
text2.place(x=120, y=50, width=100, height=30)
btn1 = Button(ventana, text="Sumar", command=fnSuma)
btn1.place(x=230, y=50, width=80, height=30)


lbl3 = Label(ventana, text='Resultado', bg='yellow')
lbl3.place(x=10, y=120, width=100, height=30)
text3 = Entry(ventana, bg='pink')
text3.place(x=120, y=120, width=100, height=30)'''

#Ventana con controles en posiciones absrelativas

lbl1 = Label(ventana, text='Primer numero', bg='yellow')
lbl1.place(relx=0.03, rely=0.04, relwidth=0.23, relheight=0.1)
text1 = Entry(ventana, bg='pink')
text1.place(relx=0.3, rely=0.04, relwidth=0.23, relheight=0.1)

def fnSuma():
    n1 = text1.get()
    n2 = text2.get()
    r = float(n1) + float(n2)
    text3.delete(0, 'end')
    text3.insert(0,r)

lbl2 = Label(ventana, text='Segundo numero', bg='yellow')
lbl2.place(relx=0.03, rely=0.17, relwidth=0.23, relheight=0.1)
text2 = Entry(ventana, bg='pink')
text2.place(relx=0.3, rely=0.17, relwidth=0.23, relheight=0.1)

btn1 = Button(ventana, text="Sumar", command=fnSuma)
btn1.place(relx=0.55, rely=0.17, relwidth=0.20, relheight=0.1)


lbl3 = Label(ventana, text='Resultado', bg='yellow')
lbl3.place(relx=0.03, rely=0.35, relwidth=0.23, relheight=0.1)
text3 = Entry(ventana, bg='pink')
text3.place(relx=0.3, rely=0.35, relwidth=0.23, relheight=0.1)

ventana.mainloop()

