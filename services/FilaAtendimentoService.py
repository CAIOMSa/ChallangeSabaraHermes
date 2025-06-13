from database.connection import Database
from utils.Logs import registrar_erro

def buscar_fila_por_cpf(cpf):
    """Busca a fila de atendimento pelo CPF"""
    db = None
    try:
        db = Database()
        query = """
        SELECT f.*, a.*
        FROM FilaAtendimento f
        JOIN AtendimentoPaciente a ON f.IdAtendimento = a.id
        JOIN Pessoa p ON a.IdPaciente = p.Id
        WHERE p.CPF = ?
        """
        retorno = db.fetch_one(query, (cpf,))
        return retorno
    except Exception as e:
        registrar_erro(str(e))
        print(f"Erro ao buscar fila por CPF {cpf}: {e}")
        return None
    finally:
        if db:
            db.close()

def buscar_fila_por_atendimento(id_atendimento):
    """Busca a fila de atendimento pelo ID do atendimento"""
    db = None
    try:
        db = Database()
        query = "SELECT * FROM FilaAtendimento WHERE IdAtendimento = ?"
        retorno = db.fetch_one(query, (id_atendimento,))
        return retorno
    except Exception as e:
        registrar_erro(str(e))
        print(f"Erro ao buscar fila por atendimento {id_atendimento}: {e}")
        return None
    finally:
        if db:
            db.close()

def registrar_atendimento_paciente(atendimento):
    """Registra o atendimento do paciente e retorna o ID gerado"""
    db = None
    try:
        db = Database()
        query = """
        INSERT INTO AtendimentoPaciente
        (IdPaciente, IdCDI, DataStart, IdConvenio, IdResultado, IdDiagnostico)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        values = (
            atendimento.id_pessoa,
            atendimento.id_cdi,
            atendimento.data_start,
            atendimento.id_convenio,
            atendimento.id_resultado,
            atendimento.id_diagnostico
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
def novoId_atendimento_paciente(campo,id_atendimento,id):
    """registra novo campo para o atendimento"""
    db = None
    try:
        db = Database()
        query = f"UPDATE AtendimentoPaciente SET {campo} = ? WHERE Id = ?"
        values = (id_atendimento,id)
        atendimento_id = db.executeAndReturnId(query, values)
        return atendimento_id
    except Exception as e:
        registrar_erro(str(e))
        print(f"Erro ao registrar atendimento do paciente: {e}")
        return None
    finally:
        if db:
            db.close()
def registrar_fila(fila):
    """Registra um atendimento na fila"""
    db = None
    try:
        print("fila:", fila)
        id_atendimento = registrar_atendimento_paciente(fila.atendimento)
        db = Database()
        query = "INSERT INTO FilaAtendimento (IdAtendimento, Urgencia, EtapaAtual, EtapaConcluida) VALUES (?, ?, ?, ?)"
        print(fila)
        values = (id_atendimento, fila.urgencia, fila.etapa_atual, fila.etapas_concluidas)
        db.execute(query, values)
        return "Atendimento registrado na fila"
    except Exception as e:
        registrar_erro(str(e))
        print(f"Erro ao registrar atendimento na fila: {e}")
        return str(e)
    finally:
        if db:
            db.close()

def atualizar_etapa_fila(id, etapa_atual):
    """Atualiza a etapa atual da fila e adiciona a etapa anterior às etapas concluídas"""
    db = None
    try:
        db = Database()

        query_select = "SELECT EtapaConcluida, EtapaAtual FROM FilaAtendimento WHERE Id = ?"
        fila = db.fetch_one(query_select, (id,))
        print(fila)
        if not fila:
            return "Atendimento não encontrado na fila"

        etapas_concluidas = fila["etapaconcluida"] or ""
        etapa_atual_anterior = fila["etapaatual"]

        etapas_concluidas += f",{etapa_atual_anterior}" if etapas_concluidas else etapa_atual_anterior
        query_update = "UPDATE FilaAtendimento SET EtapaConcluida = ?, EtapaAtual = ?,UltimoResultado = GETDATE(),EstaEmAtendimento = 0  WHERE Id = ?"
        print(query_update)
        print((etapas_concluidas, etapa_atual, id))
        db.execute(query_update, (etapas_concluidas, etapa_atual, id))

        return "Etapa da fila atualizada"
    except Exception as e:
        registrar_erro(str(e))
        print(f"Erro ao atualizar etapa da fila: {e}")
        return str(e)
    finally:
        if db:
            db.close()

def atualizar_status_fila(id):
    """cosnta que está sendo atendido"""
    db = None
    try:
        db = Database()

        query_update = "UPDATE FilaAtendimento SET UltimoResultado = GETDATE(),EstaEmAtendimento = 1  WHERE Id = ?"
        db.execute(query_update, ( id,))

        return "status da fila atualizada"
    except Exception as e:
        registrar_erro(str(e))
        print(f"Erro ao atualizar etapa da fila: {e}")
        return str(e)
    finally:
        if db:
            db.close()

def buscar_na_fila(etapaatual):
    """Busca com ordem com base na etapa atual"""
    db = None
    try:
        db = Database()
        query = """
            SELECT
                Id,
                IdAtendimento,
                Urgencia,
                UltimoResultado,
                DATEDIFF(SECOND, '00:00:00', UltimoResultado) *
                CASE
                    WHEN Urgencia = 1 THEN 1
                    WHEN Urgencia = 2 THEN 1.2
                    WHEN Urgencia = 3 THEN 1.3
                    WHEN Urgencia = 4 THEN 1.4
                    WHEN Urgencia = 5 THEN 1.5
                    WHEN Urgencia = 6 THEN 1.6
                    WHEN Urgencia = 7 THEN 1.7
                    WHEN Urgencia = 8 THEN 1.8
                    WHEN Urgencia = 9 THEN 1.9
                    WHEN Urgencia = 10 THEN 2
                    ELSE 1
                END AS TempoEmSegundosCalculado
            FROM FilaAtendimento
            WHERE EtapaAtual = ? AND EstaEmAtendimento = 0;
        """
        retorno = db.fetch_one(query, (etapaatual,))
        return retorno
    except Exception as e:
        print(f"Erro ao buscar fila por etapaatual {etapaatual}: {e}")
        return None
    finally:
        if db:
            db.close()