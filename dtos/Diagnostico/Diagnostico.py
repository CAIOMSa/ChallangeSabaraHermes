from pydantic import BaseModel # type: ignore
from typing import Optional, List
from datetime import datetime

class Diagnostico(BaseModel):
    id: int
    observacoes_medicas: Optional[str] = None
    relatorio_pessoal: Optional[str] = None
    pressao: Optional[str] = None
    saturacao_sangue: Optional[str] = None
    peso: Optional[float] = None
    exames_realizados: Optional[str] = None
    historico_med_familiar: Optional[str] = None
    condicoes_med_preexistentes: Optional[str] = None
    medicacoes_em_uso: Optional[str] = None
    restricoes: Optional[str] = None
    temperatura: Optional[str] = None
