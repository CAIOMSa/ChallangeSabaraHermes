from database.connection import Database
from dtos.Usuario.Usuario import Usuario, TipoAcesso, Page
from dtos.Usuario.UsuarioView import UsuarioView, TipoAcessoView

def buscar_todos():
    db = Database()
    try:
        query = "SELECT * FROM Usuario"
        usuarios = db.fetch_all(query)
        for usuario in usuarios:
            usuario['acessos'] = buscar_acessos_usuario(usuario['id'])
        return [UsuarioView(**usuario) for usuario in usuarios]
    finally:
        db.close()

def buscar_acessos_usuario(id_usuario):
    db = Database()
    try:
        query = """
            SELECT ta.* FROM TipoAcesso ta
            INNER JOIN Usuario_TipoAcesso uta ON ta.Id = uta.IdTipoAcesso
            WHERE uta.IdUsuario = ?
        """
        return db.fetch_all(query, (id_usuario,))
    finally:
        db.close()

def registrar(usuario: Usuario):
    db = Database()
    try:
        query = "INSERT INTO Usuario (Nome, Senha, Active, DataCriacao, DataUpdate) VALUES (?, ?, ?, GETDATE(), GETDATE())"
        usuario_id = db.executeAndReturnId(query, (usuario.nome, usuario.senha, usuario.active))
    finally:
        db.close()

def buscar_todos_tipo_acesso():
    db = Database()
    try:
        query = "SELECT * FROM TipoAcesso"
        acessos = db.fetch_all(query)
        for acesso in acessos:
            acesso['pages'] = buscar_paginas_acesso(acesso['id'])
        return [TipoAcessoView(**acesso) for acesso in acessos]
    finally:
        db.close()

def buscar_paginas_acesso(id_tipo_acesso):
    db = Database()
    try:
        query = """
            SELECT p.* FROM [Page] p
            INNER JOIN Acesso a ON p.Id = a.IdPage
            WHERE a.IdTipoAcesso = ?
        """
        return db.fetch_all(query, (id_tipo_acesso,))
    finally:
        db.close()

def registrar_acesso(tipo_acesso: TipoAcesso):
    db = Database()
    try:
        query = "INSERT INTO TipoAcesso (Nome, Active) VALUES (?, ?)"
        db.execute(query, (tipo_acesso.nome, tipo_acesso.active))
    finally:
        db.close()

def buscar_todos_pages():
    db = Database()
    try:
        query = "SELECT * FROM [Page]"
        return db.fetch_all(query)
    finally:
        db.close()

def registrar_pagina(page: Page):
    db = Database()
    try:
        query = "INSERT INTO [Page] (Nome, Url, Active) VALUES (?, ?, ?)"
        db.execute(query, (page.nome, page.url, page.active))
    finally:
        db.close()


def registrar_usuario_acesso(id_usuario,id_acesso):
    db = Database()
    try:
        query = "INSERT INTO Usuario_TipoAcesso (IdUsuario, IdTipoAcesso) VALUES (?,?)"
        db.execute(query, (id_usuario,id_acesso))
    finally:
        db.close()
def registrar_pagina_acesso(id_pagina,id_acesso):
    db = Database()
    try:
        query = "INSERT INTO Usuario (IdPage, IdTipoAcesso,Active) VALUES (?, ?,1)"
        db.execute(query, (id_pagina,id_acesso))
    finally:
        db.close()
def login(login):
    db = None
    try:
        db = Database()
        querry = """SELECT * FROM Usuario uso
                    LEFT JOIN [Login] l ON l.IdUsuario = uso.Id
                    WHERE l.CPFCRM = ? AND l.Password = ?"""
        response = db.fetch_one(querry,(login.cpfcrm,login.password))
        return response
    finally:
        db.close