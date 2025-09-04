import sqlite3
from pathlib import Path


ROOT_PATH = Path(__file__).parent


# Eu estava usando desta forma
# Isso não é uma boa prática
def criar_conexao():
    with sqlite3.connect(ROOT_PATH / "clientes.db") as conn:
        # conn é retornado já fechado.
        return conn


# o mais adequado seria assim:
class ClienteRepository:
    def __init__(self, driver, string_de_conexao):
        self.driver = driver
        self.conexao = driver.connect(string_de_conexao)

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
        except self.driver.Error:
            raise


# o exemplo de operações pode ser usado conforme descrito abaixo
# independente do banco utilizado, pois a implementação do connect
# em todos os bancos, segue os padrões da DB API do python.

# lembrando! A melhor prática é o repositório, especialmente para projetos maiores.


def criar_tabela(driver, string_de_conexao):
    conn = driver.connect(string_de_conexao)
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

    except driver.Error:
        # descarta as operações caso haja erro
        conn.rollback()
        conn.close()
        raise

    # como não usamos o with no exemplo anterior,
    # se isso fosse feito de outra forma (fora do try except),
    # algumas das operações podem estar corretas e outras não.
    # sem o rollback, as operações que deram certo ainda ficariam
    # disponíveis para commit. Após a correção do erro nas operações
    # incorretas, um novo commit seria realizado e as operações corretas
    # seriam criadas em duplicidade.


# EXEMPLOS DE EXECUÇÃO

# via função
string_de_conexao = ROOT_PATH / "cliente.db"

try:
    criar_tabela(sqlite3, string_de_conexao)
    print("Tabela criada com sucesso!")

except Exception as erro:
    print(f"Ocorreu um erro ao criar a tabela: {erro}")

# via repositorio
repo = ClienteRepository(sqlite3, string_de_conexao)

try:
    repo.criar_tabela()
    print("Tabela criada com sucesso!")
except Exception as erro:
    print(f"Ocorreu um erro ao criar a tabela: {erro}")
