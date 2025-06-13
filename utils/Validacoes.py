from datetime import datetime
from typing import Type, TypeVar, Optional, get_origin, get_args, Union
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)

def is_optional_type(tp):
    return get_origin(tp) is Union and type(None) in get_args(tp)

def get_inner_type(tp):
    return [arg for arg in get_args(tp) if arg is not type(None)][0] if is_optional_type(tp) else tp

def gerar_valor_padrao(tipo):
    tipo = get_inner_type(tipo)

    if tipo == str:
        return "desconhecido"
    elif tipo in [int, float]:
        return 0
    elif tipo == datetime:
        return datetime(1999, 1, 1)
    elif isinstance(tipo, type) and issubclass(tipo, BaseModel):
        return adaptar_para_modelo(tipo, {})  # gera submodelo com valores padrão
    return None

def adaptar_para_modelo(model: Type[T], dados: dict) -> T:
    campos = model.model_fields
    dados_formatados = {}

    for campo, definicao in campos.items():
        tipo = definicao.annotation
        valor = dados.get(campo, None)

        if valor is None:
            valor = gerar_valor_padrao(tipo)

        elif isinstance(valor, dict):
            inner_type = get_inner_type(tipo)
            if isinstance(inner_type, type) and issubclass(inner_type, BaseModel):
                valor = adaptar_para_modelo(inner_type, valor)

        elif isinstance(valor, str) and get_inner_type(tipo) == datetime:
            try:
                valor = datetime.strptime(valor, "%Y-%m-%d")
            except ValueError:
                valor = datetime(1999, 1, 1)

        dados_formatados[campo] = valor

    return model(**dados_formatados)
