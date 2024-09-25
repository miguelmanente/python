class ConversorPesosAEuros():

    def __init__(self, valorMoneda, cantidadMoneda, tipoMoneda, monedaconvertida):
        self.valorEuro = valorMoneda
        self.cantidadPesos = cantidadMoneda
        self.tipoMoneda = tipoMoneda
        self.monedaConvertida = monedaconvertida
     

    def calculoMoneda(self, valorMoneda, cantidadMoneda, tipoMoneda, monedaConvertida):
        totalMoneda =  cantidadMoneda / valorMoneda
        print(f"La cantidad de {cantidadMoneda} {tipoMoneda} son {totalMoneda} {monedaConvertida}")
    
    def calculoMoneda1(self, valorMoneda, cantidadMoneda, tipoMoneda, monedaConvertida):
        totalMoneda =  cantidadMoneda * valorMoneda
        print(f"La cantidad de {cantidadMoneda} {tipoMoneda} son {totalMoneda} {tipoMoneda1}")

cantidadBilletes = ConversorPesosAEuros(0, 0, 'tipoMoneda', 'monedaConvertida')

print("  ")
tipoCambio = input("Ingrese que operacion desea realizar Comprar y/o Vender: ")
print(" ")
tipoMoneda = input("Ingrese tipo de moneda a vender? ")
print(" ")
tipoMoneda1 = input("Ingrese tipo de moneda a comprar? ")
print(" ")

if tipoCambio == 'vender':
    valorMoneda = float(input(f"Ingrese el valor de la moneda ({tipoMoneda}) que va {tipoCambio}? "))
    print(" ")
    cantidadMoneda = float(input(f"Ingrese la cantidad de ({tipoMoneda})que desea {tipoCambio}: "))
    print(" ")
    cantidadBilletes.calculoMoneda1(valorMoneda, cantidadMoneda, tipoMoneda, tipoMoneda1)
else:
    print(" ")
    valorMoneda = float(input(f"Ingrese el valor de la moneda ({tipoMoneda1})que va a comprar? "))
    print(" ")
    cantidadMoneda = float(input(f"Ingrese la cantidad de ({tipoMoneda}) que desea vender: "))
    print(" ")
    cantidadBilletes.calculoMoneda(valorMoneda, cantidadMoneda, tipoMoneda, tipoMoneda1)















































