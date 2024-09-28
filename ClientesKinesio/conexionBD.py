import mysql.connector

class ConexionBD():

    def __init__(self):
        self.conexion = mysql.connector.connect(host = 'localhost',
                                                database = 'clientes_kinesio',
                                                port = '3306',
                                                user = 'root',
                                                password = 'Mibero606487')
    

    def inserta_cliente(self, dia, fecha, hora, nombres, asistencia):
        cursor = self.conexion.cursor()
        sql = '''INSERT INTO cli_kinesio (DIA, FECHA, HORA, NOMBRES, ASISTENCIA) VALUES('{}','{}','{}','{}','{}')'''.format(dia, fecha, hora, nombres, asistencia)
        cursor.execute(sql)
        self.conexion.commit()
        cursor.close()
    