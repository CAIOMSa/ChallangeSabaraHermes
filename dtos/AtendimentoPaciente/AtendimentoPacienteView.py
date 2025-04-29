from pydantic import BaseModel # type: ignore
from typing import Optional, List
from datetime import datetime
from dtos.Pessoa.PessoaView import PessoaView
from dtos.Pessoa.Pessoa import Convenio
from dtos.CDI.CDI import CDI
from dtos.Diagnostico.DiagnosticoView import DiagnosticoView
from dtos.Resultado.Resultado import Resultado

class AtendimentoPacienteView(BaseModel):
    id: int
    id_pessoa: PessoaView
    id_cdi: Optional[CDI]
    data_start: datetime
    data_end: Optional[datetime]
    id_convenio: Optional[Convenio]
    id_resultado: Optional[Resultado]
    id_diagnostico: Optional[DiagnosticoView]
