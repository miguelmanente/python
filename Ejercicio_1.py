#DECLARACIÓN DE VARIABLES 
"""mi_variable = 1
print("Este es mi número:",mi_variable)
MiVariable = 15 
print("Este es mi nuevo  numero:",MiVariable)"""

#USO DE WHILE
"""while mi_variable <= 10:
        print (mi_variable)
        mi_variable = mi_variable +1"""

#otro ejemplo - Serie de fibonacci

""" a, b = 0, 1
while b < 10:
        print(b, end=' ')
        a, b = b, a+b """


#USO DE FOR  (END ="" SE USA PARA MOSTRAR EN CONSOLA EL RESULTADO EN HORIZONTAL)
""" for numeros in range(10):
        print (numeros, end=' ')"""

#USO DE OPERADORES MATEMÁTICOS
#OPERADOR DE  MÓDULO RESTO
"""
a = 10
b = 3

resultado = a % b
print(resultado) """

#OPERADOR DE DIVISIÓN ENTERA 
"""
a = 10
b = 3

resultado = a // b
print(resultado) 
"""

#funcion que vienen con el programa python
"""a = '12.78'
b = 12.987

print (eval(a))   #para numeros decimales se usa eval convierte el string en numero

print (int(b))   #para numeros sin decimales se usa eval convierte el string en numero

print(round(b,2)) #redondea un numero a la cantidad de decimales que  el progrmador quiera en este caso 2"""

c = -130
d = -546.78
print (abs(c))  #valor  absoluto de un numero entero o decimal
print (abs(d))

d, e, f , g = 200, 150, 350, 50

print (max(d,e,f,g))

print (min(d,e,f,g))

h = 27
i = 3
j = 125

print (pow(i,3))

print (round(pow(h,1/3)))

print (pow(j,1/3))




#ENTRADA DE DATOS 
#USO DE INT PARA CONVERTIR TEXTO EN UN NÚMERO ENTERO

"""cantProductos = int(input("Ingrese la cantidad de productos: "))
precioProductos= int(input("Ingrese el precio por unidad: "))

resultado =  cantProductos * precioProductos

print(precioProductos," x ", cantProductos," = ", resultado)"""

#USO DE DECIMALES CON IMPRESIÓN DE 2 DECIMALES
""" cantProductos = int(input("Ingrese la cantidad de productos: "))
precioProductos= float(input("Ingrese el precio por unidad: "))

resultado =  cantProductos * precioProductos

print(precioProductos," x ", cantProductos," = ","{:.2f}".format(resultado)) """

#LISTAS (ARRAYS)

""" miVector = ['Hola', 'Miguel', 62, 'años']

for dato in miVector:
    print(dato, end=' ') """

#con uso de len que nos da la longitud de  la cadena de caracteres
""" miVector = ['Hola', 'Miguel', 'años']

for dato in miVector:
   print(dato, len(dato)) """
