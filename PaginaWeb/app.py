#Propósito de app = Flask(__name__)

#Inicializar la aplicación: Esta línea crea una instancia de la clase Flask. Esta instancia representará tu aplicación web.

#Configuración del módulo: El parámetro __name__ le dice a Flask dónde encontrar los archivos y recursos que necesita. 
# __name__ es una variable especial en Python que se establece al nombre del módulo. Si estás ejecutando el script directamente,
# __name__ se establecerá en "__main__", lo que le indica a Flask que las rutas y configuraciones están en el mismo archivo.

#¿Por qué __name__ es importante?

#Flask necesita saber la ubicación del módulo para encontrar las rutas, plantillas HTML, archivos estáticos y configuraciones.
# Utilizando __name__, Flask puede establecer correctamente el contexto de la aplicación y funcionar correctamente independientemente del nombre del archivo.
# app = Flask(__name__). ¡Es un componente esencial para cualquier aplicación Flask! 

#Propósito de @app.route('/')

# Definir la Ruta Principal: La ruta '/' representa la página principal o la raíz de tu sitio web.
# Cuando un usuario accede a la URL base de tu aplicación (por ejemplo, http://127.0.0.1:5000/), 
# Flask ejecuta la función asociada a esta ruta.
# Asociación de Funciones a URL: Este decorador @app.route('/') asocia una función de Python a una URL específica.
# Cuando un usuario visita esa URL, la función se ejecuta y su resultado se envía al navegador.

#Rutas Adicionales
#Puedes crear más rutas para otras partes de tu sitio web:
#Por ejemplo:

#@app.route('/about')
#def about():
#    return "Esta es la página About"

#@app.route('/contact')
#def contact():
#    return "Esta es la página Contact"

#Cada vez que definas una nueva ruta, puedes asociarla con una función que maneje la lógica y el contenido que deseas mostrar.

#Rutas con Parámetros
#También puedes definir rutas con parámetros para manejar URLs dinámicas:

#@app.route('/usuario/<nombre>')
#def saludar_usuario(nombre):
#    return f"¡Hola, {nombre}!"

#@app.route('/post/<int:id>')
#def mostrar_post(id):
#    return f"Mostrando el post número {id}"
# En resumen, el decorador @app.route('/') es esencial para manejar la navegación en tu aplicación Flask.
# Define qué función se ejecuta cuando un usuario accede a una URL específica.

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')

def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return "Esta es la página About"

@app.route('/contact')
def contact():
    return "Esta es la página Contact"

if __name__ == '__main__':
    app.run(debug=True)


#Propósito de if __name__ == '__main__':
# Evitar la ejecución involuntaria: En Python, cada archivo puede actuar como un módulo que puede ser importado. 
# La variable especial __name__ se establece en "__main__" únicamente cuando el archivo se ejecuta directamente. 
# Si el archivo se importa en otro script, __name__ se establece en el nombre del archivo en lugar de "__main__".

# Punto de entrada de la aplicación: Esto permite definir un punto de entrada para la ejecución de la aplicación.
# El bloque de código dentro de if __name__ == '__main__': solo se ejecutará cuando el script se ejecute directamente,
# lo cual es útil para realizar pruebas y ejecutar el servidor.

#app.run(debug=True)
# Iniciar el servidor de desarrollo: app.run() inicia el servidor de desarrollo de Flask, lo que permite que la aplicación web
# escuche peticiones en un puerto específico (por defecto, el puerto 5000).

# Modo debug: El argumento debug=True activa el modo depuración, lo cual es extremadamente útil durante el desarrollo. En este modo:

# La aplicación se reinicia automáticamente cada vez que se hacen cambios en el código.

# Se muestra un "traceback" interactivo en el navegador si se produce un error, lo que facilita la resolución de problemas.

# En resumen, esta estructura es una práctica común y recomendada en la programación de Python para asegurar que el código dentro 
# del bloque if __name__ == '__main__': se ejecute solo cuando el archivo se ejecute directamente. Esto es especialmente útil cuando
# se desarrollan aplicaciones con Flask.


