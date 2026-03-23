from fastapi import APIRouter
from app.database import conectar

router = APIRouter()


@router.get("/")
def listar_servicos():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nome, descricao, preco, duracao
        FROM servicos
        ORDER BY nome
    """)
    servicos = [dict(row) for row in cursor.fetchall()]

    conn.close()
    return servicos