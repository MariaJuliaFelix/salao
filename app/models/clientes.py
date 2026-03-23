from pydantic import BaseModel, Field


class ClienteCreate(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100)


class ClienteResponse(BaseModel):
    id: int
    nome: str