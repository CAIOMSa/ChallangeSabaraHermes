import datetime
import inspect

def registrar_erro(mensagem, arquivo_log="erros_log.txt"):
    frame = inspect.currentframe().f_back
    nome_funcao = frame.f_code.co_name
    agora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    linha_log = f"[{agora}] [{nome_funcao}] {mensagem}\n"

    with open(arquivo_log, "a", encoding="utf-8") as f:
        f.write(linha_log)
