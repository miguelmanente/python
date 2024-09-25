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
""" Diseñar un programa que genere e imprima todas las combinaciones posibles de tres dados 

dado = [1, 2, 3, 4, 5, 6]
x = 0
for i in dado:
    
    for j in dado:
        for z in dado:
            x += 1
            print (x, end="   ")
            print (i, end=" ")
            print (j,end=" ")
            print (z)

"""

# EJERCICIO Nº 3
""" Escriba cuatro programas que imprima cada uno una caja, un óvalo, una flecha y un diamante
como los siguientes. Ayuda: usar for() y switch() para determinar la línea a imprimir. """

for x in range(9):
    if x>=0 and x<=9:
        print ("*", end="")
for x in range(1):
        print ("\n*       *")
    
