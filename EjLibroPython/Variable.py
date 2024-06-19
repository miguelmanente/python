
'''
#Crear diferente tipos de variable en python#
#No hace falta avisarle a python de que tipo son las varibles él las detecta

x = 5
print("Esta variable vale: ",x)

#Sumando variables
a = 3
b = 7

print("La suma de ",a," + ",b," es = ",a+b)

#variable tipo string
cadena = "Miguel Angel Manente"
cadena1 = "Estamos aprendiendo Python"
print(cadena+" "+cadena1)
'''

# Definimos una variable x con una cadena
x = "El valor de (a+b)*c es"

# Podemos realizar múltiples asignaciones
a, b, c = 4, 3, 2

# Realizamos unas operaciones con a,b,c
d = (a + b) * c

# Definimos una variable booleana
imprimir = True

# Si imprimir, print()
if imprimir:
    print(x, d)
    print("el resultado es ",end=' ')
    print("de la fórmula de arriba")

# Salida: El valor de (a+b)*c es 14