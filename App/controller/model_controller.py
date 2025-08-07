from fastapi import APIRouter, Body, Depends, HTTPException

from App.utils.utils import *
from App.models.modelo_model import Modelo
from App.dependencias.database import ConexaoPostgres
from App.repository.model_repository import ModeloRepository

model_controller = APIRouter()

def get_db_connection():
  # Aqui você pode criar uma instância da classe ConexaoPostgres ou recuperar uma instância existente
  return ConexaoPostgres() # Retorna a instância singleton


def get_model_repository(db: ConexaoPostgres = Depends(get_db_connection)):
    """
        Função de dependência para obter o ModeloRepository
        Ele depende de get_db_connection para obter a instância da conexão.
    """
    return ModeloRepository(db)

@model_controller.get(
    "/list-model",
    tags=["Modelos"],
    summary="Listar Modelos",
    description="""
    Retorna uma lista de modelos disponíveis no sistema.

    ### Funcionalidade
    Este endpoint consulta a base de dados e retorna todos os modelos registrados, incluindo:
    - **Nome modelo**

    ### Respostas
    - **200 OK**: Lista de modelos retornada com sucesso
    - **500 Internal Server Error**: Falha na obtenção dos modelos
    """,
)
async def list_model(repo: ModeloRepository = Depends(get_model_repository)):
    """
        Lista todos os modelos cadastrados no sistema.
        Retorna uma lista com os campo 'nome_modelo'.  
    """
    
    result = repo.list_modelo([])

    # Adaptação para o caso de erro onde 'result' pode ser um dict com 'error'
    if isinstance(result, dict) and result.get('success') is False:
        raise HTTPException(status_code=500, detail=result.get('error', 'Erro desconhecido ao listar modelos'))

    # modelos = [item["nome_modelo"] for item in result]
    # modelos_ordenados = sorted(modelos)

    return { "models": result } 


@model_controller.post(
    "/create-model",
    tags=["Modelos"],
    summary="Cadastrar novo modelo",
    description="""
    Cadastrar um novo modelo no sistema com os dados fornecidos.

    ### Regras:
    - O campos nome_modelo e obrigatório.

        ### Exemplo de requisição:
        ```json
        {
        "nome_modelo": "modelo",
        "codigo_provedor: codigo_provedor
        }
        ```

    ### Funcionalidade
    Este endpoint permite cadastrar um novo modelo no sistema.

    ### Respostas
    - **200 OK**: Modelo cadastrado com sucesso.
    - **400 Bad Request**: Campos obrigatórios não fornecidos.
    - **500 Internal Server Error**: Erro ao cadastrar o modelo.
    """,
)
async def create_model(model: Modelo = Body(), repo: ModeloRepository = Depends(get_model_repository)):
    """
        Cria um novo modelo no sistema.
        - **nome_modelo**: nome único do modelo
        - **codigo_provedor**: código provedor
    """
    param = {
        'nome_modelo': model.nome_modelo,
        'codigo_provedor': model.codigo_provedor
    }

    campos_vazios = [k for k, v in param.items() if not v or str(v).strip() == '']

    if campos_vazios:
        raise HTTPException(status_code=400, detail=f"O seguinte campo é obrigatório e está vazio: {', '.join(campos_vazios)}")

    result = repo.create_modelo(param)  

    if result.get('success') is False:
        raise HTTPException(status_code=500, detail=result.get('error', 'Erro desconhecido ao cadastrar modelo'))

    return result


@model_controller.post(
    "/delete-modelos",
    tags=["Modelos"],
    summary="Deletar modelo",
    description="""
    Remove um modelo específico do sistema com base no nome fornecido.

    ### Regras:
    - O campos nome_modelo e codigo_provedor são obrigatórios.

        ### Exemplo de requisição:
        ```json
        {
        "nome_modelo": "modelo_a_ser_removido",
        "codigo_provedor: codigo_provedor
        }
        ```

    ### Funcionalidade
    Remove um modelo existente no sistema com base no nome fornecido.

    ### Respostas
    - **200 OK**: Modelo removido com sucesso.
    - **400 Bad Request**: Campos obrigatórios não fornecidos.
    - **404 Not Found: Modelo não encontrado.
    - **500 Internal Server Error**: Erro ao remove o modelo.
    """,
)
async def deletar_modelo(model: Modelo = Body(), repo: ModeloRepository = Depends(get_model_repository)):
    """
        Remove um modelo existente no sistema com base no nome fornecido.
        - **nome_modelo**: nome do modelo a ser removido
        - **codigo_provedor**: código vinculado ao modelo
    """

    param = {
        'nome_modelo': model.nome_modelo,
        'codigo_provedor': model.codigo_provedor,
        'stat_modelo': 'A'
    }
    
    
    campos_vazios = [k for k, v in param.items() if not v or str(v).strip() == '']

    if campos_vazios:
        raise HTTPException(status_code=400, detail=f"O seguinte campo é obrigatório e está vazio: {', '.join(campos_vazios)}")

    result = repo.update_modelo(retira_vazios(param))

    if not result:
        raise HTTPException(
            status_code=404,
            detail= result
        )

    return result            