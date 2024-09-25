# ORDENAMIENTO DE BURBUJAS (BUBBLE SORT)
""" Este algoritmo de clasificación simple itera sobre la lista de datos, comparando elementos en pares hasta que los elementos más grandes “burbujean” hasta el final 
    de la lista y los más pequeños permanecen al principio. Comienza comparando los dos primeros elementos de la lista, si el primer elemento es mayor que el segundo, 
    los intercambiamos, si no, se quedan como están. Luego pasamos al siguiente par de elementos, los comparamos e intercambiamos si fuera necesario.  """

array =[76, 24, 15, 6, 16, 25, 5]

cant = len(array)

for i in range(cant-1):
    for j in range(cant-1-i):
        if(array[j]>array[j+1]):
            aux = array[j]
            array[j] = array[j+1]
            array[j+1] = aux

for i in array:
    print (i, end=' ')


