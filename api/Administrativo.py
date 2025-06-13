from fastapi import APIRouter, HTTPException # type: ignore
from pydantic import BaseModel # type: ignore
from typing import List
import services.AdministrativoService as service
from dtos.Usuario.Usuario import Usuario,TipoAcesso,Page
from dtos.Usuario.UsuarioView import UsuarioView,TipoAcessoView
from utils.Logs import registrar_erro

adm_route = APIRouter()

@adm_route.get("/", response_model=List[UsuarioView])
def todos_usuarios():
    """Retorna todos os usuarios."""
    try:
        usuarios = service.buscar_todos()
        return usuarios
    except Exception as e:
        registrar_erro(str(e))
        print(f"Erro: {e}")
        return f"Erro: {str(e)}"

@adm_route.post("/")
def registrar_novo_usuario(usuario: Usuario):
    """registra uma novo usuario."""
    try:
        service.registrar(usuario)
        return {"mensagem": f"pessoa: {usuario.nome} registrada."}
    except Exception as e:
        registrar_erro(str(e))
        print(f"Erro: {e}")
        return f"Erro: {str(e)}"


@adm_route.get("/acesso", response_model=List[TipoAcessoView])
def todos_cargos_acesso():
    """Retorna todos os tipos de acessos."""
    try:
        tipo_acesso = service.buscar_todos_tipo_acesso()
        return tipo_acesso
    except Exception as e:
        registrar_erro(str(e))
        print(f"Erro: {e}")
        return f"Erro: {str(e)}"

@adm_route.post("/acesso")
def registrar_novo_acesso(tipo_acesso: TipoAcesso):
    """registra uma novo usuario."""
    try:
        service.registrar_acesso(tipo_acesso)
        return {"mensagem": f"acesso: {tipo_acesso.nome} registrado."}
    except Exception as e:
        registrar_erro(str(e))
        print(f"Erro: {e}")
        return f"Erro: {str(e)}"


@adm_route.get("/page", response_model=List[Page])
def todas_paginas():
    """Retorna todoas as páginas."""
    try:
        pages = service.buscar_todos_pages()
        return pages
    except Exception as e:
        registrar_erro(str(e))
        print(f"Erro: {e}")
        return f"Erro: {str(e)}"

@adm_route.post("/pagina")
def registrar_nova_pagina(page: Page):
    """registra uma nova página ao sistema."""
    try:
        service.registrar_pagina(page)
        return {"mensagem": f"acesso: {page.nome} registrado."}
    except Exception as e:
        registrar_erro(str(e))
        print(f"Erro: {e}")
        return f"Erro: {str(e)}"

@adm_route.post("/usuario-acesso?id-usuario{id_usuario}&id-acesso{id_acesso}")
def registrar_usuario_acesso(id_usuario: int,id_acesso:int):
    """registra uma nova correlação."""
    try:
        service.registrar_usuario_acesso(id_usuario,id_acesso)
        return {"mensagem": f"acesso designado."}
    except Exception as e:
        registrar_erro(str(e))
        print(f"Erro: {e}")
        return f"Erro: {str(e)}"

@adm_route.post("/acesso-pagina?id-pagina{id_pagina}&id-acesso{id_acesso}")
def registrar_pagina_acesso(id_pagina: int,id_acesso:int):
    """registra uma nova correlação."""
    try:
        service.registrar_pagina_acesso(id_pagina,id_acesso)
        return {"mensagem": f"pagina adicionada ao conjunto de acesso."}
    except Exception as e:
        registrar_erro(str(e))
        print(f"Erro: {e}")
        return f"Erro: {str(e)}"