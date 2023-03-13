#DEFINICION DEL MÉTODO DE INSERCION
""" Este algoritmo, al igual que la clasificación por selección, separa la lista en dos partes, ordenadas y no ordenadas. 
    También suponemos que el primer elemento está ordenado, luego pasamos al siguiente elemento que lo vamos a llamar X, 
    comparamos X con el primero, si es mayor, se queda como está pero si es más pequeño, copiamos el primer elemento en la 
    segunda posición e insertamos X como primero. """

def ordenInsercion(array):
    #Entendemos que el 1er elemento  sin ordenar es el más pequeño
    #asi que comenzamos con el segundo
    for i in range(1, len(array)):
        insertarNumero = array[i]
        # Guardamos en j el indice del elemento anterior
        j = i - 1
        #Movemos todos los elementos de la lista hacia delante si son 
        #mayores que el elemento a insertar
        while j >= 0 and array[j] > insertarNumero:
            array[j + 1] = array[j]
            j -= 1
            #Insertamos el elemnto
            array[j + 1] = insertarNumero

#comprobamos el funcionamiento
vector = [5, 2, 1, 8, 4]
print ('Lista sin ordenar: ' + str(vector))
ordenInsercion(vector)
print ('Lista ordenada: ' + str(vector))