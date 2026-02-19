import mysql.connector

conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Mibero606487",
    database="agenda"
)

cursor = conexion.cursor()

sql = "INSERT INTO personas (nombre, telefono) VALUES (%s, %s)"
valores = ("Miguel", 3364661103)

cursor.execute(sql, valores)

conexion.commit()

print("Dato guardado!")

conexion.close()
