vector = [12, 5, 1, 6, 10, 20]

print (vector[2:])   #Muestra elementos desde la posición 2 hasta la posición 5   ej: [1, 6, 10, 20]

print (vector[0:3])         #Muestra elementos desde la posición 0 hasta la posición 3 ej:   [12, 5, 1]

print (vector[:4])    #Muestra elementos desde la posición 0 hasta la posición 4  ej: [12, 5, 1, 6]

vector.append(50)   #Agrega al final de la lista el elemento 50

print (vector)   # ej:  [12, 5, 1, 6, 10, 20, 50]

del vector[5]   # Borra el elemento en la posición 5

print (vector)  # Ej: [12, 5, 1, 6, 10, 50]

vector.pop()    # Borra el último elemento de la lista

print (vector)  # Ej: [12, 5, 1, 6, 10]

vector.remove(10)   # Borra el elemento que se deseamos borrar de la lista en este caso es el diez

print (vector) # Ej: [12, 5, 1, 6]

#vector.sort()   #Ordena los elementos de la lista de menor a mayor

print (vector)  # Ej: [1, 5, 6, 12]

print (sorted(vector))   #Ordena temporalmente  la lista 

vector.reverse()    # Invierte los elementos de la lista

print (vector)  # Ej: [6, 1, 5, 12]

cantidad = len(vector)

print (cantidad)





