import sqlite3

DB_NAME = "salao.db"


def conectar():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS servicos (
        id INTEGER PRIMARY KEY,
        nome TEXT NOT NULL,
        descricao TEXT NOT NULL,
        preco REAL NOT NULL,
        duracao INTEGER NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS agendamentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER NOT NULL,
        data TEXT NOT NULL,
        horario TEXT NOT NULL,
        total REAL NOT NULL,
        duracao INTEGER NOT NULL,
        status TEXT NOT NULL DEFAULT 'pendente',
        observacao TEXT,
        FOREIGN KEY (cliente_id) REFERENCES clientes(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS agendamento_servicos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        agendamento_id INTEGER NOT NULL,
        servico_id INTEGER NOT NULL,
        status TEXT NOT NULL DEFAULT 'pendente',
        FOREIGN KEY (agendamento_id) REFERENCES agendamentos(id),
        FOREIGN KEY (servico_id) REFERENCES servicos(id)
    )
    """)

    conn.commit()
    popular_servicos_iniciais(conn)
    conn.close()


def popular_servicos_iniciais(conn):
    cursor = conn.cursor()

    servicos_padrao = [
        (1, "Corte Feminino", "Corte com finalização simples", 65.0, 50),
        (2, "Escova Lisa", "Escova modelada com acabamento liso", 45.0, 40),
        (3, "Escova Modelada", "Escova com movimento e modelagem", 55.0, 50),
        (4, "Hidratação Capilar", "Tratamento para nutrição e brilho dos fios", 70.0, 45),
        (5, "Reconstrução Capilar", "Tratamento intensivo para recuperação dos fios", 95.0, 60),
        (6, "Progressiva", "Alinhamento térmico para redução de volume", 180.0, 150),
        (7, "Coloração Completa", "Aplicação de coloração em todo o cabelo", 160.0, 120),
        (8, "Retoque de Raiz", "Retoque na raiz com coloração", 90.0, 70),
        (9, "Luzes", "Mechas para iluminação dos fios", 220.0, 180),
        (10, "Penteado", "Penteado para festas e eventos", 120.0, 70)
    ]

    for servico in servicos_padrao:
        cursor.execute("""
        INSERT OR IGNORE INTO servicos (id, nome, descricao, preco, duracao)
        VALUES (?, ?, ?, ?, ?)
        """, servico)

    conn.commit()