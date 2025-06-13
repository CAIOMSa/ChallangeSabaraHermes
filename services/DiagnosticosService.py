import json
import os
from services import FilaAtendimentoService as fs
from services import EstoqueService as es
from database.connection import Database
from utils.Logs import registrar_erro

PASTA_IMAGENS = "banco_de_imagens"
if not os.path.exists(PASTA_IMAGENS):
    os.makedirs(PASTA_IMAGENS)


def registrar(diagnostico,id_atendimento):
    db = None
    try:
        db = Database()

        query = """INSERT INTO Diagnostico (
            ObservacoesMedicas,
            RelatorioPessoal,
            Pressao,
            SaturacaoSangue,
            Peso,
            ExamesRealizados,
            HistoricoMedFamiliar,
            CondicoesMedPreexistentes,
            MedicacoesEmUso,
            Restricoes,
            Temperatura) VALUES (?, ?, ?,?, ?, ?, ?, ?, ?, ?, ?)"""
        values = (diagnostico.observacoes_medicas,
                  diagnostico.relatorio_pessoal,
                  diagnostico.pressao,
                  diagnostico.saturacao_sangue,
                  diagnostico.peso,
                  diagnostico.exames_realizados,
                  diagnostico.historico_med_familiar,
                  diagnostico.condicoes_med_preexistentes,
                  diagnostico.medicacoes_em_uso,
                  diagnostico.restricoes,
                  diagnostico.temperatura)
        id_diagnostico = db.executeAndReturnId(query, values)
        fs.novoId_atendimento_paciente("IdDiagnostico",id_atendimento,id_diagnostico)
        return "sucesso"
    except Exception as e:
        registrar_erro(str(e))
        print(f"Erro ao registrar diagnostico: {e}")
        return f"Erro: {str(e)}"
    finally:
        if db:
            db.close()

def salvar_imagem(imagem, nome_arquivo):
    """
    Salva a imagem na pasta banco_de_imagens.
    """
    caminho_arquivo = os.path.join(PASTA_IMAGENS, nome_arquivo)
    with open(caminho_arquivo, "wb") as buffer:
        buffer.write(imagem.file.read())
    return caminho_arquivo

def salvar_cdi(imagem, nome_arquivo):
    """
    Salva a imagem no banco de imagens.
    """
    caminho_imagem = salvar_imagem(imagem, nome_arquivo)
    return caminho_imagem


def registrar_cdi(id_atendimento,cdi):
    """
    Registra as conclusões do cdi no banco de dados.
    """
    db = None
    try:
        db = Database()
        print("Conectado ao banco")

        query = "INSERT INTO CDI (UrlImage) VALUES (?)"
        cdi_id = db.executeAndReturnId(query, (cdi.url_image,))
        for conclusion in cdi.id_Image_conclusions:
            query = "INSERT INTO CDImageConclusions (IdCDI,IdImageConclusion) VALUES (?,?)"
            values = (cdi_id,conclusion)
            id_relations = db.executeAndReturnId(query, values)
        fs.novoId_atendimento_paciente("IdCDI",id_atendimento,cdi_id)
        return cdi_id
    except Exception as e:
        registrar_erro(str(e))
        print(f"Erro ao registrar as conclusoes: {e}")
        return f"Erro: {str(e)}"
    finally:
        if db:
            db.close()
            print("Conexão fechada")


def registrar_detalheOp(id,detalhe_op):
    db = None
    try:
        db = Database()
        query = "INSERT INTO DetalhesOp (nome) VALUES (?)"
        detalhe_op_id = db.executeAndReturnId(query, (detalhe_op.nome,))
        for custo in detalhe_op.custos_op:
            query = "INSERT INTO CustosOp (IdDetalheOp,IdProduto,QuantGasta) VALUES (?,?,?)"
            values = (detalhe_op_id,custo.id_produto,custo.quant_gasta)
            db.execute(query,values)
            gasto = custo.quant_gasta * -1
            es.atualizar_quantidade_produto(custo.id_produto,gasto)
        query = "INSERT INTO AtendimentoDetalhesOp (IdAtendimento,IdDetalhesOp) VALUES (?,?)"
        values = (id,detalhe_op_id)
        db.execute(query,values)

        return "sucesso"
    except Exception as e:
        registrar_erro(str(e))
        print(f"Erro ao registrar detalhe op: {e}")
        return f"Erro: {str(e)}"
    finally:
        if db:
            db.close()


