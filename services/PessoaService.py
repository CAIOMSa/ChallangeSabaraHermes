from dtos.Pessoa.Pessoa import Pessoa, Convenio
from dtos.Pessoa.PessoaView import PessoaView
from database.connection import Database
from utils.Logs import registrar_erro
def buscar_todos():
    """Busca todas as pessoas com seus detalhes."""
    db = Database()
    try:
        query = "SELECT * FROM Pessoa"
        pessoas = db.fetch_all(query)
        for pessoa in pessoas:
            pessoa["contatos"] = buscar_contatos(db, pessoa["id"])
            pessoa["endereco"] = buscar_endereco(db, pessoa["id"])
            pessoa["convenio"] = buscar_convenios(db, pessoa["id"])
            pessoa["pessoas"] = buscar_pessoas_emergencia(db, pessoa["id"])
        return pessoas
    finally:
        db.close()

def buscar_por_cpf(cpf: str):
    """Busca uma pessoa pelo CPF."""
    db = Database()
    try:
        query = "SELECT * FROM Pessoa WHERE CPF = ?"
        pessoa = db.fetch_one(query, (cpf,))
        if pessoa:
            pessoa["contatos"] = buscar_contatos(db, pessoa["id"])
            pessoa["endereco"] = buscar_endereco(db, pessoa["id"])
            pessoa["convenio"] = buscar_convenios(db, pessoa["id"])
            pessoa["pessoas"] = buscar_pessoas_emergencia(db, pessoa["id"])
            return PessoaView(**pessoa)
        return None
    finally:
        db.close()

def registrar(pessoa: Pessoa):
    """Registra uma nova pessoa."""
    db = Database()
    try:
        query = """
            INSERT INTO Pessoa (DataNascimento, NomeCompleto, CPF, RG)
            VALUES (?, ?, ?, ?)
        """
        id_pessoa = db.executeAndReturnId(query, (pessoa.data_nascimento, pessoa.nome_completo, pessoa.cpf, pessoa.rg))
        if id_pessoa:
            if pessoa.contatos:
                registrar_contatos(db, id_pessoa, pessoa.contatos)
            if pessoa.endereco:
                registrar_endereco(db, id_pessoa, pessoa.endereco)
            if pessoa.convenio:
                registrar_convenios(db, id_pessoa, pessoa.convenio)
            return id_pessoa
    finally:
      db.close()

def buscar_contatos(db, id_pessoa):
    query = "SELECT * FROM Contato WHERE IdPessoa = ?"
    return db.fetch_all(query, (id_pessoa,))

def buscar_endereco(db, id_pessoa):
    query = "SELECT * FROM Endereco WHERE IdPessoa = ?"
    return db.fetch_one(query, (id_pessoa,))

def buscar_convenios(db, id_pessoa):
    query = """
        SELECT c.Id, c.Nome FROM PessoaConvenio pc
        JOIN Convenio c ON pc.IdConvenio = c.Id
        WHERE pc.IdPessoa = ?
    """
    return db.fetch_all(query, (id_pessoa,))

def buscar_pessoas_emergencia(db, id_pessoa):
    query = "SELECT * FROM PessoaEmergencia WHERE IdPessoa = ?"
    return db.fetch_all(query, (id_pessoa,))

def registrar_contatos(db, id_pessoa, contatos):
    for contato in contatos:
        print(contato)
        query = "INSERT INTO Contato (IdPessoa, Tipo, Detalhe) VALUES (?, ?, ?)"
        db.execute(query, (id_pessoa, contato.tipo, contato.detalhe))

def registrar_endereco(db, id_pessoa, endereco):
    if endereco:
        print(endereco)
        query = "INSERT INTO Endereco (IdPessoa, Cep, Rua, Complemento) VALUES (?, ?, ?, ?)"
        db.execute(query, (id_pessoa, endereco.cep, endereco.rua, endereco.complemento))

def registrar_convenios(db, id_pessoa, convenios):
    for id_convenio in convenios:
        query = "INSERT INTO PessoaConvenio (IdPessoa, IdConvenio) VALUES (?, ?)"
        db.execute(query, (id_pessoa, id_convenio))

def registrar_convenio(convenio: Convenio):
    """Registra um novo convênio."""
    db = Database()
    try:
        query = "INSERT INTO Convenio (Nome) VALUES (?)"
        db.execute(query, (convenio.nome,))
    finally:
        db.close()

def buscar_todos_convenios():
    """Retorna todos os convênios."""
    db = Database()
    try:
        query = "SELECT * FROM Convenio"
        return db.fetch_all(query)
    finally:
        db.close()

def registrar_relacao(pessoa_emergencia):
    db = None
    try:
        db = Database()
        query = "INSERT INTO PessoaEmergencia (IdPessoa, IdPessoaEmergencia, TipoDeRelacao,Active) VALUES (?, ?, ?,1)"
        values = (pessoa_emergencia.id_pessoa, pessoa_emergencia.id_pessoa_emergencia, pessoa_emergencia.tipo_de_relacao)
        db.execute(query, values)

        return "sucesso"
    except Exception as e:
        registrar_erro(str(e))
        print(f"Erro ao registrar produto: {e}")
        return f"Erro: {str(e)}"
    finally:
        if db:
            db.close()