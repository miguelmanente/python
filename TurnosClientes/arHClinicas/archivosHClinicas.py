import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext as st

def historiasClinicas():
    class Aplicacion:
        def __init__(self):
            self.ventana1=tk.Tk()
            self.scrolledtext1=st.ScrolledText(self.ventana1, width=60, height=20)
            self.scrolledtext1.grid(column=0,row=0, padx=10, pady=10)
            self.copiar()        
            self.ventana1.mainloop()

        def copiar(self):
            iniciofila='1' #self.dato1.get()
            iniciocolumna='0' #self.dato2.get()
            finfila='10' #self.dato3.get()
            fincolumna='50' # self.dato4.get()
            datos=self.scrolledtext1.get(iniciofila+"."+iniciocolumna, finfila+"."+fincolumna)
            caracteres = len(datos)
            self.label1=ttk.Label(self.ventana1, text="cuenta caracteres :")
            self.label1.grid(column=0, row=2, padx=1, pady=60, sticky='w')
            self.label2 = ttk.Label(self.ventana1, text=caracteres-1)
            self.label2.grid(column=0, row=2, padx=100, pady=60, sticky='w')

            self.boton1=ttk.Button(self.ventana1, text="Guardar", command=self.copiar)
            self.boton1.grid(column=1, row=4, padx=10, pady=10)

            ruta = '/Users/migue/OneDrive/Escritorio/Python/TurnosClientes/arHClinicas/hClinicas.txt'
            with open(ruta,'w') as archivo:             # Se crea archivo si no existe lo crea
                archivo.write(datos)
    

    aplicacion1=Aplicacion() 