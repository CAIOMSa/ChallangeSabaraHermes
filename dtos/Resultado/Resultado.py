from pydantic import BaseModel # type: ignore
from typing import Optional, List
from datetime import datetime

class CustosOp(BaseModel):
    id: int
    id_produto: Optional[int] = 0
    quant_gasta: int

class DetalhesOp(BaseModel):
    id: int
    nome: str
    custos_op: List[CustosOp]



class Resultado(BaseModel):
    id: int
    doenca: Optional[str] = None
    obs_medica: Optional[str] = None
    medicacao: Optional[str] = None