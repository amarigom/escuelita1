import sqlite3
def crear_tabla():
    conn= sqlite3.connect('database1.db')
    c= conn.cursor()
    c.execute('''  CREATE TABLE IF NOT EXISTS docentes (
        id INTEGER PRIMARY KEY,
        nombre TEXT,
        puntaje TEXT) 
    ''')
    conn.commit()
    conn.close()
def guardar_docente(nombre, puntaje):
    conn= sqlite3.connect('database1.db')
    c= conn.cursor()
    c.execute ('INSERT INTO docentes (nombre,puntaje) VALUES (?,?)',(nombre,puntaje))
    conn.commit()
    conn.close()

def ver_docentes():
    conn = sqlite3.connect('database1.db')
    c = conn.cursor()
    c.execute('SELECT * FROM docentes')
    filas = c.fetchall()
    conn.close()
    
    for fila in filas:
        print(f"ID: {fila[0]}, Nombre: {fila[1]}, Puntaje: {fila[2]}")