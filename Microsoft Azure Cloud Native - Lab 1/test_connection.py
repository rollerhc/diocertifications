import pymysql
from dotenv import load_dotenv
import os

# Carregar variáveis do arquivo .env
load_dotenv()

# Definir variáveis a partir do arquivo .env
SQL_Server = os.getenv("SQL_SERVER")
SQL_Database = os.getenv("SQL_DATABASE")
SQL_UserName = os.getenv("SQL_USERNAME")
SQL_Password = os.getenv("SQL_PASSWORD")

# Função para testar conexão com o banco de dados
def test_sql_connection():
    try:
        print("Variáveis carregadas:")
        print(f"SQL_SERVER: {SQL_Server}")
        print(f"SQL_DATABASE: {SQL_Database}")
        print(f"SQL_USERNAME: {SQL_UserName}")
        print(f"SQL_PASSWORD: {SQL_Password}")
        print("Testando conexão com o banco de dados...")
        
        connection = pymysql.connect(
            host=SQL_Server,
            user=SQL_UserName,
            password=SQL_Password,
            database=SQL_Database,
            connect_timeout=30,  # Timeout ajustável
            ssl={"ssl": {}}  # Adicione SSL se necessário
        )

        print("Conexão com o banco de dados realizada com sucesso!")
        connection.close()
    except pymysql.MySQLError as sql_error:
        print(f"Erro de SQL: {sql_error}")
    except Exception as e:
        print(f"Erro inesperado: {type(e).__name__} - {e}")

# Executar o teste
test_sql_connection()

