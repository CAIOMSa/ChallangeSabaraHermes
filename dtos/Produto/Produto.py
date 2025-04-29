from pydantic import BaseModel,field_validator # type: ignore
from typing import Optional, List
from datetime import datetime


class Produto(BaseModel):
    id: int
    nome: str
    descricao: str
    fabricante: str
    quantidade: int

class LoteEntrada(BaseModel):
    id: int
    id_produto: int
    quantidade: int
    distribuidor: str
    data_recebimento: datetime
    data_validade: datetime
    @field_validator("data_recebimento", "data_validade", mode="before")
    @classmethod
    def formatar_data(cls, value):
        if isinstance(value, str):
            return datetime.strptime(value, "%Y-%m-%d")
        return value.date() if isinstance(value, datetime) else value