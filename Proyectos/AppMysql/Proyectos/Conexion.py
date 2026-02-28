import mysql.connector
import tkinter as tk
from tkinter import messagebox 

class ConexionDB:

    def __init__(self):

        self.conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Mibero606487",
            database="agenda"
        )

        # 🔴 ESTO TE FALTABA
        self.cursor = self.conexion.cursor()

    def ejecutar(self, sql, valores=None):

        self.cursor.execute(sql, valores or ())

    def guardar(self):

        self.conexion.commit()

    def cerrar(self):
        if self.cursor:
            self.cursor.close()
        if self.conexion:
            self.conexion.close()
            messagebox.showinfo("Conexión a la base de datos", "Conexión cerrada correctamente")

