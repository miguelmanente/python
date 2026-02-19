from Conexion import ConexionDB

class Contacto:

    def __init__(self):
        self.db = ConexionDB()

    def crear(self, nombre, telefono):

        sql = "INSERT INTO personas (nombre, telefono) VALUES (%s, %s)"
        valores = (nombre, telefono)

        self.db.ejecutar(sql, valores)
        self.db.guardar()

