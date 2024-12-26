from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Mibero606487'
app.config['MYSQL_DB'] = 'flaskcontact'
mysql = MySQL(app)

@app.route('/')
def Index():
    return "Hola Mundo!!!!!!"

@app.route('/add_contact')
def add_contact():
    return "Agregar contactos"

@app.route('/edit_contact')
def edit_contact():
    return "Editar contactos"

@app.route('/delete')
def delete_contact():
    return "Borrar contactos"

if __name__ == '__main__':
    app.run(port=3000, debug=True)



