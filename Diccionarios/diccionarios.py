#Creación de diccionario con {clave y valor}

d0 ={'nombre': 'Miguel', 'apellido':'Manente', 'edad': 64, 'profesion':'Profesor', 'estudio': 'Analista de Sistemas' } #Creación de un diccionario

'''print(d0['nombre'], d0['apellido'], d0['edad'])     #Accedemos y mostramos algunos valores que hay dentro del diccionario
#----------------------------------------------------------------------------------------------------------------------------------------
#Extraer valores del diccionarios a una variable
nombre = d0['nombre']
apellido = d0['apellido']
edad =d0['edad']
profesion = d0['profesion']
estudios = d0['estudio']

print(f'Mi apellido es {apellido} mi nonmbre es {nombre} tengo {edad} años, soy {profesion}, mis estudios son: {estudios}')  # Usamos cadenas f
# 
'''
#----------------------------------------------------------------------------------------------------------------------------------------

'''#Agregar nuevos valores al diccionario

d0['materia'] ='Programación'
d0['antiguedad'] = 22

# ---------------------------------------------------------------------------------------------------------------------------------------
#Modificar valores en un diccionario

d0['nombre'] = 'Miguel Ángel'

print(d0)

#Mostrará en pantalla : {'nombre': 'Miguel Ángel', 'apellido': 'Manente', 'edad': 64, 'profesion': 'Profesor', 'estudio': 'Analista de Sistemas', 'materia': 'Programación', 'antiguedad': 22}

#-----------------------------------------------------------------------------------------------------------------------------------------

#Eliminar pares clave-valor

del d0['antiguedad']
del d0['materia']

print(d0)

#Mostrará en pantalla : {'nombre': 'Miguel Ángel', 'apellido': 'Manente', 'edad': 64, 'profesion': 'Profesor', 'estudio': 'Analista de Sistemas'}
'''
#------------------------------------------------------------------------------------------------------------------------------------------

'''#Uso del get() para acceder a valores

nombre = d0.get('nombre', 'El nombre no existe')
print(nombre)

apellido =d0.get('apellido', 'El apellido no existe')
print(apellido)
'''
#------------------------------------------------------------------------------------------------------------------------------------------
'''
#Pasar en bucle FOR-IN por un diccionario {clave, valor}

for clave, valor in d0.items():
    print(clave,":",valor)

#---------------------------------------------------------------------------------------------------------------------------------------------
#Pasar en bucle por todas las claves del diccionario

for clave in d0.keys():
    print(clave.title())

#------------------------------------------------------------------------------------------------------------------------------------------------
#Pasar en bucle por todas las claves en un orden particular

for clave in sorted(d0.keys()):
    print(clave.title())
'''
#Mostrará en pantalla :
'''
Apellido
Edad
Estudio
Nombre
Profesion
'''
#-----------------------------------------------------------------------------------------------------------------------------------------------

'''
#Pasar en bucle por todas los valores del diccionario

for valor in d0.values():
    print(valor)
'''
#-------------------------------------------------------------------------------------------------------------------------------------------------
'''
#Usamos set()para armar un conjunto de valores sin repetición, es decir sin valores duplicados
for valor in set(d0.values()):
    print(valor)
'''
#------------------------------------------------------------------------------------------------------------------------------------------------
'''
#Creación de LISTAS de DICCIONARIOS
d0 ={'nombre': 'Miguel', 'apellido':'Manente', 'edad': 64, 'profesión':'Profesor', 'estudio': 'Analista de Sistemas' } #Creación de un diccionario
    
d1={'nombre': 'Belkis', 'apellido':'Sioli', 'edad': 60, 'profesión':'Cocinera', 'estudio': 'Primarios'} #Creación de otro diccionario

diccionarios = [d0, d1]   # Creación de una lista de diccionarios

for dic in diccionarios:        # Usando el bucle for - in podemos mostrar la lista de diccionarios creados
    print(dic)

#En pantalla se mostrará:
{'nombre': 'Miguel', 'apellido': 'Manente', 'edad': 64, 'profesión': 'Profesor', 'estudio': 'Analista de Sistemas'}
{'nombre': 'Belkis', 'apellido': 'Sioli', 'edad': 60, 'profesión': 'Cocinera', 'estudio': 'Primarios'}
'''
#------------------------------------------------------------------------------------------------------------------------------------------------

#Creación de Listas de Diccionarios de mayor cantidad
'''
dic = []    #creación de lista vacía

#Agregamos un primer diccionario a la lista dic
for dic1 in range(1):
    d0 ={'nombre': 'Miguel', 'apellido':'Manente', 'edad': 64, 'profesión':'Profesor', 'estudio': 'Analista de Sistemas' } #Creación de un diccionario
    dic.append(d0)

#Agregamos un 2do diccionario a la lista dic
for dic2 in range(1):
    d1={'nombre': 'Belkis', 'apellido':'Sioli', 'edad': 60, 'profesión':'Cocinera', 'estudio': 'Primarios'} #Creación de otro diccionario
    dic.append(d1)

#Agregamos un 3er diccionario a la lista dic
for dic3 in range(1):
    d2={'nombre': 'Romina', 'apellido':'Manente', 'edad': 37, 'profesión':'Médica', 'estudio': 'Universitario'} #Creación de otro diccionario
    dic.append(d2)

#Mostramos los tres diccionarios agregados con append [:3] estos corchetes indican la cantidad de objetos a mostrar en este caso 3
for d in dic[:3]:
    print(d)

#En pantalla se mostrará:
#{'nombre': 'Miguel', 'apellido': 'Manente', 'edad': 64, 'profesión': 'Profesor', 'estudio': 'Analista de Sistemas'}
#{'nombre': 'Belkis', 'apellido': 'Sioli', 'edad': 60, 'profesión': 'Cocinera', 'estudio': 'Primarios'}    
#{'nombre': 'Romina', 'apellido': 'Manente', 'edad': 37, 'profesión': 'Médica', 'estudio': 'Universitario'}

print(f"Total de diccionarios agregados son: {len(dic)}")

#En pantalla se mostrará:
#Total de diccionarios agregados son: 3
'''

#convertir un diccionario en JSON 

#Convertir un diccionario a una cadena JSON (serialización)

import json     #Importar el módulo JSON

#d0 ={'nombre': 'Miguel', 'apellido':'Manente', 'edad': 64, 'profesion':'Profesor', 'estudio': 'Analista de Sistemas' } #Creación de un diccionario

'''
cadenaJson = json.dumps(d0)    #Convertirmos  un diccionarios a través dumps en una cadena JSON

print(cadenaJson)    #mostramos el resultado de la conversión: 
                    # En pantalla se vería: {"nombre": "Miguel", "apellido": "Manente", "edad": 64, "profesi\u00f3n": "Profesor", "estudio": "Analista de Sistemas"}

#Convertir una cadena JSON a un diccionario (deserialización)

d0 = json.loads(cadenaJson)

print(d0)
'''
#Si deseamos guardar la cadena JSON en un archivo, hacemos lo siguiente:
'''
with open("datos.json", "w") as archivoJSON:
    json.dump(d0, archivoJSON)
'''

#Leer JSON desde un archivo

with open("datos.json", "r") as cadenaJSON:
    d0 = json.load(cadenaJSON)

print(d0)