import sqlite3
import hashlib

DB_PATH = "usuarios.db"  # ou o caminho que preferir

def inicializar_banco():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                senha_hash TEXT NOT NULL
            )
        ''')
        conn.commit()

def registrar_usuario(username, senha):
    senha_hash = hashlib.sha256(senha.encode()).hexdigest()
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO usuarios (username, senha_hash) VALUES (?, ?)", 
                           (username, senha_hash))
            conn.commit()
        return True, "Usuário registrado com sucesso."
    except sqlite3.IntegrityError:
        return False, "Nome de usuário já está em uso."

def verificar_login(username, senha):
    senha_hash = hashlib.sha256(senha.encode()).hexdigest()
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE username = ? AND senha_hash = ?", 
                       (username, senha_hash))
        usuario = cursor.fetchone()
        if usuario:
            return True, "Login bem-sucedido."
        else:
            return False, "Nome de usuário ou senha incorretos."
