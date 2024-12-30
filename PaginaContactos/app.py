# Flask: frameware que ayuda a la creación de aplicaciones web con python
# Render_template: Función que renderiza las paginas html que están en la carpeta templates
# Request: utilizado para enlazar lo que hay en un formulario con una conexión de BD através del metodo POST o GET
# Redirect y url_for: Crea un bucle para volver a la misma página don de se ejecutó
# flash: Permite poner mensaje cuanto se insertaron registro en una una BD, por ej. pag. 36.

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

#instancia de la clase Flask, creación de la aplicación
app = Flask(__name__)

# Configuración de la conexión a MYSQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Mibero606487'
app.config['MYSQL_DB'] = 'flaskcontact'
mysql = MySQL(app)

# Configuraciones
app.secret_key ='mysecretkey'

#Definir las rutas a cada una de las página que tendrá el proyecto
@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()

    return render_template('index.html', contacts = data)

@app.route('/add_contact', methods = ['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contacts (fullname, phone, email) VALUES (%s, %s, %s)', (fullname, phone, email))
        mysql.connection.commit()
        flash('CONTACTO AGREGADO SATISFACTORIAMENTE!!!')
        return redirect(url_for('Index'))
    
@app.route('/edit/<id>')
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = %s', (id))
    data = cur.fetchall()
    return render_template('edit-contact.html', contact = data[0])

@app.route('/update/<id>', methods = ['POST'])
def update_contact(id):
    if request. method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE contacts
            SET fullname = %s,
                phone = %s,
                email = %s 
            WHERE id = %s   
        """,(fullname, phone, email, id))
        mysql.connection.commit()
    flash('CONTACTO ACTUALIZADO CORRECTAMENTE')
    return redirect(url_for('Index'))

@app.route('/delete/<string:id>')
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('CONTACTO REMOVIDO SATISFACTORIAMENTE')
    return redirect(url_for('Index'))

#Ejecución de APP en la raiz o pagina principal
if __name__ == '__main__':
    app.run(port=3000, debug=True)



