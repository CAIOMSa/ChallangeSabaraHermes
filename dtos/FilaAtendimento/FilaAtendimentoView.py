from pydantic import BaseModel # type: ignore
from typing import Optional, List
from datetime import datetime
from dtos.AtendimentoPaciente.AtendimentoPacienteView import AtendimentoPacienteView

class FilaAtendimentoView(BaseModel):
    id: int
    id_atendimento: AtendimentoPacienteView
    urgencia: int
    etapas_concluidas: Optional[str]
    etapa_atual: str
    esta_em_atendimento: bool
    ultimo_resultado: datetime