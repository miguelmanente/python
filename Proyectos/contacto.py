from Conexion import ConexionDB

class Contacto:

    def __init__(self):
        self.db = ConexionDB()

    def crear(self, nombre, telefono):

        sql = "INSERT INTO personas (nombre, telefono) VALUES (%s, %s)"
        valores = (nombre, telefono)

        self.db.ejecutar(sql, valores)
        self.db.guardar()

    def leer(self):

        sql = "SELECT * FROM personas"
        cursor = self.db.ejecutar(sql)
        return cursor.fetchall()
    
    # def leer_por_id(self, id):
    #     sql = f"SELECT * FROM personas WHERE id = %s"
    #     cursor = self.db.ejecutar(sql, (id,))
    #     return cursor.fetchone()


    def actualizar(self, id, nombre, telefono):

        sql = "UPDATE personas SET nombre=%s, telefono=%s WHERE id=%s"
        valores = (nombre, telefono, id)

        self.db.ejecutar(sql, valores)
        self.db.guardar()
    
    def eliminar(self, id):

        sql = "DELETE FROM personas WHERE id=%s"
        valores = (id,)

        self.db.ejecutar(sql, valores)
        self.db.guardar()