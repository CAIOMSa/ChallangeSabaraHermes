from database.connection import Database
from utils.Logs import registrar_erro

def buscar_todos():
        db = None
        try:
            db = Database()

            query = "SELECT * FROM Produtos"
            retorno = db.fetch_all(query)
            return retorno
        except Exception as e:
            registrar_erro(str(e))
            print(f"Erro ao buscar os produtos: {e}")
            return f"Erro: {str(e)}"
        finally:
            if db:
                db.close()

def buscar_pelo_id(id):
        db = None
        try:
            db = Database()

            query = "SELECT * FROM Produtos WHERE Id = ?"
            retorno = db.fetch_one(query, (int(id),))
            return retorno
        except Exception as e:
            registrar_erro(str(e))
            print(f"Erro ao buscar o produto de id {id}: {e}")
            return f"Erro: {str(e)}"
        finally:
            if db:
                db.close()
def buscar_por_nome(nome):
        db = None
        try:
            db = Database()

            query = "SELECT * FROM Produtos WHERE Nome = ?"
            retorno = db.fetch_one(query, (nome,))
            return retorno
        except Exception as e:
            registrar_erro(str(e))
            print(f"Erro ao buscar o produto de nome {nome}: {e}")
            return f"Erro: {str(e)}"
        finally:
            if db:
                db.close()

def atualizar_quantidade_produto(id,quant):
        db = None
        try:
            db = Database()
            atual = buscar_pelo_id(id)
            print(atual)
            quantidade = quant + atual["quantidade"]
            query = "UPDATE Produtos SET Quantidade = ? WHERE Id = ?"
            retorno = db.execute(query, (quantidade,int(id)))
            return retorno
        except Exception as e:
            registrar_erro(str(e))
            print(f"Erro ao carregar lote {id}: {e}")
            return f"Erro: {str(e)}"
        finally:
            if db:
                db.close()

def registrar(produto):
    db = None
    try:
        db = Database()

        query = "INSERT INTO Produtos (Nome, Descricao, Fabricante, Quantidade) VALUES (?, ?, ?, 0)"
        values = (produto.nome, produto.descricao, produto.fabricante)
        db.execute(query, values)

        return "sucesso"
    except Exception as e:
        registrar_erro(str(e))
        print(f"Erro ao registrar produto: {e}")
        return f"Erro: {str(e)}"
    finally:
        if db:
            db.close()


def registrar_lote(lote):
    db = None
    try:
        db = Database()
        atualizar_quantidade_produto(lote.id_produto,lote.quantidade)
        query = "INSERT INTO LoteEntrada (IdProduto, Quantidade,Distribuidor, DataValidade) VALUES (?, ?, ?)"
        values = (lote.id_produto, lote.quantidade,lote.distribuidor, lote.data_validade)
        db.execute(query, values)

        return "sucesso"
    except Exception as e:
        registrar_erro(str(e))
        print(f"Erro ao registrar produto: {e}")
        return f"Erro: {str(e)}"
    finally:
        if db:
            db.close()

def buscar_todos_lotes():
    db = None
    try:
        db = Database()
        query = "SELECT * FROM LoteEntrada"
        retorno = db.fetch_all(query)
        for lote in retorno:
            try:
                produto = buscar_pelo_id(lote["idproduto"])
                lote["produto"] = produto
                lote["data_validade"] = lote["datavalidade"]
                lote["data_recebimento"] = lote["datarecebimento"]
            except Exception as e:
                registrar_erro(str(e))
                print(f"Erro ao buscar produto do lote {lote['id']}: {e}")
                lote["produto"] = None  # Ou um dict vazio padrão

        return retorno

    except Exception as e:
        registrar_erro(str(e))
        print(f"Erro ao buscar os lotes: {e}")
        raise Exception(f"Erro ao buscar os lotes: {e}")  # <--- AQUI

    finally:
        if db:
            db.close()