def registrar_resultado(id_atendimento,resultado):
    db = None
    try:
        db = Database()
        query = "INSERT INTO Resultado (Doenca,ObsMedica,Medicacao) VALUES (?,?,?)"
        result_id = db.executeAndReturnId(query, (resultado.doenca,resultado.obs_medica,resultado.medicacao))
        fs.novoId_atendimento_paciente("IdResultado",id_atendimento,result_id)
        return "sucesso"
    except Exception as e:
        registrar_erro(str(e))
        print(f"Erro ao registrar resultado: {e}")
        return f"Erro: {str(e)}"
    finally:
        if db:
            db.close()

def registrar_trein_ml_agent(grande_base):
    for base in grande_base:
        resultado = base.id_resultado
        diagnostico = base.id_diagnostico
        fluxo_registro_trein_ML(resultado,diagnostico)
    return "sucesso"


def fluxo_registro_trein_ML(resultado,diagnostico):
    db = None
    try:
        db = Database()
        query = "INSERT INTO Resultado (Doenca,ObsMedica,Medicacao) VALUES (?,?,?)"
        result_id = db.executeAndReturnId(query, (resultado.doenca,resultado.obs_medica,resultado.medicacao))
    except Exception as e:
        registrar_erro(str(e))
        print(f"Erro ao registrar resultado: {e}")
        return f"Erro: {str(e)}"
    finally:
        if db:
            db.close()
    try:
        db = Database()

        query = """INSERT INTO Diagnostico (
            ObservacoesMedicas,
            RelatorioPessoal,
            Pressao,
            SaturacaoSangue,
            Peso,
            ExamesRealizados,
            HistoricoMedFamiliar,
            CondicoesMedPreexistentes,
            MedicacoesEmUso,
            Restricoes,
            Temperatura) VALUES (?, ?, ?,?, ?, ?, ?, ?, ?, ?, ?)"""
        values = (diagnostico.observacoes_medicas,
                  diagnostico.relatorio_pessoal,
                  diagnostico.pressao,
                  diagnostico.saturacao_sangue,
                  diagnostico.peso,
                  diagnostico.exames_realizados,
                  diagnostico.historico_med_familiar,
                  diagnostico.condicoes_med_preexistentes,
                  diagnostico.medicacoes_em_uso,
                  diagnostico.restricoes,
                  diagnostico.temperatura)
        id_diagnostico = db.executeAndReturnId(query, values)
    except Exception as e:
        registrar_erro(str(e))
        print(f"Erro ao registrar diagnostico: {e}")
        return f"Erro: {str(e)}"
    finally:
        if db:
            db.close()
    try:
        db = Database()
        query = """
        INSERT INTO AtendimentoPaciente
        (IdPaciente, IdCDI, DataStart, IdConvenio, IdResultado, IdDiagnostico)
        VALUES (?, ?, GETDATE(), ?, ?, ?)
        """
        values = (
            0,
            0,
            0,
            result_id,
            id_diagnostico
        )
        atendimento_id = db.executeAndReturnId(query, values)
        return atendimento_id
    except Exception as e:
        registrar_erro(str(e))
        print(f"Erro ao registrar atendimento do paciente: {e}")
        return None
    finally:
        if db:
            db.close()

def coleta_base_ML():
        db = None
        try:
            db = Database()

            query = """
            SELECT * FROM AtendimentoPaciente ap
            LEFT JOIN Diagnostico dg ON ap.IdDiagnostico = dg.Id
            LEFT JOIN CDI cdi ON ap.IdCDI = cdi.Id
            LEFT JOIN CDImageConclusions cdic ON cdi.Id = cdic.IdImageConclusion
            LEFT JOIN Resultado r ON ap.IdResultado = r.Id
            WHERE r.Id IS NOT NULL
            """
            retorno = db.fetch_all(query)
            return retorno
        except Exception as e:
            registrar_erro(str(e))
            print(f"Erro ao buscar os a base: {e}")
            return f"Erro: {str(e)}"
        finally:
            if db:
                db.close()
def analise_modelo_d(diagnostico):
    from models.DiagnosticosModel import prever_doenca
    entrada = {
        "relatoriopessoal": diagnostico.relatorio_pessoal,
        "observacoesmedicas": diagnostico.observacoes_medicas,
        "obsmedica": diagnostico.observacoes_medicas,
        "pressao": diagnostico.pressao,
        "saturacaosangue": diagnostico.saturacao_sangue,
        "peso": diagnostico.peso,
        "temperatura": diagnostico.temperatura,
        "historicomedfamiliar": diagnostico.historico_med_familiar,
        "condicoesmedpreexistentes": diagnostico.condicoes_med_preexistentes,
        "medicacoesemuso": diagnostico.medicacoes_em_uso,
        "restricoes": diagnostico.restricoes,
        "examesrealizados": diagnostico.exames_realizados
    }
    res = prever_doenca(entrada)
    print(res)
    return res