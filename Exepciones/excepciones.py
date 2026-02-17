# LOS COMENTARIOS QUE SE PUEDEN USAR SON:
# PARA UNA SOLA LÍNEA
"""PARA VARIAS LÍNEAS"""
# y CTRL + SHIFT + / PARA COMENTAR VARIAS LÍNEAS DE CÓDIGOS


a = 5
b = 0

# try:
#    c = a / b
# except ZeroDivisionError:
#    print("No se puede dividir por cero")

# poner más de una excepción en el mismo bloque try, para que se puedan manejar varias excepciones a la vez
"""
try:
    c = 5 / 0   # Esto generará una excepción de división por cero
    d = 2 + "Hola" # Esto generará una excepción de tipo, ya que no se pueden sumar un número y una cadena
except ZeroDivisionError:
    print("No se puede dividir por cero")
except TypeError:
   print("No se pueden sumar un número y una cadena")
"""

# Otra forma de indicar el error en poner las ecepciones en el mismo except
"""
try:
    c = 5 / 0   # Esto generará una excepción de división por cero
    d = 2 + "Hola" # Esto generará una excepción de tipo, ya que no se pueden sumar un número y una cadena
except (ZeroDivisionError, TypeError):
    print("Excepcion ZeroDivision/TypeError")
"""

# Si no sabemos los tipos de excepciones se escribe EXCEPCION en el except
# try:
#     c = 5 / 0   # Esto generará una excepción de división por cero
#     d = 2 + "Hola" # Esto generará una excepción de tipo, ya que no se pueden sumar un número y una cadena
# except Exception:
#     print("Se ha producido un ERROR por excepcion")


# No obstante hay una forma de saber que excepción ha sido la que ha ocurrido.
# try:
#     d = 2 + "Hola" # Esto generará una excepción de tipo, ya que no se pueden sumar un número y una cadena
# except Exception as ex:
#     print("Se ha producido un ERROR por excepcion")
#     print("El error es: ", type(ex))

# USO DEL ELSE EN LAS EXCEPCIONES
# try:
#     x = 5 / 0
# except Exception as ex:
#     print("Se ha producido un ERROR por excepcion")
#     print("El error es: ", type(ex))
# else:
#     print("No se ha producido ningún error, el resultado es: ", x)


#Uso del FINALLY en las excepciones
# try:
#     x = 5 / 0
# except:
#     print("Entra en except, ha ocurrido una excepción")
# finally:
#     print("Entra en finally, se ejecuta siempre, haya o no haya excepción")

# Ejemplo de excepciones con manejos de archivos
try:
    with open('fichero.txt') as file:
        read_data = file.read()
# Capturamos una excepción concreta
except OSError:
    print('OSError. No se pudo abrir el archivo fichero.txt')
    