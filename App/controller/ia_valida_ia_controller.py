from fastapi import APIRouter, Body, Depends, HTTPException

from App.utils.ia import get_model, use_upstash_index
from App.utils.utils import *

from typing import Literal, Optional
from pydantic import BaseModel, Field

from langchain_core.prompts import ChatPromptTemplate

class AvaliacaoRespostaModeloSchema(BaseModel):
    """
    Esquema Pydantic para avaliar a resposta de um modelo de IA
    com base em um prompt de RAG (Retrieval Augmented Generation).
    """
    # Detalhes do contexto original e da interação
    perguntaDoUsuario: str = Field(description="A pergunta original feita pelo usuário ao modelo.")
    respostaDoModelo: str = Field(description="A resposta gerada pelo modelo que está sendo avaliada.")

    # Critérios de Avaliação
    exclusivamenteBaseadoNoContexto: bool = Field(
        description="Indica se a resposta se baseou exclusivamente no contexto fornecido."
    )
    comentarioExclusivamenteBaseadoNoContexto: Optional[str] = Field(
        default=None,
        description="Comentários adicionais se a resposta não foi exclusivamente baseada no contexto (ex: informações externas identificadas)."
    )

    diretoEConciso: bool = Field(description="Indica se a resposta foi direta e concisa.")
    comentarioDiretoEConciso: Optional[str] = Field(
        default=None,
        description="Comentários adicionais se a resposta não foi direta e concisa."
    )
    
    citouFontes: Literal['Sim', 'Não', 'Não aplicável'] = Field(
        description="Indica se o modelo citou suas fontes, se aplicável."
    )
    comentarioCitouFontes: Optional[str] = Field(
        default=None,
        description="Comentários adicionais se a citação de fontes foi inadequada ou ausente quando necessária."
    )

    gerenciouRespostaIncompletaCorretamente: Literal['Sim', 'Não', 'Não aplicável'] = Field(
        description="Indica se o modelo gerenciou corretamente a ausência de informações para a resposta."
    )
    comentarioGerenciouRespostaIncompletaCorretamente: Optional[str] = Field(
        default=None,
        description="Comentários adicionais se o gerenciamento da resposta incompleta foi incorreto (ex: tentou inferir ou adivinhar)."
    )

    alucinacaoOuInferenicaNaoJustificada: bool = Field(
        description="Indica se a resposta contém alucinação ou inferência não justificada."
    )
    comentarioAlucinacaoOuInferenicaNaoJustificada: Optional[str] = Field(
        default=None,
        description="Comentários adicionais se houve alucinação ou inferência não justificada, com exemplos se possível."
    )

    pontuacaoGeral: int = Field(
        ge=0, le=5,
        description="Pontuação geral da resposta, de 1 (Muito Ruim) a 5 (Excelente). Se o modelo alucinou, Zero (0)."
    )

    comentariosFinaisAvaliador: Optional[str] = Field(
        default=None,
        description="Comentários adicionais ou observações finais do avaliador."
    )

ia_valida_ia_controller = APIRouter()

@ia_valida_ia_controller.get(
    "/ia-valida-ia",
    tags=["validação"],
    summary="IA valida outra IA",
)
async def list_aleatorio():
    """
        Lista todos os provedores cadastrados no sistema.
        Retorna uma lista com os campo 'nome_provedor'.  
    """
    query = 'teste'
    
    index = use_upstash_index()
    llm = get_model( provider='gemini', model_name='gemini-2.5-flash' )
    
    results = index.query(
        data=query,
        top_k=10,
        include_metadata=True, 
    )
    
    if not results:
        return f"Nenhum resultado encontrado para '{query}'."

    system_template = """
    **Instruções para o Avaliador:**

    Você recebeu uma **[Pergunta]** do usuário, um **[Contexto]** e a **[Resposta do Modelo]** gerada com base nas instruções fornecidas. Sua tarefa é avaliar a qualidade da **[Resposta do Modelo]** em relação às regras estabelecidas.

    **[Contexto Original da Pergunta do Usuário]**
    ```
    {rag}
    ```

    **[Pergunta do Usuário]**
    {user_question}
    """
    
    model_template = """
    **[Resposta do Modelo]**
    {model_response}
    """

    formatted_results = "\n---\n".join(
        [f"Fonte: {res.metadata.get('source', 'N/A')}\nConteúdo: {res.metadata.get('_pageContentLC', 'N/A')}" for res in results]
    )
    
    structured_llm = llm.with_structured_output(AvaliacaoRespostaModeloSchema)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_template),
        ("human", model_template),
    ])
    
    chain = prompt | structured_llm

    # Invoca a cadeia com os parâmetros necessários
    return await chain.ainvoke({
        "rag": formatted_results, # Substituído pelo exemplo
        "user_question": 'resposta de teste',
        "model_response": query
    })