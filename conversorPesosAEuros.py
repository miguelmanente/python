class ConversorPesosAEuros():

    def __init__(self, valorMoneda, cantidadMoneda, tipoMoneda, monedaconvertida):
        self.valorEuro = valorMoneda
        self.cantidadPesos = cantidadMoneda
        self.tipoMoneda = tipoMoneda
        self.monedaCovertida = monedaconvertida
     

    def calculoEuro(self, valorMoneda, cantidadMoneda, tipoMoneda, monedaConvertida):
        totalMoneda =  cantidadMoneda / valorMoneda
        print("La cantidad de ", cantidadMoneda, " ", tipoMoneda, " en ", monedaConvertida, " es: ", totalMoneda)
    

cantidadBilletes = ConversorPesosAEuros(1550, 930000, 'moneda', 'cantidad')

print("Ingrese que conversión de divisas desea realizar:  -Pesos a Euros(pe) - Euros a Pesos(ep)")

tipoMoneda = input("Ingrese tipo de moneda a convertir? ")

monedaCovertida = input("Ingrese el tipo de moneda en que va a convertir? ")

valorMoneda = int(input("Ingrese el valor de la moneda en que va a convertir? "))

cantidadMoneda = int(input("Ingrese la cantidad de la moneda que convertira: "))

cantidadBilletes.calculoEuro(valorMoneda, cantidadMoneda, tipoMoneda, monedaCovertida)















































