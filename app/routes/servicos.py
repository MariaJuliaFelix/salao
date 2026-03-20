from fastapi import APIRouter

router = APIRouter(prefix="/servicos", tags=["Serviços"])

@router.get("/")
def listar_servicos():
    return {"msg": "listar serviços"}