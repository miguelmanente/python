#Crear y leer archivo de texto 
'''
file = open('Archivos/data.txt','r')   #abro el archivo
# print(file)
lineas = file.readlines()       #leo el archivo linea x lineas
print(lineas)
file.close()   #cierra el archivo
'''
'''
#Crear y leer archivo de texto usando with(no cierra el archivo automaticamente)
ruta = 'Archivos/data.txt'
with open(ruta,'r') as archivo:       #abro el archivo
    lineas = archivo.readlines()   #leo el archivo linea x lineas
    # print(lineas)

#print(lineas)     #como vemos fuera de la estructura ya se cerro el archivo y yo puedo seguir viendo la información

for i in lineas:
    print(i.replace('\n',''))   #reemplaza \n por espacios en blanco
'''
'''
# otra forma de eliminar \n del final de cada linea y quedando una lista terminada
ruta = 'Archivos/data.txt'
with open(ruta,'r') as archivo: 
    contenido =archivo.read()
    lineas = contenido.split('\n')  #saca lo \n del final de cada linea quedando una lista para trabajar
    print(lineas)
'''

'''
#Para saber la posición del archivo en que estamos usamos
ruta = 'Archivos/data.txt'
with open(ruta,'r') as archivo: 
    #pos = archivo.tell()   #en este lugar nos 0(cero) por que todavía no leimos el archivo
    #print(pos)

    contenido =archivo.read()
    lineas = contenido.split('\n')
    pos = archivo.tell()    #en este lugar nos 43 por que leimos el archivo y el cursor se ubico al final
    print(pos)
    print('El archivo tiene {0} caracteres de longitud '.format(pos))
'''


'''
# Ubicar el cursor en una posición deseada con seek
ruta = 'Archivos/data.txt'
with open(ruta,'r') as archivo: 
    archivo.seek(12)    #Ubica el cursor a partir de esa posición en este caso no muestra ni python y java
    pos = archivo.tell()
    print(pos)
    contenido = archivo.read()
    lineas = contenido.split('\n')
    print(lineas)
'''
# Crear y escribir un nuevo archivo .txt con write
ruta = 'Archivos/data1.txt'
with open(ruta,'w') as archivo:             # Se crea archivo si no existe lo crea
    archivo.write('Miguel\nAngel\nManente')     # Almacena en el archivo creado los datos con write

with open(ruta,'a') as archivo:                     # Habilita al archivo para agregar (a) datos al archivo            
    archivo.write('\nBelkis\nGuadalupe\nSioli')     # Agrega los datos con write al archivo

with open(ruta,'r') as archivo1:  #leer archivo creado
    lineas = archivo1.read()                            
    contenido =lineas.split('\n')       # Al final de cada líneas elimina \n y se mostraran un al lado del otro
    print(contenido)
