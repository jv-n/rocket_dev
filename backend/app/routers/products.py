from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse

router = APIRouter(prefix="/products", tags=["Products"])


# GET /products/search/?query=...
@router.get("/search/", response_model=list[ProductResponse])
def search_products(query: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = db.query(Product).filter(Product.name.contains(query)).offset(skip).limit(limit).all()
    return products


# GET /products?category=...
@router.get("/", response_model=list[ProductResponse])
def list_products(category: str | None = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = db.query(Product)
    if category:
        products = products.filter(Product.category == category)
    return products.offset(skip).limit(limit).all()


# GET /products/{product_id}
@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: str, db: Session = Depends(get_db)):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


# POST /products
@router.post("/", response_model=ProductResponse, status_code=201)
def create_product(body: ProductCreate, db: Session = Depends(get_db)):
    product = Product(**body.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


# PATCH /products/{product_id}
@router.patch("/{product_id}", response_model=ProductResponse)
def patch_product(product_id: str, body: ProductUpdate, db: Session = Depends(get_db)):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(product, field, value)
    db.commit()
    db.refresh(product)
    return product


# DELETE /products/{product_id}
@router.delete("/{product_id}", status_code=204)
def delete_product(product_id: str, db: Session = Depends(get_db)):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
