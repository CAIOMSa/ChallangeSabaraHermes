from pydantic import BaseModel # type: ignore
from typing import Optional, List
from datetime import datetime

class FilaAtendimento(BaseModel):
    id: int
    id_atendimento: int
    urgencia: int
    etapas_concluidas: Optional[str]
    etapa_atual: str