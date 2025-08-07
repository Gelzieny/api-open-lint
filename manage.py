from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from starlette.responses import RedirectResponse

from App.controller.model_controller import model_controller
from App.controller.provedor_controller import provedor_controller

app = FastAPI(
    title="LLM Evaluation Pipeline",
    description="API para gerenciar e avaliar o desempenho de modelos de linguagem (LLMs)."
)


app.include_router(provedor_controller)
app.include_router(model_controller)

@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")