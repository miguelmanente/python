#COMBIMAR ODEN (MERGE SORT)
""" Este algoritmo comienza dividiendo la lista en dos, luego esas dos mitades en 4 y así sucesivamente hasta que 
    tengamos listas de un elemento de longitud. Después, estos elementos se vuelven a unir en orden. Primero 
    fusionaremos los elementos individuales en pares de nuevo ordenándolos entre sí, luego seguiremos ordenándolos
    en grupos hasta que tengamos una sola lista ordenada. """

def merge(listaIzq, listaDer):
    listaOrdenada = []
    indiceListaIzq = indiceListaDer = 0
    #Creamos variables para las longitudes de la lista
    largoListaIzq, largoListaDer = len(listaIzq), len(listaDer)

    for _ in range(largoListaIzq + largoListaDer):
        if indiceListaIzq < largoListaIzq and indiceListaDer < largoListaDer:
            # Comprobamos el valor de cada elemento inicial de las listas para ver
            # cual es menor. Si el elemento al principio de la lista izquierda es más 
            # pequeño, se añade a la lista ordenada
            if listaIzq[indiceListaIzq] <= listaDer[indiceListaDer]:
                listaOrdenada.append(listaIzq[indiceListaIzq])
                indiceListaIzq += 1
            # Si el elemento al principio de la lista de la derecha es más pequeño,
            # se añade a la lista ordenada
            else:
                listaOrdenada.append(listaDer[indiceListaDer])
                indiceListaDer += 1

        #Si llegamos al final de la lista de la izquierda, añadimos los elementos
        # de la lista de la derecha

        elif indiceListaIzq == largoListaIzq:
            listaOrdenada.append(listaDer[indiceListaDer])
            indiceListaDer += 1
        #Si llegamos al final de la lista de la derecha, añadimos los elementos
        #de la lista de la izquierda
        elif indiceListaDer == largoListaDer:
            listaOrdenada.append(listaIzq[indiceListaIzq])
            indiceListaIzq += 1
    return listaOrdenada

def mergeSort(numero):
    # Si la lista tiene un solo elemento, devuélvelo
    if len(numero) <= 1:
        return numero
    # Obtenenmos el indice medio para separar la lista en dos
    medio = len(numero) // 2
    #Ordenamos y fusionamos cada mitad
    listaIzq = mergeSort(numero[:medio])
    listaDer = mergeSort(numero[medio:])
    #Fusionamos las listas ordenadas en una nueva ordenada
    return merge(listaIzq, listaDer)

#Comprobamos el funcionamiento
vector = [5, 2, 1, 8, 4]
print ('Lista sin ordenar: ' + str(vector))
vector = mergeSort(vector)
print ('Lista ordenada: ' + str(vector))

