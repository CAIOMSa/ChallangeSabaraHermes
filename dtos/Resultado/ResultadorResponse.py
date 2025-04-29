from pydantic import BaseModel # type: ignore
from typing import Optional, List
from datetime import datetime
from dtos.Diagnostico.Diagnostico import Diagnostico
from dtos.Resultado.Resultado import Resultado
from dtos.CDI.CDI import CDI

class AtendimentoPacienteResponseML(BaseModel):
    id: int
    id_pessoa: Optional[int] = 0
    id_cdi: Optional[CDI]
    data_start: datetime
    data_end: Optional[datetime]
    id_convenio: Optional[int] = 0
    id_resultado: Optional[Resultado]
    id_diagnostico: Optional[Diagnostico]
