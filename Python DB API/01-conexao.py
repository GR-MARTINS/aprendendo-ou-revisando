# Passo 1 - instalar o driver do banco de dados no ambiente virtual.
# exemplos com o pip:
#    -mysql: pip install mysql-connector-python
#    -postgreSQL: pip install psycopg

# passo 2 - importar o drive do banco de dados. 
# Neste caso, o banco de dados é o sqlite.
import sqlite3
from pathlib import Path


ROOT_PATH = Path(__file__).parent

# passo 3 - Criara conexão. Indenpendente do banco, o padrão é o mesmo: 
#   - chamar a função connect e fornecer os dados para a conexão.
#   - os dados para conexão vão variar de acordo com o banco que está sendo utilizado.
conn = sqlite3.connect(ROOT_PATH/"clientes.db")
print(conn)

# Exemplos de conexão com outros bancos:
# conexão com postgreSQL
"""
import psycopg

try:
    conn = psycopg.connect(
            host="your_host",
            database="your_database",
            user="your_user",
            password="your_password"
        )
except psycopg.Error as erro:
    print(f"Error: {erro}")
"""
# conexão com mysql
"""
# conexão com mysql
import mysql.connector
try:
    conn = mysql.connector.connect(
            host="your_host",
            user="your_username",
            passwd="your_password",
            database="your_database"
        )
except mysql.connector.Error as erro:
    print(f"Error: {erro}")
        """
