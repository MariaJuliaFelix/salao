from pydantic import BaseModel

class Cliente(BaseModel):
    id: int
    nome: str
    telefone: str