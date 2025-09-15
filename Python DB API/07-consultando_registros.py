import sqlite3
from pathlib import Path
from exceptions import (
    ErroDeConexao,
    ErroAoCriarTabelaCliente,
    ErroAoInserirCliente,
    ErroAoAtualizarCliente,
    ErroAoExcluirCliente,
    ErroAoInserirClientes,
    ErroAoBuscarCliente,
    ErroAoBuscarClientes,
    ErroAoListarClientesOrdenadosPorNome,
    ErroAoListarPorEmail,
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
        conn.rollback()
        raise ErroAoAtualizarCliente(f"Erro ao atualizar cliente! {erro}")


def excluir_registro(conexao, **kwargs):
    cursor = conexao.cursor()
    try:
        cursor.execute("DELETE FROM clientes WHERE id=?", (kwargs.get("id"),))
        conexao.commit()
    except Exception as erro:
        conexao.rollback()
        raise ErroAoExcluirCliente(f"Erro ao excluir cliente! {erro}")


def inserir_varios_registros(conexao, dados: list[tuple]):
    cursor = conexao.cursor()
    try:
        # dados é uma lista de tuplas [(nome1, email1), (nome2, email2)...]
        cursor.executemany("INSERT INTO clientes (nome, email) VALUES (?, ?)", dados)
        conexao.commit()
    except Exception as erro:
        conexao.rollback()
        raise ErroAoInserirClientes(f"Erro ao inserir clientes!{erro}")


def recuperar_cliente(conexao, id):
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT * FROM clientes WHERE id=?", (id,))
        resultado = cursor.fetchone()
        return resultado
    except Exception as erro:
        conexao.rollback()
        raise ErroAoBuscarCliente(f"Erro ao buscar cliente! {erro}")


def listar_clientes(conexao):
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT * FROM clientes")
        return cursor.fetchall()
    except Exception as erro:
        raise ErroAoBuscarClientes(f"Erro ao buscar clientes! {erro}")


def listar_clientes_ordenados_por_nome(conexao, ordem: str = "ASC"):
    """Busca todos os clientes no banco e ordena por nome

    Args:
        conexao (any): objeto de conexao com o banco de dados
        ordem (str): informe 'ASC' para ordenar de forma crescente e 'DESC'  para ordenar de forma decrescente.

    Returns:
        list[tuple]: lista de tuplas, onde cada tupla armazena as informações de um cliente.
    """
    try:
        cursor = conexao.cursor()
        # Nesse caso, não dá para passar a ordem através do place holder '?'
        # Já que os valores de ordem são conhecidos, para evitar
        # sql injection, use um if.
        if ordem not in ["ASC", "DESC"]:
            raise ErroAoListarClientesOrdenadosPorNome(
                "A ordem deve ser 'ASC' ou 'DESC'"
            )
        cursor.execute(f"SELECT * FROM clientes ORDER BY nome {ordem}")
        return cursor.fetchall()
    except Exception as erro:
        raise ErroAoListarClientesOrdenadosPorNome(
            f"Erro ao listar clientes ordenados por nome! {erro}"
        )


def listar_clientes_por_email(conexao, email):
    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM clientes WHERE email LIKE ?", (f"%{email}%",))
        return cursor.fetchall()
    except Exception as erro:
        raise ErroAoListarPorEmail(f"Erro ao listar clientes por email! {erro}")


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
        except Exception as erro:
            raise ErroAoExcluirCliente(f"Erro ao excluir cliente! {erro}")

    def inserir_varios_registros(self, dados: list[tuple]):
        try:
            with self.conexao as conn:
                cursor = conn.cursor()
                # dados é uma lista de tuplas [(nome1, email1), (nome2, email2)...]
                cursor.executemany(
                    "INSERT INTO clientes (nome, email) VALUES (?, ?)", dados
                )
        except Exception as erro:
            raise ErroAoInserirClientes(f"Erro ao inserir clientes!{erro}")

    def recuperar_cliente(self, id):
        try:
            with self.conexao as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM clientes WHERE id=?", (id,))
                resultado = cursor.fetchone()
                return resultado
        except Exception as erro:
            raise ErroAoBuscarCliente(f"Erro ao buscar cliente! {erro}")

    def listar_clientes(self):
        try:
            with self.conexao as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM clientes")
                return cursor.fetchall()
        except Exception as erro:
            raise ErroAoBuscarClientes(f"Erro ao buscar clientes! {erro}")

    def listar_clientes_ordenados_por_nome(self, ordem: str = "ASC"):
        """Busca todos os clientes no banco e ordena por nome

        Args:
            ordem (str): 'ASC' para ordenar de forma crescente e 'DESC'  para ordenar de forma decrescente.

        Returns:
            list[tuple]: lista de tuplas, onde cada tupla armazena as informações de um cliente.
        """
        try:
            with self.conexao as conn:
                cursor = conn.cursor()
                # Nesse caso, não dá para passar a ordem através do place holder '?'
                # Já que os valores de ordem são conhecidos, para evitar
                # sql injection, use um if.
                if ordem not in ["ASC", "DESC"]:
                    raise ErroAoListarClientesOrdenadosPorNome(
                        "A ordem deve ser 'ASC' ou 'DESC'"
                    )
                cursor.execute(f"SELECT * FROM clientes ORDER BY nome {ordem}")
                return cursor.fetchall()
        except Exception as erro:
            raise ErroAoListarClientesOrdenadosPorNome(
                f"Erro ao listar clientes ordenados por nome! {erro}"
            )

    def listar_clientes_por_email(self, email):
        try:
            with self.conexao as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM clientes WHERE email LIKE ?", (f"%{email}%",)
                )
                return cursor.fetchall()
        except Exception as erro:
            raise ErroAoListarPorEmail(f"Erro ao listar clientes por email! {erro}")


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
#     dados = [
#         ("Raimunda", "raimunda@gmail.com"),
#         ("Simba", "simba@gmail.com"),
#         ("Nala", "nala@gmail.com"),
#     ]
#     inserir_varios_registros(conn, dados)
#     print(f"Clientes cadastrados com Sucesso!")
#     print(recuperar_cliente(conn, 2))
#     print(listar_clientes(conn))
#     print(listar_clientes_ordenados_por_nome(conn, ordem="ASC"))
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
    dados = [
        ("Raimunda", "raimunda@gmail.com"),
        ("Simba", "simba@gmail.com"),
        ("Nala", "nala@gmail.com"),
    ]
    repo.inserir_varios_registros(dados)
    print(f"Clientes cadastrados com Sucesso!")
    print(repo.recuperar_cliente(2))
    print(repo.listar_clientes())
    print(repo.listar_clientes_ordenados_por_nome(ordem="ASC"))
    print(repo.listar_por_email(ordem="ASC"))

except Exception as erro:
    print(f"{erro}")
