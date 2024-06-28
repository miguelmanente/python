#Llenar una matriz cuadrada de 3 filas y columnas con números aleatorios
'''
from random import randint

matriz =[]

for i in range(3):
    fila = []
    
    for j in range(3):
        fila.append(randint(1,100))

    matriz.append(fila)
print(matriz, sep =" ")
'''
#Llenar una matriz no cuadrada que las filas y las columnas se ingresen desde el teclado 

from random import randint

matriz = []

fila = int(input("Ingrese el número de filas de la matriz "))
columna = int(input("Ingrese la cantidad de columnas de la matriz "))

for i in range(fila):
    filas = []

    for j in range(columna):
        filas.append(randint(1,100))

    matriz.append(filas)

print(matriz)    
