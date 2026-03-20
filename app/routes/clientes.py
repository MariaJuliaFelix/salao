from fastapi import APIRouter

router = APIRouter(prefix="/clientes", tags=["Clientes"])

@router.get("/")
def listar_clientes():
    return {"msg": "listar clientes"}
