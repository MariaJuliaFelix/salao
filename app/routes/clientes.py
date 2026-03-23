from fastapi import APIRouter
from app.database import conectar

router = APIRouter()


@router.post("/")
def criar_cliente(cliente: dict):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO clientes (nome) VALUES (?)", (cliente["nome"],))
    conn.commit()

    cliente_id = cursor.lastrowid
    conn.close()

    return {"id": cliente_id, "nome": cliente["nome"]}


@router.get("/")
def listar_clientes():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT id, nome FROM clientes ORDER BY nome")
    clientes = [dict(row) for row in cursor.fetchall()]

    conn.close()
    return clientes