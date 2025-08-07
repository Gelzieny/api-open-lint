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

# import os
# from dotenv import load_dotenv

# load_dotenv()

# POSTGRES_PRODUCAO_DB = os.getenv('POSTGRES_PRODUCAO_DB')
# POSTGRES_PRODUCAO_USER = os.getenv('POSTGRES_PRODUCAO_USER')
# POSTGRES_PRODUCAO_HOST = os.getenv('POSTGRES_PRODUCAO_HOST')
# POSTGRES_PRODUCAO_PORT = os.getenv('POSTGRES_PRODUCAO_PORT')
# POSTGRES_PRODUCAO_PASSWORD = os.getenv('POSTGRES_PRODUCAO_PASSWORD')

# GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL')
# NODE_TLS_REJECT_UNAUTHORIZED = os.getenv('NODE_TLS_REJECT_UNAUTHORIZED')

# UPSTASH_VECTOR_REST_URL = os.getenv('UPSTASH_VECTOR_REST_URL')
# UPSTASH_VECTOR_REST_TOKEN = os.getenv('UPSTASH_VECTOR_REST_TOKEN')

# if not OLLAMA_BASE_URL:
#     print("A variável de ambiente OLLAMA_BASE_URL não está definida.")