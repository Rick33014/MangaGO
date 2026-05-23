import sqlite3

def init_db():
    conn = sqlite3.connect('mangas.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS colecao (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            volume INTEGER NOT NULL,
            editora TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print("Banco de dados inicializado!")

if __name__ == "__main__":
    init_db()