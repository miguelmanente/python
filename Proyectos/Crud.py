class CRUD:

    def __init__(self, db, tabla):
        self.db = db
        self.tabla = tabla

    def crear(self, datos):
        columnas = ', '.join(datos.keys())
        valores = ', '.join(['%s'] * len(datos))

        sql = f"INSERT INTO {self.tabla} ({columnas}) VALUES ({valores})"

        self.db.ejecutar(sql, tuple(datos.values()))
        self.db.commit()

    def leer_todos(self):
        sql = f"SELECT * FROM {self.tabla}"
        cursor = self.db.ejecutar(sql)
        return cursor.fetchall()

    def leer_por_id(self, id):
        sql = f"SELECT * FROM {self.tabla} WHERE id = %s"
        cursor = self.db.ejecutar(sql, (id,))
        return cursor.fetchone()

    def actualizar(self, id, datos):
        set_clause = ', '.join([f"{col}=%s" for col in datos.keys()])
        sql = f"UPDATE {self.tabla} SET {set_clause} WHERE id = %s"

        valores = list(datos.values())
        valores.append(id)

        self.db.ejecutar(sql, tuple(valores))
        self.db.commit()

    def eliminar(self, id):
        sql = f"DELETE FROM {self.tabla} WHERE id = %s"
        self.db.ejecutar(sql, (id,))
        self.db.commit()
