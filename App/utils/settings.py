from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')
    
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
