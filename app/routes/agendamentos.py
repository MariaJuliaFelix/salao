from fastapi import APIRouter

router = APIRouter(prefix="/agendamentos", tags=["Agendamentos"])

@router.get("/")
def listar_agendamentos():
    return {"msg": "listar agendamentos"}


