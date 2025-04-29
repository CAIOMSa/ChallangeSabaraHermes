from pydantic import BaseModel,field_validator # type: ignore
from typing import Optional, List
from datetime import datetime


class Endereco(BaseModel):
    id: int
#    id_pessoa: int
    cep: str
    rua: str
    complemento: Optional[str]

class Contato(BaseModel):
    id: int
#    id_pessoa: int
    tipo: str
    detalhe: str

class Convenio(BaseModel):
    id: int
    nome: str

class PessoaEmergencia(BaseModel):
    id: int
    id_pessoa: int
    id_pessoa_emergencia: int
    tipo_de_relacao: str
    active: bool



class Pessoa(BaseModel):
    id: int
    data_nascimento: datetime
    nome_completo: str
    cpf: str
    rg: str
    contatos: List[Contato]
    endereco: Endereco
    convenio: Optional[List[int]]

    @field_validator("data_nascimento", mode="before")
    @classmethod
    def formatar_data(cls, value):
        if isinstance(value, str):
            return datetime.strptime(value, "%Y-%m-%d")
        return value.date() if isinstance(value, datetime) else value
