def ordena(array):

    cant = len(array)

    for i in range(cant-1):
        for j in range(cant-1-i):
            if(array[j]>array[j+1]):
                aux = array[j]
                array[j] = array[j+1]
                array[j+1] = aux

    for i in array:
        print (i, end=' ')