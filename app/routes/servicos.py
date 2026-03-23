from fastapi import APIRouter

router = APIRouter()

# simulando banco
servicos = [
    {"id": 1, "nome": "Corte", "descricao": "Corte feminino", "preco": 50, "duracao": 30},
    {"id": 2, "nome": "Escova", "descricao": "Escova modeladora", "preco": 40, "duracao": 25},
    {"id": 3, "nome": "Manicure", "descricao": "Unhas completas", "preco": 30, "duracao": 20},
]

@router.get("/servicos")
def listar_servicos():
    return servicos