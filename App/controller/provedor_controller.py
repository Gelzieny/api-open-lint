from fastapi import APIRouter, Body, Depends, HTTPException

from App.utils.utils import *
from App.dependencias.database import ConexaoDB
from App.repository.provedor_repository import AprovedorRepository

provedor_controller = APIRouter()

def get_db_connection():
    # Aqui você pode criar uma instância da classe ConexaoDB ou recuperar uma instância existente
    return ConexaoDB() # Retorna a instância singleton


def get_provedor_repository(db: ConexaoDB = Depends(get_db_connection)):
    """
        Função de dependência para obter o AprovedorRepository
        Ele depende de get_db_connection para obter a instância da conexão.
    """
    return AprovedorRepository(db)

@provedor_controller.get(
    "/list-provedor",
    tags=["Provedor"],
    summary="Listar provedor",
    description="""
    Retorna uma lista de provedores disponíveis no sistema.

    ### Funcionalidade
    Este endpoint consulta a base de dados e retorna todos os provedores registrados, incluindo:
    - **Nome provedor**

    ### Respostas
    - **200 OK**: Lista de provedores retornada com sucesso
    - **500 Internal Server Error**: Falha na obtenção dos provedores
    """,
)
async def list_provedor(repo: AprovedorRepository = Depends(get_provedor_repository)):
    """
        Lista todos os provedores cadastrados no sistema.
        Retorna uma lista com os campo 'nome_provedor'.  
    """
    
    result = repo.list_provedor([])

    # Adaptação para o caso de erro onde 'result' pode ser um dict com 'error'
    if isinstance(result, dict) and result.get('success') is False:
        raise HTTPException(status_code=500, detail=result.get('error', 'Erro desconhecido ao listar nome_provedor'))

    return { "models": result } 
