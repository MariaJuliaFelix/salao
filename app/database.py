import sqlite3

def conectar():
    return sqlite3.connect("salao.db")


def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS agendamentos (
        id INTEGER PRIMARY KEY,
        cliente_nome TEXT,
        servicos TEXT,
        total REAL,
        duracao INTEGER,
        horario TEXT
    )
    """)

    conn.commit()
    conn.close()