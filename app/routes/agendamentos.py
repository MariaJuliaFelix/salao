from fastapi import APIRouter

router = APIRouter()

agendamentos = []

@router.post("/agendamentos")
def criar_agendamento(agendamento: dict):
    agendamentos.append(agendamento)
    return agendamento