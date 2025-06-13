from fastapi import APIRouter, HTTPException # type: ignore
from pydantic import BaseModel # type: ignore
from typing import List
import services.PessoaService as service
from dtos.Pessoa.Pessoa import Pessoa,Convenio,PessoaEmergencia
from dtos.Pessoa.PessoaView import PessoaView
from utils.Logs import registrar_erro


pessoas_route = APIRouter()

@pessoas_route.get("/", response_model=List[PessoaView])
def todos_pessoas():
    """Retorna todas as pessoas."""
    try:
        pessoas = service.buscar_todos()
        return pessoas
    except Exception as e:
        registrar_erro(str(e))
        print(f"Erro: {e}")
        return f"Erro: {str(e)}"

@pessoas_route.get("/CPF={cpf}", response_model=PessoaView)
def busca_pessoa_cpf(cpf: str):
    """Retorna a pessoa com o cpf."""
    try:
        pessoa = service.buscar_por_cpf(cpf)
        return pessoa
    except Exception as e:
        registrar_erro(str(e))
        print(f"Erro: {e}")
        return f"Erro: {str(e)}"


@pessoas_route.post("/")
def registrar_nova_pessoa(pessoa: Pessoa):
    """registra uma nova pessoa."""
    try:
        id = service.registrar(pessoa)
        return {"id": id}
    except Exception as e:
        registrar_erro(str(e))
        print(f"Erro: {e}")
        return f"Erro: {str(e)}"

@pessoas_route.post("/convenio")
def registrar_novo_convenio(convenio: Convenio):
    """registra um novo convenio de entrada."""
    try:
        service.registrar_convenio(convenio)
        return {"mensagem": f"convenio registrado."}
    except Exception as e:
        registrar_erro(str(e))
        print(f"Erro: {e}")
        return f"Erro: {str(e)}"
@pessoas_route.get("/convenio",response_model=List[Convenio])
def buscar_todos_convenios():
    """verifica todos os convenios."""
    try:
        print("teste")
        convenios_do_banco = service.buscar_todos_convenios()
        convenios: List[Convenio] = [Convenio(**conv) for conv in convenios_do_banco]
        print(convenios)
        return convenios
    except Exception as e:
        registrar_erro(str(e))
        print(f"Erro: {e}")
        return f"Erro: {str(e)}"

@pessoas_route.post("/pessoa-emergencial")
def registrar_nova_pessoa(pessoa_emergencia: PessoaEmergencia):
    """registra uma nova pessoa."""
    try:
        service.registrar_relacao(pessoa_emergencia)
        return {"mensagem": f"relação registrada."}
    except Exception as e:
        registrar_erro(str(e))
        print(f"Erro: {e}")
        return f"Erro: {str(e)}"
