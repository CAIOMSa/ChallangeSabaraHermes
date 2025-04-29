from pydantic import BaseModel # type: ignore
from typing import Optional, List
from datetime import datetime
from dtos.AtendimentoPaciente.AtendimentoPaciente import AtendimentoPaciente

class FilaAtendimentoResponse(BaseModel):
    id: int
    atendimento: AtendimentoPaciente
    urgencia: int
    etapas_concluidas: Optional[str]
    etapa_atual: str