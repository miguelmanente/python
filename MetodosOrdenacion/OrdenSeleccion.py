# ORDEN DE SELECCIÓN (SELECTION SORT)

""" Este algoritmo separa la lista en dos partes, ordenada y no ordenada. Continuamente “elimina” el elemento más pequeño de la parte sin ordenar y lo agrega a la parte ordenada.
Lo que realmente realiza este algoritmo es tratar la parte izquierda de la lista como la parte ordenada buscando en toda la lista el elemento más pequeño y poniéndolo el primero.
Después, sabiendo que ya tenemos el elemento más pequeño el primero, buscamos en toda la lista el elemento más pequeño de los restantes sin ordenar y lo intercambiamos con el 
siguiente ordenado y así hasta acabar con la lista. Cuantos más elementos tengamos ordenados, menos elementos tendremos que examinar. """

def ordenSeleccion(array):
    #el valor de i corresponde al numero de datos que se ordenaron
    for i in range(len(array)):
        #Entendemos que el 1er elemento sin ordenar es el más pequeño
        numeroMenor = i
        #Este bucle  trabaja  sobre los elementos no clasificados
        for j in range(i+1, len(array)):
            if array[j] < array[numeroMenor]:
                numeroMenor = j
        # Intercambio el valor del elemento sin ordenar mas bajo
        # con el primero sin ordenar
        array[i], array[numeroMenor] = array[numeroMenor], array[i]

#Comprobamos el funcionamiento
vector = [5, 2, 1, 8, 4]
print ('Lista sin ordenar: ' + str(vector))
ordenSeleccion(vector)
print ('Lista ordenada: ' + str(vector))



