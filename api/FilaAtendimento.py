from fastapi import APIRouter, HTTPException
from dtos.AtendimentoPaciente.AtendimentoPaciente import AtendimentoPaciente
from dtos.FilaAtendimento.FilaAtendimento import FilaAtendimento
from dtos.FilaAtendimento.FilaAtendimentoResponse import FilaAtendimentoResponse
import services.FilaAtendimentoService as fila_service

atendimento_route = APIRouter()

@atendimento_route.get("/CPF={cpf}")
def buscar_fila_por_cpf(cpf: str):
    """Busca a fila de atendimento do paciente pelo CPF"""
    try:
        fila = fila_service.buscar_fila_por_cpf(cpf)
        if not fila:
            raise HTTPException(status_code=404, detail="Paciente não encontrado na fila")
        return fila
    except Exception as e:
       registrar_erro(str(e))
        print(f"Erro ao buscar fila por CPF: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@atendimento_route.get("/id-atendimento={id_atendimento}")
def buscar_fila_por_atendimento(id_atendimento: int):
    """Busca a fila de atendimento pelo ID do atendimento"""
    try:
        fila = fila_service.buscar_fila_por_atendimento(id_atendimento)
        if not fila:
            raise HTTPException(status_code=404, detail="Atendimento não encontrado na fila")
        return fila
    except Exception as e:
       registrar_erro(str(e))
        print(f"Erro ao buscar fila por ID do atendimento: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@atendimento_route.post("/")
def registrar_fila(fila: FilaAtendimentoResponse):
    """Registra um atendimento e o adiciona à fila"""
    try:
        fila_service.registrar_fila(fila)
        return {"message": "Atendimento registrado e adicionado à fila com sucesso"}
    except Exception as e:
       registrar_erro(str(e))
        print(f"Erro ao registrar atendimento na fila: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@atendimento_route.put("/id-fila={id}&etapa-atual={etapa_atual}")
def atualizar_etapa_fila(id: int, etapa_atual: str):
    """Atualiza a etapa atual da fila"""
    try:
        fila_service.atualizar_etapa_fila(id, etapa_atual)
        return {"message": "Etapa da fila atualizada com sucesso"}
    except Exception as e:
       registrar_erro(str(e))
        print(f"Erro ao atualizar etapa da fila: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@atendimento_route.put("/esta-em-atendimento?id-fila={id}")
def atualizar_status(id: int):
    """Atualiza a etapa atual da fila"""
    try:
        fila_service.atualizar_status_fila(id)
        return {"message": "Etapa da fila atualizada com sucesso"}
    except Exception as e:
       registrar_erro(str(e))
        print(f"Erro ao atualizar etapa da fila: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@atendimento_route.get("/busca-pacientes-ordem?etapa-atual={etapaatual}")
def atualizar_status(etapaatual: str):
    """busca ordem com base na etapa atual da fila"""
    try:
        fila_service.buscar_na_fila(etapaatual)
        return {"message": "Etapa da fila atualizada com sucesso"}
    except Exception as e:
       registrar_erro(str(e))
        print(f"Erro ao atualizar etapa da fila: {e}")
        raise HTTPException(status_code=500, detail=str(e))