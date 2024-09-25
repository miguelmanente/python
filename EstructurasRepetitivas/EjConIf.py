#EJERCICIO Nº 1
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

# EJERCICIO Nº 2
""" Se ingresa por teclado una sucesión no vacía y finita de números positivos, nulos o negativos.
Por medio de un programa determinar la cantidad de números positivos que se presentan antes
del primer número negativo de la sucesión y obtener la suma y el promedio 

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
"""
# EJERCICIO Nº 3
""" Escribir un programa que determine si una lista de cuatro valores numéricos dada está ordenada de menor a mayor. 

lista = [10, 20, 30 , 40, 50]

cant =len(lista)
num = lista[0]
cv = 0
cf = 0

for i in range(cant):
    if num <= lista[i]:
        num = lista[i]
        cv = cv + 1
    else:
        cf =cf + 1

if cv == cant:
    print("La lista esta ordenada de menor a mayor")
else: 
    print("La lista No está ordenada de menor a mayor")
"""

# EJERCICIO Nº 4
""" Realizar un programa que imprima todos los números primos comprendidos entre el 2 y un
valor límite que se ingresará al ejecutar el programa. 

def es_primo(num):
    if num < 2:     #si es menos que 2 no es primo, por lo tanto devolverá Falso
        return False
    
    for i in range(2, num):  #un rango desde el dos hasta el numero que nosotros elijamos
        if num % i == 0:     #si el resto da 0 no es primo, por lo tanto devuelve Falso
            return False
    
    return True    #de lo contrario devuelve Verdadero


def primos(num1):

    cont = 0

    for i in range(num1):
        if es_primo(i) == True:     #Llamamos a la primera funcion para ahorrar trabajo 😉
            cont += 1               #Que va a determinar si es primo o no
            print (i, end=' ')

    print ("Hay", cont, "numeros primos")       #Total de numeros primos

num1 = int(input("Ingrese hasta donde desea mostrar números primos:  "))

primos(num1)

"""

# EJERCICIO Nº 5

""" Escribir un programa que al ingresar una fecha en formato DD/MM, determine si es válida o no.
Para simplificar la lógica, considerar que el año no es bisiesto. Usar la estructura de control
switch(). """

dia = int(input("Ingrese el día:  "))
mes = int(input("Ingrese el mes del año que desea averiguar:  "))

switch ={                   #SWITCH NO EXISTE EN PYTHON ,PERO SE PUEDE EMULAR USANDO UN DICCIONARIO
    1: "Enero",
    2: "Febrero",
    3: "Marzo",
    4: "Abril",
    5: "Mayo",
    6: "Junio",
    7: "Julio",
    8: "Agosto",
    9: "Setiembre",
    10: "Octubre",
    11: "Noviembre",
    12: "Diciembre"
}

if (dia >= 1 and dia <= 31 and mes >= 1 and mes <= 12):
    nroMes = switch.get(mes,"No es número del mes correcto")    #LLAMADO AL DICCIONARIO USANDO GET Y DOS ARGUMENTOS EL NUMERO DE OPCION Y EL MENSAJE DE ERROR 
    print("El día es: ",dia)
    print("El mes es: ",nroMes)
else:
    print("La fecha solicitada no es correcta")