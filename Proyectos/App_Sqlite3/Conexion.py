import tkinter as tk
from tkinter import messagebox 
import sqlite3

class ConexionDB:

    def __init__(self):
        self.conexion = sqlite3.connect("agenda.db")
        self.cursor = self.conexion.cursor()
        self.crear_tabla()

    def crear_tabla(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS personas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                telefono TEXT NOT NULL
            )
        """)
        self.conexion.commit()

    def cerrar(self):
        self.conexion.close()
        messagebox.showinfo("Conexión a la base de datos", "Conexión cerrada correctamente")
        
    # def cerrar(self):
    #     if self.cursor:
    #         self.cursor.close()
    #     if self.conexion:
    #         self.conexion.close()
    #         messagebox.showinfo("Conexión a la base de datos", "Conexión cerrada correctamente")

