from typing import List, Optional
from pydantic import BaseModel, Field


class AgendamentoCreate(BaseModel):
    cliente_nome: str = Field(..., min_length=2, max_length=100)
    servicos: List[int] = Field(..., min_length=1)
    data: str
    horario: str
    observacao: Optional[str] = None


class AgendamentoUpdate(BaseModel):
    cliente_nome: str = Field(..., min_length=2, max_length=100)
    servicos: List[int] = Field(..., min_length=1)
    data: str
    horario: str
    observacao: Optional[str] = None


class StatusAgendamentoUpdate(BaseModel):
    status: str


class StatusServicoUpdate(BaseModel):
    status: str