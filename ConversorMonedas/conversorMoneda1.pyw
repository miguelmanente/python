from tkinter import *
from tkinter import font, messagebox


class ConversorMoneda(Frame):
    def __init__(self, master=None, ):
        super().__init__(master, bg="#E5D9F2")
        self.master=master
        self.pack()
        self.crearControles()
     
    def calculoMoneda(self):
        self.vMoneda = self.txtVendeMoneda.get()
        self.cMoneda = self.txtCompraMoneda.get()

        if self.vMoneda == 'Pesos' and self.cMoneda == 'Euros' or  self.vMoneda == 'Pesos' and self.cMoneda == 'Dolares':
            self.n1 = self.txtCantAvender.get()
            self.n2 = self.txtCantAComprar.get()
            self.r = float(self.n1) / float(self.n2)
            self.txtTotal.delete(0, 'end')
            self.txtTotal.insert(0,self.r)
        
        elif self.vMoneda == 'Euros' and self.cMoneda == 'Pesos' or  self.vMoneda == 'Dolares' and self.cMoneda == 'Pesos':
            self.n1 = self.txtCantAvender.get()
            self.n2 = self.txtCantAComprar.get()
            self.r = float(self.n1) * float(self.n2)
            self.txtTotal.delete(0, 'end')
            self.txtTotal.insert(0,self.r)
        elif self.vMoneda == 'Euros' and self.cMoneda == 'Dolares' or  self.vMoneda == 'Dolares' and self.cMoneda == 'Euros':
            self.n1 = self.txtCantAvender.get()
            self.n2 = float(self.txtCantAComprar.get())
            self.r = float(self.n1) * float(self.n2)
            self.txtTotal.delete(0, 'end')
            self.txtTotal.insert(0,self.r)
        else:
            messagebox.showwarning("ERROR", "Hay campos sin LLENAR!!! o Están mal escritos")
    
    def limpiarDatos(self):
        self.txtVendeMoneda.delete(0, END)
        self.txtCompraMoneda.delete(0, END)
        self.txtCantAvender.delete(0, END)
        self.txtCantAComprar.delete(0, END)
        self.txtTotal.delete(0, END)


    def crearControles(self):
        #Creación de controles
        frameTitulo = Frame(ventana, width=925, height=50)
        frameTitulo.place(x=10, y=4)

        lblTitulo = Label(frameTitulo, text="CONVERTIR MONEDAS PESOS, EUROS, DÓLARES", bg="white", fg="black", font="Arial 18 bold")
        lblTitulo.place(x=450, y=25, anchor='center')

        frameControles = Frame(ventana, width=800, height=30)
        frameControles.place(x=10, y=80)
        self.lblVendeMoneda = Label(frameControles, text="Moneda a Vender: ", bg="#8967B3", fg="white", font="Arial 14 bold")
        self.txtVendeMoneda = Entry(frameControles, bg="#D2E0FB", font="Arial 14 bold")
        self.lblCompraMoneda = Label(frameControles, text="Moneda a Comprar: ", bg="#8967B3", fg="white", font="Arial 14 bold")
        self.txtCompraMoneda = Entry(frameControles, bg="#D2E0FB", font="Arial 14 bold")
        self.lblCantAVender = Label(frameControles, text="Cantidad a Vender: ", bg="#8967B3", fg="white", font="Arial 14 bold")
        self.txtCantAvender = Entry(frameControles, bg="#D2E0FB", font="Arial 14 bold")
        self.lblCantAComprar = Label(frameControles, text="Valor Moneda a comprar: ", bg="#8967B3", fg="white", font="Arial 14 bold")
        self.txtCantAComprar = Entry(frameControles, bg="#D2E0FB", font="Arial 14 bold")
        self.lblTotal = Label(frameControles, text="Total Dinero: ", bg="#8967B3", fg="white", font="Arial 14 bold")
        self.txtTotal = Entry(frameControles, bg="#D2E0FB", font="Arial 14 bold")
        
        #Posicionamientos de Controles
        #self.lblTitulo.pack()

        self.lblVendeMoneda.grid(row=3, column=0, padx=5, pady=10, ipady=4)
        self.txtVendeMoneda.grid(row=3, column=1, padx=5, pady=10, ipady=4)
        self.lblCompraMoneda.grid(row=3, column=2, padx=5, pady=10, ipady=4)
        self.txtCompraMoneda.grid(row=3, column=3, padx=5, pady=10, ipady=4)
        self.lblCantAVender.grid(row=5, column=0, padx=5, pady=10, ipady=4)
        self.txtCantAvender.grid(row=5, column=1, padx=5, pady=10, ipady=4)
        self.lblCantAComprar.grid(row=5, column=2, padx=5, pady=10, ipady=4)
        self.txtCantAComprar.grid(row=5, column=3, padx=5, pady=10, ipady=4)
        self.lblTotal.grid(row=6, column=0, padx=5, pady=10, ipady=4)
        self.txtTotal.grid(row=6, column=1, padx=5, pady=10, ipady=4)

        #Botón para calcular el total de moneda convertida
        self.btnConvertir = Button(frameControles, text="Convertir", bg="#2E236C", fg="white", font="Arial 14 bold", command=self.calculoMoneda)
        self.btnConvertir.grid(row=6, column=2, padx=5, pady=10, ipady=4 )

        self.btnLimpiar = Button(frameControles, text="Limpiar Datos", bg="#2E236C", fg="white", font="Arial 14 bold", command=self.limpiarDatos)
        self.btnLimpiar.grid(row=6, column=3, padx=5, pady=10, ipady=4 )
      
ventana = Tk()
ventana.geometry("950x350")
ventana.title("Conversor de monedas extranjeras")
ventana.config(bg="#E5D9F2")
app = ConversorMoneda(ventana)

app.mainloop()

