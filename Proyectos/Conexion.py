import mysql.connector

class ConexionDB:

    def __init__(self):
        self.conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Mibero606487",
            database="agenda"
        )

    def ejecutar(self, sql, valores=None):
        cursor = self.conexion.cursor()

        if valores:
            cursor.execute(sql, valores)
        else:
            cursor.execute(sql)

        return cursor

    def guardar(self):
        self.conexion.commit()

    def cerrar(self):
        self.conexion.close()

