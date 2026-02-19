# # definición de una clase
# class Perro:
#     pass

# # Crear un objeto de la clase perro
# mi_perro = Perro()


# class Perro:
#     # El método __init__ es el constructor de la clase, se ejecuta cada vez que se crea un objeto de la clase
#     def __init__(self, nombre, raza):
#         print(f"Creando perro {nombre}, {raza}")

#         # Atributos de INSTANCIA, se definen dentro del método __init__ y se acceden a través de self
#         self.nombre = nombre
#         self.raza = raza


# # Creamos un objeto de la clase perro
# mi_perro = Perro("Manchita", "MuyLinda")
# print(type(mi_perro))
# print(mi_perro.nombre)
# print(mi_perro.raza)


#Atributo de Clase
# class Perro:
#     # Atributo de clase, se define fuera del método __init__ y se accede a través de la clase o del objeto
#     especie = "mamifero"

#     def __init__(self, nombre, raza):
#         print(f"Creando perro {nombre}, {raza}")

#         # Atributos de INSTANCIA
#         self.nombre = nombre
#         self.raza = raza

# print(Perro.especie)

#Definiendo métodos en la clase
class Perro:

    #Atibuto de clase
    especie = "mamifero"

    def __init__(self, nombre, raza):
        print(f"Creando perro {nombre}, {raza}")

        #Atributo de instancia
        self.nombre = nombre
        self.raza = raza

    # Método de instancia, se define dentro de la clase y se accede a través del objeto
    def ladrar(self):
        print("Guau guau")

    def camina1(self, pasos):
        print(f"{self.nombre} está caminando y ha dado {pasos} pasos")

# Creamos un objeto de la clase perro
mi_perro = Perro("Manchita", "MuyLinda")
mi_perro.ladrar()
mi_perro.camina1(5)

