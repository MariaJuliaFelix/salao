from pydantic import BaseModel


class ServicoResponse(BaseModel):
    id: int
    nome: str
    descricao: str
    preco: float
    duracao: int