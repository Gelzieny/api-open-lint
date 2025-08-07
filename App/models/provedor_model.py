from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class ProvedorModel(BaseModel):
    nome_provedor: str = Field(
        default=...,
        description="Nome do provedor do LLM (ex: 'OpenAI', 'Google')."
    )