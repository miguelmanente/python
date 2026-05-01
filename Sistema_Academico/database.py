import sqlite3
import hashlib
import os

# ---------------- Ruta dinámica de la base de datos profesores --------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "profesores.db")

#--------- función que permite conectarse a la BD profesores -----------------------
def conectar():
    """
    Establece la conexión con la base de datos SQLite
    y habilita las claves foráneas.
    """
    conn = sqlite3.connect(DATABASE)
    #conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn
# ----------------------------------------------------------------------------------

# -------------------- Encriptar contraseña de usuarios ----------------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()
#-----------------------------------------------------------------------------------

# ----------- Registrar usuario que luego permite loguearse ------------------------
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
# --------------------------- Fin función Registrar Usuario -------------------------


# ---------------------- Validar login del usuario para loguearse -------------------
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
# ---------------------------- Fin función validación---------------------------------------------------

#---------------------  CREAR Y VERIFICAR SI ESTÁN CREADAS LAS TABLAS ----------------
def crear_tablas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS profesores (
        id_profesor INTEGER PRIMARY KEY AUTOINCREMENT,
        apenom TEXT,
        telefono TEXT,
        email TEXT,
        sitrev TEXT,
        fechatp TEXT
    );

    CREATE TABLE IF NOT EXISTS materias (
        id_materia INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        descripcion TEXT
    );

    CREATE TABLE IF NOT EXISTS cursos (
        id_curso INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        turno TEXT
    );

    CREATE TABLE IF NOT EXISTS horarios (
        id_horario INTEGER PRIMARY KEY AUTOINCREMENT,
        id_curso INTEGER,
        id_materia INTEGER,
        dia TEXT,
        hentrada TEXT,
        hsalida TEXT,
        FOREIGN KEY (id_curso) REFERENCES cursos(id_curso),
        FOREIGN KEY (id_materia) REFERENCES materias(id_materia)
    );

    CREATE TABLE IF NOT EXISTS asignaciones_docentes (
        id_asignacion INTEGER PRIMARY KEY AUTOINCREMENT,
        id_profesor INTEGER,
        id_horario INTEGER,
        srprofesor TEXT,
        FOREIGN KEY (id_profesor) REFERENCES profesores(id_profesor),
        FOREIGN KEY (id_horario) REFERENCES horarios(id_horario)
    );
    """)

    conn.commit()
    conn.close()