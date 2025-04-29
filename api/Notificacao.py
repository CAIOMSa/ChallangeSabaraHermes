from fastapi import APIRouter, HTTPException # type: ignore
from pydantic import BaseModel # type: ignore
from typing import List

notificacao_route = APIRouter()

@notificacao_route.get("/notif")
def Login():
    """Retorna dados do usuário."""
    try:
        reponse = {"message" : "testando"}
        return reponse
    except Exception as e:
        print(f"Erro: {e}")
        return f"Erro: {str(e)}"