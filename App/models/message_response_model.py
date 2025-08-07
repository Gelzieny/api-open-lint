from typing import Optional
from pydantic import BaseModel, Field

class MessageResponse(BaseModel):
    mensagem: str = Field(description="Exemplo de Mensagem", default='Valor Default')
    cod_retorno: int = Field()
