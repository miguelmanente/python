from tkinter import *
from tkinter import font, messagebox
import requests


ventana = Tk()
ventana.geometry("950x350")
ventana.title("Conversor de monedas extranjeras")
ventana.config(bg="#E5D9F2")


API_KEY = '6fce5ca7f3e13df5983d2d05'
URL = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD'


def get_rates():
    response = requests.get(URL)
    data = response.json()


    if response.status_code != 200:
        messagebox.showwarning('ERROR','Error al obtener las tasas de cambio')
        return None
    return data['conversion_rates']

def convert_currency(amount, from_currency, to_currency, rates):
    if from_currency != 'USD':
        amount = amount / float(rates[from_currency])
    return amount * rates[to_currency]

def main():
    rates = get_rates()
    if rates:
        amount =  float(txtCantAvender.get())
        from_currency = txtVendeMoneda.get()
        to_currency = txtCompraMoneda.get()

        resultado = convert_currency(amount, from_currency, to_currency, rates)
        resultado1 = f"{resultado:.2f}"
        txtTotal.insert(0,resultado1)
        vMoneda  = rates[from_currency]
        vMoneda1 = f"{vMoneda:.2f}"
        txtCantAComprar.insert(0, vMoneda1)
       

def limpiarDatos():
    txtVendeMoneda.delete(0, END)
    txtCompraMoneda.delete(0, END)
    txtCantAvender.delete(0, END)
    txtCantAComprar.delete(0, END)
    txtTotal.delete(0, END)


#Creación de controles
frameTitulo = Frame(ventana, width=925, height=50)
frameTitulo.place(x=10, y=4)

lblTitulo = Label(frameTitulo, text="CONVERTIR MONEDAS PESOS, EUROS, DÓLARES", bg="white", fg="black", font="Arial 18 bold")
lblTitulo.place(x=450, y=25, anchor='center')

frameControles = Frame(ventana, width=800, height=30)
frameControles.place(x=10, y=80)
lblVendeMoneda = Label(frameControles, text="Moneda a Vender: ", bg="#8967B3", fg="white", font="Arial 14 bold")
txtVendeMoneda = Entry(frameControles, bg="#D2E0FB", font="Arial 14 bold")
lblCompraMoneda = Label(frameControles, text="Moneda a Comprar: ", bg="#8967B3", fg="white", font="Arial 14 bold")
txtCompraMoneda = Entry(frameControles, bg="#D2E0FB", font="Arial 14 bold")
lblCantAVender = Label(frameControles, text="Cantidad a Vender: ", bg="#8967B3", fg="white", font="Arial 14 bold")
txtCantAvender = Entry(frameControles, bg="#D2E0FB", font="Arial 14 bold")
lblCantAComprar = Label(frameControles, text="Valor Moneda a comprar: ", bg="#8967B3", fg="white", font="Arial 14 bold")
txtCantAComprar = Entry(frameControles, bg="#D2E0FB", font="Arial 14 bold")
lblTotal = Label(frameControles, text="Total Dinero: ", bg="#8967B3", fg="white", font="Arial 14 bold")
txtTotal = Entry(frameControles, bg="#D2E0FB", font="Arial 14 bold")

#Posicionamientos de Controles

lblVendeMoneda.grid(row=3, column=0, padx=5, pady=10, ipady=4)
txtVendeMoneda.grid(row=3, column=1, padx=5, pady=10, ipady=4)
lblCompraMoneda.grid(row=3, column=2, padx=5, pady=10, ipady=4)
txtCompraMoneda.grid(row=3, column=3, padx=5, pady=10, ipady=4)
lblCantAVender.grid(row=5, column=0, padx=5, pady=10, ipady=4)
txtCantAvender.grid(row=5, column=1, padx=5, pady=10, ipady=4)
lblCantAComprar.grid(row=5, column=2, padx=5, pady=10, ipady=4)
txtCantAComprar.grid(row=5, column=3, padx=5, pady=10, ipady=4)
lblTotal.grid(row=6, column=0, padx=5, pady=10, ipady=4)
txtTotal.grid(row=6, column=1, padx=5, pady=10, ipady=4)

#Botón para calcular el total de moneda convertida
btnConvertir = Button(frameControles, text="Convertir", bg="#2E236C", fg="white", font="Arial 14 bold", command=main)
btnConvertir.grid(row=6, column=2, padx=5, pady=10, ipady=4 )

btnLimpiar = Button(frameControles, text="Limpiar Datos", bg="#2E236C", fg="white", font="Arial 14 bold", command=limpiarDatos)
btnLimpiar.grid(row=6, column=3, padx=5, pady=10, ipady=4 )

ventana.mainloop()

