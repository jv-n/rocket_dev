from fastapi import FastAPI
from app.routers import (
    pedidos,
    produtos,
    consumidores,
    vendedores,
    avaliacoes_pedido,
    itens_pedido

)

app = FastAPI(
    title="Sistema de Compras Online",
    description="API para gerenciamento de pedidos, produtos, consumidores e vendedores.",
    version="1.0.0",
)

app.include_router(pedidos.router)
app.include_router(produtos.router)
app.include_router(consumidores.router)
app.include_router(vendedores.router)
app.include_router(avaliacoes_pedido.router)
app.include_router(itens_pedido.router)

@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "API rodando com sucesso!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)