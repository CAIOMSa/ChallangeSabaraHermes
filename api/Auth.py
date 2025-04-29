from fastapi import APIRouter, HTTPException # type: ignore
from pydantic import BaseModel # type: ignore
from typing import List
import services.AdministrativoService as service
from dtos.Usuario.Usuario import Usuario,TipoAcesso,Page,LoginResponse
from dtos.Usuario.UsuarioView import UsuarioView,TipoAcessoView

auth_route = APIRouter()

@auth_route.post("/login")
def Login(login:LoginResponse):
    """Retorna dados do usuário."""
    try:
        reponse = service.login(login)
        return reponse
    except Exception as e:
        print(f"Erro: {e}")
        return f"Erro: {str(e)}"