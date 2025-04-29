from fastapi import APIRouter
from api.Administrativo import adm_route
from api.Auth import auth_route
from api.Diagnosticos import diagnostico_route
from api.Estoque import products_route
from api.FilaAtendimento import atendimento_route
from api.Pessoa import pessoas_route
from api.Notificacao import notificacao_route

api_router = APIRouter()
api_router.include_router(auth_route, prefix="/auth", tags=["Auth"])

api_router.include_router(adm_route, prefix="/administrativa", tags=["Administrativa"])
api_router.include_router(atendimento_route, prefix="/atendimento", tags=["Atendimento"])
api_router.include_router(diagnostico_route, prefix="/diagnostico", tags=["Diagnostico"])
api_router.include_router(products_route, prefix="/produtos", tags=["Produtos"])
api_router.include_router(pessoas_route, prefix="/pessoas", tags=["Pessoa"])
api_router.include_router(notificacao_route, prefix="/notificacao", tags=["Notificações"])