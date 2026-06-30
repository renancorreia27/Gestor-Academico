import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

class ConexaoMySQL:
    """Gerenciador de conexão com o MySQL utilizando o padrão Singleton."""
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(ConexaoMySQL, cls).__new__(cls)
            cls._instancia.conexao = None
        return cls._instancia

    def conectar(self):
        """Estabelece a conexão usando variáveis de ambiente de produção."""
        if self.conexao and self.conexao.is_connected():
            return self.conexao

        try:
            self.conexao = mysql.connector.connect(
                host=os.getenv('DB_HOST', 'localhost'),
                user=os.getenv('DB_USER', 'root'),
                password=os.getenv('DB_PASSWORD', ''),
                database=os.getenv('DB_NAME', 'gestor'),
                port=os.getenv('DB_PORT', '3307')
            )
            return self.conexao
        except Error as e:
            print(f"[ConexaoMySQL] Erro ao conectar: {e}")
            return None

    def fechar_conexao(self):
        """Encerra a conexão ativa."""
        if self.conexao and self.conexao.is_connected():
            self.conexao.close()
            self.conexao = None
