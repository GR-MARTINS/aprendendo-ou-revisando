import sqlite3
from pathlib import Path
from exceptions import (
    ErroDeConexao,
    ErroAoCriarTabelaCliente,
    ErroAoInserirCliente,
    ErroAoAtualizarCliente,
    ErroAoExcluirCliente,
)

ROOT_PATH = Path(__file__).parent

# Eu estava usando desta forma
# Isso não é uma boa prática

# def criar_conexao():
#     with sqlite3.connect(ROOT_PATH / "clientes.db") as conn:
#         # conn é retornado já fechado.
#         return conn


# Essa forma é mais adequada do que a anterior
def criar_conexao(driver, string_de_conexao):
    try:
        return driver.connect(string_de_conexao)

    except driver.Error as erro:
        raise ErroDeConexao(f"Erro ao conectar no banco! {erro}")


# o exemplo de operações pode ser usado conforme descrito abaixo
# independente do banco utilizado, pois a implementação do connect
# em todos os bancos, segue os padrões da DB API do python.

# lembrando! A melhor prática é o repositório, especialmente para projetos maiores.


def criar_tabela(conn):
    cursor = conn.cursor()

    # mais de uma operação pode ser enviada ao mesmo tempo
    try:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome VARCHAR(100),
                email VARCHAR(150))
            """
        )
        # executa as operações no banco
        conn.commit()

    except Exception as erro:
        # descarta as operações caso haja erro
        conn.rollback()
        conn.close()
        raise ErroAoCriarTabelaCliente(f"Erro ao criar tabela clientes! {erro}")

    # como não usamos o with no exemplo anterior,
    # se isso fosse feito de outra forma (fora do try except),
    # algumas das operações podem estar corretas e outras não.
    # sem o rollback, as operações que deram certo ainda ficariam
    # disponíveis para commit. Após a correção do erro nas operações
    # incorretas, um novo commit seria realizado e as operações corretas
    # seriam criadas em duplicidade.


def inserir_na_tabela(conn, **kwargs):
    cursor = conn.cursor()

    # extrutura identica a criada na função criar_conexao
    # todas as operações realizadas no banco serão inseridas
    # dessa forma, devido aos motivos comentados anteriormente
    # no escopo da função criar_conexao.
    try:
        # não devem ser criadas strings formatadas, elas possibilitam
        # slq injection atacks. Para evitar isso, deve ser passado dentro
        # da query os place holders "?" ou "%s" (a depender do banco utilizado)
        # e após a query, uma tupla contendo os dados.
        cursor.execute(
            "INSERT INTO clientes (nome, email) VALUES (?, ?)",
            (
                kwargs.get("nome"),
                kwargs.get("email"),
            ),
        )
        conn.commit()

    except Exception as erro:
        conn.rollback()
        raise ErroAoInserirCliente(f"Erro ao inserir cliente! {erro}")


def atualizar_registro(conn, **kwargs):
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE clientes SET nome=?, email=? WHERE id=?",
            (
                kwargs.get("nome"),
                kwargs.get("email"),
                kwargs.get("id"),
            ),
        )
        conn.commit()
    except Exception as erro:
        raise ErroAoAtualizarCliente(f"Erro ao atualizar cliente! {erro}")


def excluir_registro(conexao, **kwargs):
    cursor = conexao.cursor()
    try:
        cursor.execute("DELETE FROM clientes WHERE id=?", (kwargs.get("id"),))
        conexao.commit()
    except Exception as erro:
        raise ErroAoExcluirCliente(f"Erro ao excluir cliente! {erro}")


# Repositório
# o mais adequado seria assim:
class ClienteRepository:
    def __init__(self, driver, string_de_conexao):
        self.driver = driver
        try:
            self.conexao = driver.connect(string_de_conexao)
        except self.driver.Error as erro:
            raise ErroDeConexao(f"Erro ao conectar no banco! {erro}")

    def criar_tabela(self):
        try:
            with self.conexao as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """CREATE TABLE IF NOT EXISTS clientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome VARCHAR(100),
                    email VARCHAR(150))
                """
                )
        except self.driver.Error as erro:
            raise ErroAoCriarTabelaCliente(f"Erro ao criar tabela clientes! {erro}")

    def inserir_na_tabela(self, **kwargs):
        try:
            with self.conexao as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO clientes (nome, email) VALUES (?, ?)",
                    (
                        kwargs.get("nome"),
                        kwargs.get("email"),
                    ),
                )
        except self.driver.Error as erro:
            raise ErroAoInserirCliente(f"Erro ao inserir cliente! {erro}")

    def atualizar_registro(self, **kwargs):
        try:
            with self.conexao as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE clientes SET nome=?, email=? WHERE id=?",
                    (
                        kwargs.get("nome"),
                        kwargs.get("email"),
                        kwargs.get("id"),
                    ),
                )
        except Exception as erro:
            raise ErroAoAtualizarCliente(f"Erro ao atualizar cliente! {erro}")

    def excluir_registro(self, **kwargs):
        try:
            with self.conexao as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM clientes WHERE id=?", (kwargs.get("id"),))
                self.conexao.commit()
        except Exception as erro:
            raise ErroAoExcluirCliente(f"Erro ao excluir cliente! {erro}")

# EXEMPLOS DE EXECUÇÃO

string_de_conexao = ROOT_PATH / "cliente.db"

# via função
# try:
#     conn = criar_conexao(sqlite3, string_de_conexao)
#     criar_tabela(conn)
#     print("Tabela criada com sucesso!")
#     dados = {"nome": "teste", "email": "teste@email.com"}
#     inserir_na_tabela(conn, nome=dados.get("nome"), email=dados.get("email"))
#     print(f"Cadastro do cliente {dados.get("nome")} realizado com sucesso!")
#     dados = {"id": 1, "nome": "teste 01", "email": "teste01@email.com"}
#     atualizar_registro(conn, **dados)
#     print(f"Cadastro do cliente {dados.get("nome")} atualizado com sucesso!")
#     excluir_registro(conn, **dados)
#     print(f"Cadastro do cliente {dados.get("nome")} excluido com sucesso!")
#     conn.close()

# except Exception as erro:
#     print(f"{erro}")

# via repositorio
try:
    repo = ClienteRepository(sqlite3, string_de_conexao)
    repo.criar_tabela()
    print("Tabela criada com sucesso!")
    dados = {"nome": "teste", "email": "teste@email.com"}
    repo.inserir_na_tabela(nome=dados.get("nome"), email=dados.get("email"))
    print(f"Cadastro do cliente {dados.get("nome")} realizado com sucesso!")
    dados = {"id": 1, "nome": "teste 01", "email": "teste01@email.com"}
    repo.atualizar_registro(**dados)
    print(f"Cadastro do cliente {dados.get("nome")} atualizado com sucesso!")
    repo.excluir_registro(**dados)
    print(f"Cadastro do cliente {dados.get("nome")} excluido com sucesso!")
except Exception as erro:
    print(f"{erro}")
