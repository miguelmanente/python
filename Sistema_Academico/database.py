import sqlite3
import hashlib
import os

# Ruta dinámica de la base de datos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "profesores.db")

#función que permite conectarse a la Base de datos
def conectar():
    """
    Establece la conexión con la base de datos SQLite
    y habilita las claves foráneas.
    """
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

# Encriptar contraseña de usuarios
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Registrar usuario que luego permite loguearse
def registrar_usuario(username, password):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO usuarios (username, password) VALUES (?, ?)",
            (username, hash_password(password))
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False  # Usuario ya existe

# Validar login para loguearse
def validar_usuario(username, password):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM usuarios WHERE username = ? AND password = ?",
        (username, hash_password(password))
    )
    usuario = cursor.fetchone()
    conn.close()
    return usuario

#---------------------  CREAR Y VERIFICAR SI ESTÁN CREADAS LAS TABLAS ----------------
def crear_tablas():
    """
    Crea todas las tablas necesarias para el sistema académico
    si aún no existen.
    """
    conn = conectar()
    cursor = conn.cursor()

    cursor.executescript("""
    -- Tabla Profesores
    CREATE TABLE IF NOT EXISTS profesores (
        id_profesor INTEGER PRIMARY KEY AUTOINCREMENT,
        apenom TEXT NOT NULL,
        telefono TEXT NOT NULL,
        email TEXT NOT NULL,
        sitrev TEXT NOT NULL,
        fechatp TEXT NOT NULL
    );

    -- Tabla Materias
    CREATE TABLE IF NOT EXISTS materias (
        id_materia INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        descripcion TEXT
    );

    -- Tabla Cursos
    CREATE TABLE IF NOT EXISTS cursos (
        id_curso INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        nivel TEXT
    );

    -- Relación Profesor - Materia (N:N)
    CREATE TABLE IF NOT EXISTS profesor_materia (
        id_profesor INTEGER NOT NULL,
        id_materia INTEGER NOT NULL,
        PRIMARY KEY (id_profesor, id_materia),
        FOREIGN KEY (id_profesor) REFERENCES profesores(id_profesor) ON DELETE CASCADE,
        FOREIGN KEY (id_materia) REFERENCES materias(id_materia) ON DELETE CASCADE
    );

    -- Relación Materia - Curso (N:N)
    CREATE TABLE IF NOT EXISTS materia_curso (
        id_materia INTEGER NOT NULL,
        id_curso INTEGER NOT NULL,
        PRIMARY KEY (id_materia, id_curso),
        FOREIGN KEY (id_materia) REFERENCES materias(id_materia) ON DELETE CASCADE,
        FOREIGN KEY (id_curso) REFERENCES cursos(id_curso) ON DELETE CASCADE
    );

    -- (Opcional) Tabla de usuarios para login
    CREATE TABLE IF NOT EXISTS usuarios (
        id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    );
    """)

    conn.commit()
    conn.close()