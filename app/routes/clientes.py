from fastapi import APIRouter

router = APIRouter()

clientes = []

@router.post("/clientes")
def criar_cliente(cliente: dict):
    clientes.append(cliente)
    return cliente