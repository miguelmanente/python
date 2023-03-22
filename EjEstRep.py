# ESTRUCTURAS REPETITIVAS

# EJERCICIO Nº 1
""" Escribir un programa que calcule y muestre en pantalla los números de la sucesión de Fibonacci.
Para calcular la sucesión de Fibonacci, los dos primeros términos de la serie son 0 y 1, a partir
del tercero, cada término se obtiene sumando los dos términos que lo preceden. 
# CON FOR
fib = 1
aux = 1

cantidad = int(input("Ingrese hasta que numero quiere mostrar la seri de fibonacci:  "))

for i in range(cantidad):
    aux += fib
    fib = aux - fib
    print (fib, end=" ")

# CON WHILE
fib = 1
aux = 1
contador = 1

cantidad = int(input("Ingrese hasta que numero quiere mostrar la seri de fibonacci:  "))

while (contador <= cantidad):
    aux += fib
    fib = aux - fib
    contador += 1
    print (fib, end=" ")

"""

# EJERCICIO Nº 2







