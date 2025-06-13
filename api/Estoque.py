from fastapi import APIRouter, HTTPException # type: ignore
from fastapi.responses import JSONResponse
from pydantic import BaseModel # type: ignore
from typing import Dict, List,Any
import services.EstoqueService as service
from dtos.Produto.Produto import Produto,LoteEntrada
from dtos.Produto.ProdutoView import Lote
from utils.Validacoes import  adaptar_para_modelo
products_route = APIRouter()
@products_route.get("/", response_model=List[Produto])
def todos_produtos():
    """Retorna todos os produtos."""
    try:
        produtos = service.buscar_todos()
        return produtos
    except Exception as e:
       registrar_erro(str(e))
        print(f"Erro: {e}")
        return f"Erro: {str(e)}"

@products_route.get("/produto-nome={nome}", response_model=Produto)
def busca_produto_nome(nome: str):
    """Retorna todos os produtos."""
    try:
        produto = service.buscar_por_nome(nome)
        return produto
    except Exception as e:
       registrar_erro(str(e))
        print(f"Erro: {e}")
        return f"Erro: {str(e)}"


@products_route.post("/")
def registrar_novo_produto(produto: Produto):
    """registra um novo produto."""
    try:
        service.registrar(produto)
        return {"mensagem": f"produto {produto.nome} registrado."}
    except Exception as e:
       registrar_erro(str(e))
        print(f"Erro: {e}")
        return f"Erro: {str(e)}"

@products_route.post("/lote")
def registrar_novo_lote(lote: LoteEntrada):
    """registra um novo lote de entrada."""
    try:
        service.registrar_lote(lote)
        return {"mensagem": f"lote registrado."}
    except Exception as e:
       registrar_erro(str(e))
        print(f"Erro: {e}")
        return f"Erro: {str(e)}"

@products_route.get("/lote", response_model=List[Lote])
async def buscar_historico_de_lote():
    print("teste")
    try:
        lotes = service.buscar_todos_lotes()
        t = []
        for lote in lotes:
            t.append(adaptar_para_modelo(Lote,lote))
        return lotes
    except Exception as e:
       registrar_erro(str(e))
            print(f"Erro ao adaptar lote {lote}: {str(e)}")

