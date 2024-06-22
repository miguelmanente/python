""" function menorMayor(numeros)
La función llamada 'menorMayor' recibe como argumento un arreglo de números llamado 'numeros' y debe devolver un arreglo que 
contenga el menor número del arreglo 'numeros' en la posición cero y el mayor número del arreglo'numeros' en la posición 1.
Ej:
menorMayor([4, 6, 1, 7, 15]) debe retornar [1, 15]
ya que 1 es el número más chico (menor) dentro del arreglo [4, 6, 1, 7, 15]
y 15 es el número más grande (mayor) dentro del arreglo [4, 6, 1, 7, 15] """

def menorMayor(numero):
    cantidad = len(numero)
    menor = numero[0]
    mayor = numero[0]
    array = [0,0]
    
    for i in range(cantidad):
        if numero[i] < menor:
            menor = numero[i]
            array[0] = menor        
        
        if numero[i] > mayor:
            mayor = numero[i]
            array[1] = mayor
        
    return array
print(menorMayor([4, 6, 1, 7, 15]))


