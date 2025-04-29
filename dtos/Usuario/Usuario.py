from pydantic import BaseModel # type: ignore
from typing import Optional, List
from datetime import datetime

class Usuario(BaseModel):
    id: int
    type: str
    active: bool
    data_criacao: datetime
    data_update: datetime

class Login(BaseModel):
    id: Optional[int]
    id_usuario: Optional[int]
    cpfcrm: str
    password: str

class LoginResponse(BaseModel):
        cpfcrm: str
        password: str


class TipoAcesso(BaseModel):
    id: int
    nome: str
    active: bool

class UsuarioTipoAcesso(BaseModel):
    id: int
    id_usuario: int
    id_tipo_acesso: int


class Acesso(BaseModel):
    id: int
    id_page: int
    id_tipo_acesso: int
    active: bool


class Page(BaseModel):
    id: int
    nome: str
    url: str
    active: bool