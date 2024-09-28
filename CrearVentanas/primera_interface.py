from tkinter import *    #Importar las Librerías necesarias para trabajar
                         #con los elementos gráficos

raiz = Tk()           #Sobre una variable cualquiera llamamos a la clase Tk() para crear una ventana ppal   
raiz.title("Primera Interface")   #De esta menera podemos poner un titulo a la ventana
#raiz.resizable(1,0) # si en los parentesis ponemos (0,0) o (False, False)
                    # La ventana no se podrá agrandar ni con el mouse ni botón maximizar
                    # Si en los parentesis ponemos (1,0) o (True, False) la  ventana solo se podrá agrandar horizontalmente
                    # Si en los parentesis ponemos (1,1) o (True, True) la ventana se podrá agrandar con el mouse y el botón maximizar
                                        
raiz.iconbitmap("ficheros.ico")  #De esta forma podemos cambiar el ícono de la ventana
#raiz.geometry("650x350")  #con geometry podemos redimensionar la ventana
raiz. config(bg="blue")   #Una de la cosas que podemos hacer con config es darle color al fondo de la ventana raiz

miframe = Frame() #Creamos un marco o Frame en la ventana ppal llamada raiz

miframe.pack()   #con pack lo empaquetamos para quedar en la ventana (queda como fondo sin que lo vemos hasta...)
miframe.config(bg="red") #Le damos color al fondo
miframe.config(width="650", height="350") #de esta forma podemos darle tamaño al frame y si agrandamos la ventan veremos la ventana ppal al fondo y el frame arriba
#miframe.pack(side="left") #posiciona el frame a la izquierda de la ventana
#miframe.pack(side="right") #posiciona el frame a la derecha de la ventana
#miframe.pack(side="top") #posiciona el frame arriba de la ventana
#miframe.pack(side="bottom") #posiciona el frame abajo de la ventana

#miframe.pack(side="left", anchor="n")  #Con Anchor posicionamos p.ej. izquierda y arriba
#miframe.pack(side="right", anchor="s") #Con Anchor posicionamos p.ej. iderecha y abajo

#miframe.pack(fill="x")  #Expande el frame horizontalmente a todoa la ventana raiz
#miframe.pack(fill="y")  #Coloca el frame en el medio de la pantalla pe no lo expande a lo largo
#miframe.pack(fill="y", expand="True") #de esta forma expande el frame a lo alto de la ventana raiz
#miframe.pack(fill="both", expand="True")  #El frame se expande a toda la ventana raiz

#miframe.config(bd=15)    #con bd le especificamos el tamaño del border a utilizar
miframe.config(relief="sunken")  # con relief especificamos el tipo de borde a aplicar

miframe.config(cursor="pirate")  #Para cambiar la forma del cursor del mouse usamos cursor=




raiz.mainloop()