from pydantic import BaseModel

class Servico(BaseModel):
    id: int
    nome: str
    descricao: str
    preco: float
    duracao: int