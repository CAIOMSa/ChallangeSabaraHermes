from pydantic import BaseModel,field_validator # type: ignore
from typing import Optional, List
from datetime import datetime
from dtos.Pessoa.Pessoa import Contato,Endereco,Convenio,PessoaEmergencia

class PessoaView(BaseModel):
    id: int
    data_nascimento: Optional[datetime] = None
    nome_completo: Optional[str] = None
    cpf: Optional[str] = None
    rg: Optional[str] = None
    pessoas: Optional[List[PessoaEmergencia]] = None
    contatos: Optional[List[Contato]] = None
    endereco: Optional[Endereco] = None
    convenio: Optional[List[Convenio]] = None

    @field_validator("data_nascimento", mode="before")
    @classmethod
    def formatar_data(cls, value):
        if isinstance(value, str):
            return datetime.strptime(value, "%Y-%m-%d")
        return value.date() if isinstance(value, datetime) else value

#Unico json para envio e retorno