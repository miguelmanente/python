from Conexion import ConexionDB


class Contacto:

    def __init__(self):
        self.db = ConexionDB()

    def crear(self, nombre, telefono):

        sql = "INSERT INTO personas (nombre, telefono) VALUES (%s, %s)"
        valores = (nombre, telefono)

        self.db.ejecutar(sql, valores)
        self.db.guardar()

    # def leer(self):

    #     sql = "SELECT * FROM personas"
    #     cursor = self.db.ejecutar(sql)
    #     return self.db.cursor.fetchall()

    def leer(self):
        sql = "SELECT * FROM personas ORDER BY nombre ASC"
        self.db.cursor.execute(sql)
        return self.db.cursor.fetchall()
  
    # def leer_por_id(self, id):
    #     sql = f"SELECT * FROM personas WHERE id = %s"
    #     cursor = self.db.ejecutar(sql, (id,))
    #     return cursor.fetchone()

    def buscar_por_apellido(self, apellido):

        sql = "SELECT id, nombre, telefono FROM personas WHERE nombre LIKE %s"

        self.db.cursor.execute(sql, ("%" + apellido + "%",))

        return self.db.cursor.fetchall()

    def actualizar(self, id, nombre, telefono):

        sql = """
             UPDATE personas
             SET nombre = %s,
             telefono = %s
             WHERE id = %s
           """

        self.db.cursor.execute(sql, (nombre, telefono, id))
        self.db.conexion.commit()

    def eliminar(self, id):

       sql = "DELETE FROM personas WHERE id = %s"

       self.db.cursor.execute(sql, (id,))
       self.db.conexion.commit()


    def cerrar_conexion(self):
        self.db.cerrar()