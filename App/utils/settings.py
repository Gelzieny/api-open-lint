import enum 
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class DatabaseType(str, enum.Enum):
    SQLITE = "SQLITE"
    POSTGRES = "POSTGRES"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    DATABASE_TYPE: DatabaseType = DatabaseType.SQLITE

    SQLITE_DB_PATH: Optional[str] = None
    
    POSTGRES_PRODUCAO_DB: str
    POSTGRES_PRODUCAO_USER: str
    POSTGRES_PRODUCAO_HOST: str
    POSTGRES_PRODUCAO_PORT: int
    POSTGRES_PRODUCAO_PASSWORD: str
    
    
    GEMINI_API_KEY: str
    OLLAMA_BASE_URL: str
    NODE_TLS_REJECT_UNAUTHORIZED: int
    UPSTASH_VECTOR_REST_URL: str
    UPSTASH_VECTOR_REST_TOKEN: str
    
settings = Settings()
