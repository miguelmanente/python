from tkinter import *

root=Tk()

miframe = Frame(root, width=500, height=600)

miframe.pack()

milabel = Label(miframe, text="Hola Miguel Angel")  #creacion de una etiqueta o label con un texto en el frame
#milabel.pack()  #par poder verlo en la ventana principal lo empaquetamos con pack
                #pero se verá muy chico pq la ventan el frame tomarán las dimensiones del label
                #para evitar eso usamos place() con valores de ancho y alto
#milabel.place(x=100, y=100)  #ubica el label a 100 en x y 100 del borde superior


#Label(miframe, text="Hola Miguel Angel", fg="red", font=("Comic Sans MS",18) ).place(x=10, y=200) #otra forma de escribir lo anterior 
mimage = PhotoImage(file="Whtasapp.png")   #forma de poner imagen en el frame, estenxiones png y gif
Label(miframe, image=mimage).place(x=0, y=0)  #forma de utilizarlo en un label
root.mainloop()