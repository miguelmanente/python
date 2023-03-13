contador = 1

num = int(input('Ingrese un numero entero: '))

maximo = num
minimo = num

while (contador <= 5):
    num = int(input('Ingrese un numero entero: '))

    if(num > maximo):
        maximo = num
    
    if (num < minimo):
        minimo  = num
    contador += 1

print ('El número máximo ingresado es: ', maximo)
print ('El número mínimo ingresado es: ', minimo)