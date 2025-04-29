from pydantic import BaseModel # type: ignore
from typing import Optional, List
from datetime import datetime

class AtendimentoPaciente(BaseModel):
    id: int
    id_pessoa: int
    id_cdi: Optional[int]
    data_start: datetime
    data_end: Optional[datetime]
    id_convenio: Optional[int] = None
    id_resultado: Optional[int] = None
    id_diagnostico: Optional[int] = None
