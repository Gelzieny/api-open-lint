from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from starlette.responses import RedirectResponse

from App.controller.model_controller import model_controller
from App.controller.provedor_controller import provedor_controller
from App.controller.ia_valida_ia_controller import ia_valida_ia_controller

app = FastAPI(
    title="LLM Evaluation Pipeline",
    description="API para gerenciar e avaliar o desempenho de modelos de linguagem (LLMs)."
)


app.include_router(provedor_controller)
app.include_router(model_controller)
app.include_router(ia_valida_ia_controller)

@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)