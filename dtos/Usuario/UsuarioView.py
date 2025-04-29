from pydantic import BaseModel # type: ignore
from typing import Optional, List
from datetime import datetime
from dtos.Usuario.Usuario import TipoAcesso,Page
class UsuarioView(BaseModel):
    id: int
    nome: str
    senha: str
    active: bool
    acessos: List[TipoAcesso] = []
    data_criacao: datetime
    data_update: datetime
class TipoAcessoView(BaseModel):
    id: int
    nome: str
    active: bool
    pages: List[Page] = []
