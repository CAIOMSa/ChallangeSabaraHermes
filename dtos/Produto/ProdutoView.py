from pydantic import BaseModel,field_validator # type: ignore
from typing import Optional, List
from datetime import datetime
from dtos.Produto.Produto import Produto

class Lote(BaseModel):
    id: Optional[int] = None
    produto: Optional[Produto] = None
    quantidade: Optional[int] = None
    distribuidor:Optional[str] = None
    data_recebimento: Optional[datetime] = None
    data_validade: Optional[datetime] = None
    @field_validator("data_recebimento", "data_validade", mode="before")
    @classmethod
    def formatar_data(cls, value):
        if isinstance(value, str):
            return datetime.strptime(value, "%Y-%m-%d")
        return value.date() if isinstance(value, datetime) else value