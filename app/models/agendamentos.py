from pydantic import BaseModel

class Agendamento(BaseModel):
    id: int
    cliente_id: int
    servicos: list[int]
    horario: str