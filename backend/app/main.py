from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import (
    orders,
    products,
    customers,
    sellers,
    order_reviews,
    order_items,
    image_categories,
)

app = FastAPI(
    title="Online Shopping System",
    description="API for managing orders, products, customers, and sellers.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(orders.router)
app.include_router(products.router)
app.include_router(customers.router)
app.include_router(sellers.router)
app.include_router(order_reviews.router)
app.include_router(order_items.router)
app.include_router(image_categories.router)


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "API running successfully!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
