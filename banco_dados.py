import sqlite3

def criar_banco():
    conn = sqlite3.connect("financeiro.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            valor REAL,
            tipo TEXT,
            categoria TEXT,
            descricao TEXT,
            datahora TEXT
        )
    """)
    
    conn.commit()
    conn.close()