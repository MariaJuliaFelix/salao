from fastapi import APIRouter, HTTPException
from app.models.agendamentos import Agendamento
from app.database import conectar

router = APIRouter()

@router.post("/")
def criar_agendamento(agendamento: Agendamento):
    conn = conectar()
    cursor = conn.cursor()

    # 🔥 VERIFICAR HORÁRIO
    cursor.execute("SELECT * FROM agendamentos WHERE horario = ?", (agendamento.horario,))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Horário já ocupado")

    cursor.execute("""
        INSERT INTO agendamentos (id, cliente_nome, servicos, total, duracao, horario)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        agendamento.id,
        agendamento.cliente_nome,
        str(agendamento.servicos),
        agendamento.total,
        agendamento.duracao,
        agendamento.horario
    ))

    conn.commit()
    conn.close()

    return agendamento


@router.get("/")
def listar_agendamentos():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM agendamentos")
    dados = cursor.fetchall()

    conn.close()

    resultado = []

    for d in dados:
        resultado.append({
            "id": d[0],
            "cliente_nome": d[1],
            "servicos": d[2],
            "total": d[3],
            "duracao": d[4],
            "horario": d[5]
        })

    return resultado