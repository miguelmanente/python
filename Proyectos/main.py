from contacto import Contacto

contacto = Contacto()

while True:

    print("\n--- AGENDA ---")
    print("1 - Agregar contacto")
    print("2 - Ver contactos")
    print("3 - Actualizar contacto")
    print("4 - Eliminar contacto")
    print("5 - Salir")

    opcion = input("Seleccione una opción: ")

    # AGREGAR
    if opcion == "1":

        nombre = input("Nombre: ")
        telefono = int(input("Telefono: "))

        contacto.crear(nombre, telefono)
        print("Contacto agregado!")

    # VER
    elif opcion == "2":

        datos = contacto.leer()

        print("\nLISTA DE CONTACTOS:\n")

        for fila in datos:
            print(f"ID: {fila[0]} | Nombre: {fila[1]} | Tel: {fila[2]}")

    # ACTUALIZAR
    elif opcion == "3":

        id = int(input("ID del contacto a modificar: "))
        nombre = input("Nuevo nombre: ")
        telefono = int(input("Nuevo telefono: "))

        contacto.actualizar(id, nombre, telefono)
        print("Contacto actualizado!")

    # ELIMINAR
    elif opcion == "4":

        datos = contacto.leer()

        print("\nCONTACTOS ACTUALES:\n")

        for fila in datos:
            print(f"ID: {fila[0]} | Nombre: {fila[1]} | Tel: {fila[2]}")

        print("\n--- ELIMINAR CONTACTO ---")

        id = int(input("Ingrese ID del contacto a eliminar: "))

        confirmar = input("¿Seguro que desea eliminar? (s/n): ")

        if confirmar.lower() == "s":
            contacto.eliminar(id)
            print("Contacto eliminado!")
        else:
            print("Operación cancelada.")

    # SALIR
    elif opcion == "5":
        contacto.db.cerrar()
        print("Adios Miguel!")
        break

    else:
        print("Opción inválida")
