import os
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text

load_dotenv()

from App.utils.settings import settings, DatabaseType


class ConexaoPostgres:
    """
    Gerencia a conexão com o banco de dados PostgreSQL usando SQLAlchemy.
    Implementa o padrão Singleton para garantir uma única instância de pool de conexões.
    """
    _instance = None 

    def __new__(cls, *args, **kwargs):
        """
        Método chamado antes de __init__ para controlar a criação da instância.
        Garanta que apenas uma instância de ConexaoPostgres seja criada.
        """
        if cls._instance is None:
            cls._instance = super(ConexaoPostgres, cls).__new__(cls)
            cls._instance._initialize()  
        return cls._instance

    def _initialize(self):
        """
        Inicializa a conexão com o banco de dados. Este método é chamado apenas uma vez
        quando a primeira instância da classe ConexaoPostgres é criada.
        """
        
        if settings.DATABASE_TYPE.upper() == DatabaseType.POSTGRES:
            print("Iniciando conexão com o PostgreSQL...")
            self.database_url = (
                f"postgresql://{settings.POSTGRES_PRODUCAO_USER}"
                f":{settings.POSTGRES_PRODUCAO_PASSWORD}"
                f"@{settings.POSTGRES_PRODUCAO_HOST}"
                f":{settings.POSTGRES_PRODUCAO_PORT}"
                f"/{settings.POSTGRES_PRODUCAO_DB}"
            )
            engine_args = {
                "pool_size": 5,
                "max_overflow": 10,
                "pool_recycle": 3600,
                "pool_pre_ping": True
            }

        elif settings.DATABASE_TYPE.upper() == DatabaseType.SQLITE:
            print(f"Iniciando conexão com o SQLite em: {settings.SQLITE_DB_PATH}...")
            if not settings.SQLITE_DB_PATH:
                raise ValueError("A variável de ambiente SQLITE_DB_PATH deve ser definida quando DATABASE_TYPE é SQLITE.")
            
            self.database_url = f"sqlite:///{settings.SQLITE_DB_PATH}"
            # O argumento 'check_same_thread' é específico e recomendado para SQLite com FastAPI/Uvicorn
            engine_args = {"connect_args": {"check_same_thread": False}}
            
        else:
            # Lança um erro se um tipo de banco de dados inválido for fornecido
            raise ValueError(f"DATABASE_TYPE inválido: '{settings.DATABASE_TYPE}'. Use 'POSTGRES' ou 'SQLITE'.")

        try:
            self.engine = create_engine(self.database_url, **engine_args)

            with self.engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            print("Conexão com o PostgreSQL inicializada e testada com sucesso!")
        except Exception as e:

            print(f"ERRO: Falha crítica ao inicializar a conexão com o PostgreSQL: {e}")
            raise
        self.Session = sessionmaker(bind=self.engine)

    def executar_query(self, query: str, params: dict = None, commit: bool = False):
        session = self.Session()
        try:
            result = session.execute(text(query), params or {})
            if commit:
                session.commit()
                return {"success": True, "rows_affected": result.rowcount}
            return [dict(row._mapping) for row in result.fetchall()]
        except Exception as request_error:
            session.rollback()  # Em caso de erro, desfaz a transação
            print(f"Erro ao executar query: {request_error}")
            return {"success": False, "error": str(request_error)}
        finally:
            session.close() 

    def select(self, query: str, params: dict = None):
        return self.executar_query(query, params)

    def insert(self, query: str, params: dict = None):
        return self.executar_query(query, params, commit=True)

    def delete(self, query: str, params: dict = None):
        return self.executar_query(query, params, commit=True)

    def update(self, query: str, params: dict = None):
        return self.executar_query(query, params, commit=True) 
    
    def teste(self):
        try:
            r = self.select("SELECT 1;")
            if isinstance(r, list) and r and '?column?' in r[0]:
                resultado = r[0]['?column?']
                return {
                    "status": "success" if resultado == 1 else "error",
                    "resultado": "Conexão bem-sucedida" if resultado == 1 else "Falha na conexão"
                }
            else:
                return {
                    "status": "error",
                    "resultado": "Falha na conexão: Resposta inesperada da query de teste."
                }
        except Exception as e:
            return {
                "status": "error",
                "resultado": f"Falha na conexão: {e}"
            }