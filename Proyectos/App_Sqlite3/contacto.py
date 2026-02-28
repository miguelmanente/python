
from Conexion import ConexionDB

class Contacto:

    def __init__(self):
        self.db = ConexionDB()

    def crear(self, nombre, telefono):
        sql = "INSERT INTO personas (nombre, telefono) VALUES (?, ?)"
        self.db.cursor.execute(sql, (nombre, telefono))
        self.db.conexion.commit()

    def leer(self):
        sql = "SELECT * FROM personas ORDER BY nombre ASC"
        self.db.cursor.execute(sql)
        return self.db.cursor.fetchall()

    def buscar_por_apellido(self, texto):
        sql = """
            SELECT * FROM personas
            WHERE nombre LIKE ?
            ORDER BY nombre ASC
        """
        self.db.cursor.execute(sql, ("%" + texto + "%",))
        return self.db.cursor.fetchall()

    def actualizar(self, id, nombre, telefono):
        sql = """
            UPDATE personas
            SET nombre = ?, telefono = ?
            WHERE id = ?
        """
        self.db.cursor.execute(sql, (nombre, telefono, id))
        self.db.conexion.commit()

    def eliminar(self, id):
        sql = "DELETE FROM personas WHERE id = ?"
        self.db.cursor.execute(sql, (id,))
        self.db.conexion.commit()

    def cerrar_conexion(self):
        self.db.cerrar()