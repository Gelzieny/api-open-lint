import os
from typing import Union, Literal

from App.utils.settings import settings
from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI
from upstash_vector import Index

# Define os provedores de modelo como literais para verificação de tipo
PROVIDERS = {
    "OLLAMA": "ollama",
    "GEMINI": "gemini",
}

# Variável global para armazenar a instância do índice Upstash (padrão singleton)
_index = None

def use_upstash_index() -> Index:
    # TODO: Substituir os literais por variáveis globais.
    """
    Inicializa e retorna uma instância singleton do cliente Upstash Vector Index.

    As credenciais são obtidas a partir das variáveis de ambiente:
    - UPSTASH_VECTOR_REST_URL
    - UPSTASH_VECTOR_REST_TOKEN

    Returns:
        Uma instância da classe upstash_vector.Index.
    """
    global _index
    if _index is None:
        _index = Index(
            url=settings.UPSTASH_VECTOR_REST_URL,
            token=settings.UPSTASH_VECTOR_REST_TOKEN,
        )
    return _index

def get_model(provider: Literal["ollama", "gemini"], model_name: str) -> Union[ChatOllama, ChatGoogleGenerativeAI]:
    # TODO: Substituir os literais por variáveis globais.
    """
    Obtém uma instância de um modelo de linguagem com base no provedor e no nome do modelo especificados.

    Args:
        provider: O provedor do modelo ('ollama' ou 'gemini').
        model_name: O nome do modelo a ser utilizado.

    Returns:
        Uma instância de ChatOllama ou ChatGoogleGenerativeAI.

    Raises:
        ValueError: Se um provedor inválido for especificado.
    """
    if provider == PROVIDERS["OLLAMA"]:
        return ChatOllama(
            base_url=settings.OLLAMA_BASE_URL,
            model=model_name,
        )
    elif provider == PROVIDERS["GEMINI"]:
        return ChatGoogleGenerativeAI(
            model=model_name,
            google_api_key=settings.GEMINI_API_KEY,
        )
    else:
        raise ValueError("Provedor inválido especificado.")
