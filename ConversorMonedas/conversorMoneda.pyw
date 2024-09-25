from tkinter import *
from tkinter import font

class ConversorMoneda(Frame):
    def __init__(self, master=None):
        super().__init__(master, bg="#E5D9F2")
        self.master=master
        self.pack()
        self.crearControles()
     
    def calculoMoneda(self):
        self.n1 = self.text1.get()
        self.n2 = self.text2.get()
        self.r = float(self.n1) / float(self.n2)
        self.text3.delete(0, 'end')
        self.text3.insert(0,self.r)
      
    def calculoMoneda1(self):
        self.n1 = self.text4.get()
        self.n2 = self.text5.get()
        self.r = float(self.n1) * float(self.n2)
        self.text6.delete(0, 'end')
        self.text6.insert(0,self.r)

    def calculoMoneda2(self):
        self.n1 = self.text7.get()
        self.n2 = self.text8.get()
        self.r = float(self.n1) / float(self.n2)
        self.text9.delete(0, 'end')
        self.text9.insert(0,self.r)
    
    def calculoMoneda3(self):
        self.n1 = self.text10.get()
        self.n2 = self.text11.get()
        self.r = float(self.n1) * float(self.n2)
        self.text12.delete(0, 'end')
        self.text12.insert(0,self.r)

    def crearControles(self):
        #primera fila de controles pesos a euros
        self.lblTitulo = Label(self, text="CONVERTIR PESOS A EUROS", bg="#8967B3", fg="white")
        self.lbl1 = Label(self, text = "Cantidad de Pesos: ", bg="#8967B3", fg="white")
        self.text1 = Entry(self, bg="#D2E0FB")
        self.lbl2 = Label(self, text="Valor del Euro", bg="#8967B3", fg="white")
        self.text2 = Entry(self, bg="#D2E0FB")
        self.lbl3 = Label(self, text="Total ", bg="#8967B3", fg="white")
        self.text3 = Entry(self, bg="#D2E0FB")
        self.btn1 = Button(self, text="Convertir", bg="#2E236C", fg="white", command=self.calculoMoneda)
        #primera fila de controles pesos a euros
        self.lblTitulo.grid(row=0, column=0)
        self.lbl1.grid(row=1, column=0, padx=2, pady=10, ipady=4)
        self.text1.grid(row=1, column=1, padx=2, pady=10, ipady=4)
        self.lbl2.grid(row=1, column=2, padx=2, pady=10, ipady=4)
        self.text2.grid(row=1, column=3, padx=2, pady=10, ipady=4)
        self.lbl3.grid(row=1, column=4, padx=2, pady=10, ipady=4)
        self.text3.grid(row=1, column=5, padx=2, pady=10, ipady=4)
        self.btn1.grid(row=1, column=6, padx=2, pady=10, ipady=1)
        
        #Segunda fila de controles euros a pesos
        self.lbl1Titulo = Label(self, text="CONVERTIR EUROS A PESOS", bg="#8967B3", fg="white")
        self.lbl4 = Label(self, text = "Cantidad de euros: ", bg="#8967B3", fg="white")
        self.text4 = Entry(self, bg="#D2E0FB")
        self.lbl5 = Label(self, text="Valor del Euro", bg="#8967B3", fg="white")
        self.text5 = Entry(self, bg="#D2E0FB")
        self.lbl6 = Label(self, text="Total ", bg="#8967B3", fg="white")
        self.text6 = Entry(self, bg="#D2E0FB")
        self.btn2 = Button(self, text="Convertir", bg="#2E236C", fg="white", command=self.calculoMoneda1)
        #pSegunda fila de controles EUROS a PESOS
        self.lbl1Titulo.grid(row=2, column=0)
        self.lbl4.grid(row=3, column=0, padx=2, pady=15, ipady=4)
        self.text4.grid(row=3, column=1, padx=2, pady=15, ipady=4)
        self.lbl5.grid(row=3, column=2, padx=2, pady=15, ipady=4)
        self.text5.grid(row=3, column=3, padx=2, pady=15, ipady=4)
        self.lbl6.grid(row=3, column=4, padx=2, pady=15, ipady=4)
        self.text6.grid(row=3, column=5, padx=2, pady=15, ipady=4)
        self.btn2.grid(row=3, column=6, padx=2, pady=15, ipady=1)

        #Tercera fila de controles pesos a dolares 
        self.lbl2Titulo = Label(self, text="CONVERTIR PESOS A DOLARES", bg="#8967B3", fg="white")
        self.lbl7 = Label(self, text = "Cantidad de pesos: ", bg="#8967B3", fg="white")
        self.text7 = Entry(self, bg="#D2E0FB")
        self.lbl8 = Label(self, text="Valor del dólar", bg="#8967B3", fg="white")
        self.text8 = Entry(self, bg="#D2E0FB")
        self.lbl9 = Label(self, text="Total ", bg="#8967B3", fg="white")
        self.text9 = Entry(self, bg="#D2E0FB")
        self.btn3 = Button(self, text="Convertir", bg="#2E236C", fg="white", command=self.calculoMoneda2)
        #Tercera fila de controles pesos a dolares
        self.lbl2Titulo.grid(row=4, column=0)
        self.lbl7.grid(row=5, column=0, padx=2, pady=10, ipady=4)
        self.text7.grid(row=5, column=1, padx=2, pady=10, ipady=4)
        self.lbl8.grid(row=5, column=2, padx=2, pady=10, ipady=4)
        self.text8.grid(row=5, column=3, padx=2, pady=10, ipady=4)
        self.lbl9.grid(row=5, column=4, padx=2, pady=10, ipady=4)
        self.text9.grid(row=5, column=5, padx=2, pady=10, ipady=4)
        self.btn3.grid(row=5, column=6, padx=2, pady=10, ipady=1)

        #Cuarta fila de controles dolares a pesos
        self.lbl3Titulo = Label(self, text="CONVERTIR DOLARES A PESOS", bg="#8967B3", fg="white")
        self.lbl10 = Label(self, text = "Cantidad de dólares: ", bg="#8967B3", fg="white")
        self.text10 = Entry(self, bg="#D2E0FB")
        self.lbl11 = Label(self, text="Valor del dólar", bg="#8967B3", fg="white")
        self.text11 = Entry(self, bg="#D2E0FB")
        self.lbl12 = Label(self, text="Total ", bg="#8967B3", fg="white")
        self.text12 = Entry(self, bg="#D2E0FB")
        self.btn4 = Button(self, text="Convertir", bg="#2E236C", fg="white", command=self.calculoMoneda3)
        #Cuarta fila de controles dolares pesos
        self.lbl3Titulo.grid(row=6, column=0)
        self.lbl10.grid(row=7, column=0, padx=2, pady=10, ipady=4)
        self.text10.grid(row=7, column=1, padx=2, pady=10, ipady=4)
        self.lbl11.grid(row=7, column=2, padx=2, pady=10, ipady=4)
        self.text11.grid(row=7, column=3, padx=2, pady=10, ipady=4)
        self.lbl12.grid(row=7, column=4, padx=2, pady=10, ipady=4)
        self.text12.grid(row=7, column=5, padx=2, pady=10, ipady=4)
        self.btn4.grid(row=7, column=6, padx=2, pady=10, ipady=1)
       
ventana = Tk()
ventana.geometry("800x350")
ventana.title("Conversor de monedas extranjeras")
ventana.config(bg="#E5D9F2")
app = ConversorMoneda(ventana)

app.mainloop()

