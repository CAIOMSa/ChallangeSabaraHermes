from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import List
from dtos.CDI.CDI import CDI
from  dtos.Diagnostico.Diagnostico import Diagnostico
from  dtos.Diagnostico.DiagnosticoView import DiagnosticoView
from dtos.Resultado.Resultado import Resultado,DetalhesOp
from dtos.Resultado.ResultadorResponse import AtendimentoPacienteResponseML
import services.DiagnosticosService as service

diagnostico_route = APIRouter()

@diagnostico_route.get("/id-atendimento={id}", response_model=DiagnosticoView)
def diagnostico_paciente(id: int):
    """Retorna o diagnóstico por ID do atendimento."""
    try:
        diagnostico = service.buscar_por_Id(id)
        return diagnostico
    except Exception as e:
        print(f"Erro: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@diagnostico_route.post("/id-atendimento={id}")
def atualizar_diagnostico(id: int,diagnostico: Diagnostico):
    """Atualiza um diagnóstico existente ID do atendimento."""
    try:
        service.registrar(diagnostico,id)
        return {"mensagem": "Diagnóstico atualizado com sucesso!", "id_diagnostico": id}
    except Exception as e:
        print(f"Erro: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@diagnostico_route.put("/id-atendimento=={id}")
def atualizar_diagnostico(id: int,diagnostico: Diagnostico):
    """Atualiza um diagnóstico existente ID do atendimento."""
    try:
        service.atualizar(id,diagnostico)
        return {"mensagem": "Diagnóstico atualizado com sucesso!", "id_diagnostico": id}
    except Exception as e:
        print(f"Erro: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@diagnostico_route.post("/resultados?id-atendimento={id}")
def registrar_resultado(id: int,resultado: Resultado):
    """registra um resultado."""
    try:
        service.registrar_resultado(resultado,id)
        return {"mensagem": "Diagnóstico atualizado com sucesso!", "id_diagnostico": id}
    except Exception as e:
        print(f"Erro: {e}")
        raise HTTPException(status_code=500, detail=str(e))



@diagnostico_route.post("/cdi-registrar-imagem/")
async def registrar_cdi_img(imagem: UploadFile = File(...)):
    """
    Faz o upload da imagem e salva no banco de imagens, sem análise da IA.
    """
    try:
        caminho_imagem = service.salvar_cdi(imagem, imagem.filename)
        return {"mensagem": "Imagem registrada com sucesso!", "caminho": caminho_imagem, "nome": imagem.filename}
    except Exception as e:
        print(f"Erro: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@diagnostico_route.post("/cdi-registrar-conclusoes?id-atendimento={id}")
async def registrar_cdi(id:int,cdi:CDI):
    """
    Registra o cdi pelo atendimento
    """
    try:
        id_cdi = service.registrar_cdi(id,cdi)
        return {"mensagem": "Registrado com sucesso!", "id": id_cdi}
    except Exception as e:
        print(f"Erro: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@diagnostico_route.post("/cdi-analise")
async def analisar_cdi(imagem: UploadFile = File(...)):
    """
    Manda para a ia analisar.
    """
    try:
        print("a")
    except Exception as e:
        print(f"Erro: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@diagnostico_route.post("/realizacoes?id-atendimento={id}")
def registrar_detalheOp(id: int,detalhe_op: DetalhesOp):
    """
    registra detalhe de operacional
    """
    try:
        service.registrar_detalheOp(id, detalhe_op)
        return {"mensagem": "realização médica registrada com sucesso"}
    except Exception as e:
        print(f"Erro: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@diagnostico_route.post("/temporario-para-modelo-ml")
async def registrar_trein_ml_agent(grande_base: List[AtendimentoPacienteResponseML]):
    """
    modelo de esperado para treinamento de ml
    """
    try:
        service.registrar_trein_ml_agent(grande_base)
        return {"mensagem": "Registrado com sucesso!"}
    except Exception as e:
        print(f"Erro: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@diagnostico_route.post("/enviar-para-analise")
async def envia_para_analise(diagnostico: Diagnostico):
    """
    envia para analise
    """
    try:
        resultados = service.analise_modelo_d(diagnostico)
        return resultados
    except Exception as e:
        print(f"Erro: {e}")
        raise HTTPException(status_code=500, detail=str(e))