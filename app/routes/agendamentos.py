from fastapi import APIRouter, HTTPException
from app.models.agendamentos import Agendamento

router = APIRouter()

agendamentos = []

@router.get("/disponibilidade")
def verificar_disponibilidade(data: str, horario: str):
    for agendamento in agendamentos:
        if agendamento.data == data and agendamento.horario == horario:
            return {"disponivel": False}

    return {"disponivel": True}


@router.post("/")
def criar_agendamento(agendamento: Agendamento):
    for item in agendamentos:
        if item.data == agendamento.data and item.horario == agendamento.horario:
            raise HTTPException(status_code=400, detail="Esse horário já está ocupado")

    agendamentos.append(agendamento)
    return agendamento


@router.get("/")
def listar_agendamentos():
    return agendamentos