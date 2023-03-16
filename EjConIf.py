""" Escribir un programa que determine si el primero de una lista de tres números dados es menor que los otros dos. 

a = int(input("Ingrese el 1er numero entero: "))
b = int(input("Ingrese el 2do número entero: "))
c = int(input("Ingrese el 3er número entero: "))

if a < b and a < c:
    print("El número ",a," es el menor de los tres números ingresados")
elif b < a and b < c:
    print("El número ",b," es el menor de los tres números ingresados")
elif c < a and c < b:
      print("El número ",c," es el menor de los tres números ingresados") 
else:
     print("No exiten menores")  """

""" Se ingresa por teclado una sucesión no vacía y finita de números positivos, nulos o negativos.
Por medio de un programa determinar la cantidad de números positivos que se presentan antes
del primer número negativo de la sucesión y obtener la suma y el promedio """

num, contPos, contNeg, contIgu = 1, 0, 0, 0

while num <= 10:
    n1 = int(input("Ingrese un número entero positivo, negativo o cero:    "))

    if n1 > 0:
        contPos = contPos + 1
    elif n1 < 0:
        contNeg = contNeg + 1
    else:
        contIgu = contIgu + 1
    
    num += 1

print("Se ingresaron ",contPos," números positivos")
print("Se ingresaron ",contNeg," números negativos")
print("Se ingresaron ",contIgu," números nulos")


