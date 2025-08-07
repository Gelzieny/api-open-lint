import os
from typing import Literal, Union, Dict

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from langchain_community.llms import Ollama
from langchain_google_genai import ChatGoogleGenerativeAI
from upstash_vector import Index


# Importa as variáveis de ambiente específicas do seu módulo App.utils.environment
# Certifique-se de que este módulo está configurado corretamente
from App.utils.settings import settings

PROVIDERS = {
    "OLLAMA": "ollama",
    "GEMINI": "gemini",
}

ProviderType = Literal[PROVIDERS["OLLAMA"], PROVIDERS["GEMINI"]]

# --- Funções de Utilitário (não precisam ser alteradas) ---
_index = None

def use_upstash_index() -> Index:
    """
    Retorna uma instância singleton do cliente Upstash Vector.
    """
    global _index
    if _index is None:
        upstash_vector_url = settings.UPSTASH_VECTOR_REST_URL
        upstash_vector_token = settings.UPSTASH_VECTOR_REST_TOKEN

        if not upstash_vector_url or not upstash_vector_token:
            raise ValueError("UPSTASH_VECTOR_REST_URL and UPSTASH_VECTOR_REST_TOKEN must be set.")

        _index = Index(url=upstash_vector_url, token=upstash_vector_token)
    return _index

# A função get_model precisa ser adaptada para aceitar os parâmetros diretamente
def get_model(provider, model: str) -> Union[Ollama, ChatGoogleGenerativeAI]:
    """
    Cria e retorna uma instância do modelo de linguagem (LLM) apropriado.
    """
    llm = None
    if provider == PROVIDERS["OLLAMA"]:
        ollama_base_url = settings.OLLAMA_BASE_URL or "http://localhost:11434"
        llm = Ollama(
            base_url=ollama_base_url,
            model=model
        )
    elif provider == PROVIDERS["GEMINI"]:
        gemini_api_key = os.environ.get("GEMINI_API_KEY")
        if not gemini_api_key:
            raise ValueError("GEMINI_API_KEY must be set for the GEMINI provider.")
        llm = ChatGoogleGenerativeAI(
            model=model,
            api_key=gemini_api_key
        )
    else:
        raise ValueError("Invalid provider")

    return llm