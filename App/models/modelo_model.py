from typing import Optional
from pydantic import BaseModel, Field

class Modelo(BaseModel):
    nome_modelo: Optional[str] = Field(
        default=...,
        description="Nome do modelo associado para registro ou filtro",
        example="modelo_v1"
    )
    codigo_provedor: str = Field(..., description="Código provedor")

