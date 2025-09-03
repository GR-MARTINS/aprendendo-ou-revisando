import sqlite3
from pathlib import Path


ROOT_PATH = Path(__file__).parent


def criar_conexao():
    with sqlite3.connect(ROOT_PATH / "clientes.db") as conn:
        return conn


# o exemplo de operações podem ser usados conforme descrito abaixo
# independente do banco utilizado, pois a implementação do connect
# em todos os bancos, segue os padrões da DB API do python.


def criar_tabela(conn, cursor):
    # mais de uma operação pode ser enviada ao mesmo tempo
    try:
        cursor.execute(
            """CREATE TABLE clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome VARCHAR(100),
                email VARCHAR(150))
            """
        )
        # executa as operações no banco
        conn.commit()
        return None

    except Exception as erro:
        # descarta as operações caso haja erro
        conn.rollback()
        return erro

    # se isso fosse feito de outra forma (fora do try except),
    # algumas das operações podem estar corretas e outras não.
    # sem o rollback, as operações que deram certo ainda ficariam
    # disponíveis para commit. Após a correção do erro nas operações
    # incorretas, um novo commit seria realizado e as operações corretas
    # seriam criadas em duplicidade.


conn = criar_conexao()

erro = criar_tabela(conn, conn.cursor())

if erro:
    print(f"Ocorreu um erro ao criar a tabela: {erro}")
else:
    print("Tabela criada com sucesso!")
