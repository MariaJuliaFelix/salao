from pydantic import BaseModel

class Agendamento(BaseModel):
    id: int
    cliente_nome: str
    servicos: list[int]
    total: float
    duracao: int
    horario: str