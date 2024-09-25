#Calcular el factorial de un número igresado por teclado

factorial = 1

numero = int(input('Ingrese un número entero por teclado:  '))

numero1 = numero

while (numero > 0):
    factorial = factorial * numero 
    numero -= 1

print('El factorial del número ',numero1,' es: ', factorial)