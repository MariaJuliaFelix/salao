from fastapi import APIRouter
from app.models.clientes import Cliente

router = APIRouter()

clientes = []

@router.post("/")
def criar_cliente(cliente: Cliente):
    clientes.append(cliente)
    return cliente

@router.get("/")
def listar_clientes():
    return clientes