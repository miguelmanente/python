class ConversorPesosAEuros():

    def __init__(self, valorMoneda, cantidadMoneda, tipoMoneda, monedaconvertida):
        self.valorEuro = valorMoneda
        self.cantidadPesos = cantidadMoneda
        self.tipoMoneda = tipoMoneda
        self.monedaCovertida = monedaconvertida
     

    def calculoMoneda(self, valorMoneda, cantidadMoneda, tipoMoneda, monedaConvertida):
        totalMoneda =  cantidadMoneda / valorMoneda
        print(f"La cantidad de {cantidadMoneda} {tipoMoneda} son {totalMoneda} {monedaConvertida}")
    
    def calculoMoneda1(self, valorMoneda, cantidadMoneda, tipoMoneda, monedaConvertida):
        totalMoneda =  cantidadMoneda * valorMoneda
        print(f"La cantidad de {cantidadMoneda} {tipoMoneda} son {totalMoneda} {monedaConvertida}")

cantidadBilletes = ConversorPesosAEuros(0, 0, 'tipoMoneda', 'monedaConvertida')

print("  ")
tipoCambio = input("Ingrese que operacion desea realizar Comprar/Vender: ")
print(" ")
tipoMoneda = input("Ingrese tipo de moneda a comprar/vender? ")
print(" ")
monedaConvertida = input("Ingrese el tipo de moneda en que quiere los billetes? ")
print(" ")
valorMoneda = int(input("Ingrese el valor de la moneda que va comprar/vender? "))
print(" ")
cantidadMoneda = int(input("Ingrese la cantidad de billetes que desea comprar/vender: "))
print(" ")

if tipoCambio == 'vender':
    cantidadBilletes.calculoMoneda1(valorMoneda, cantidadMoneda, tipoMoneda, monedaConvertida)
else:
    cantidadBilletes.calculoMoneda(valorMoneda, cantidadMoneda, tipoMoneda, monedaConvertida)















































