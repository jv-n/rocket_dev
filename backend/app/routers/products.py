import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.order_item import OrderItem
from app.models.product import Product
from app.schemas.product import BestSellingProductResponse, ProductCreate, ProductUpdate, ProductResponse, ProductSalesResponse

router = APIRouter(prefix="/products", tags=["Products"])


# GET /products/search/?query=...
@router.get("/search/", response_model=list[ProductResponse])
def search_products(query: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = db.query(Product).filter(Product.name.contains(query)).offset(skip).limit(limit).all()
    return products

#GET /products/count
@router.get("/count")
def count_products(db: Session = Depends(get_db)):
    total = db.query(func.count(Product.product_id)).scalar() or 0
    return {"total_products": total}

# GET /products?category=...
@router.get("/", response_model=list[ProductResponse])
def list_products(category: str | None = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = db.query(Product)
    if category:
        products = products.filter(Product.category == category)
    return products.offset(skip).limit(limit).all()


# GET /products/best-selling?limit=10
@router.get("/best-selling", response_model=list[BestSellingProductResponse])
def best_selling_products(limit: int = 10, db: Session = Depends(get_db)):
    rows = (
        db.query(
            Product,
            func.count(OrderItem.order_id).label("orders_count"),
            func.sum(OrderItem.price_brl).label("total_revenue"),
        )
        .join(OrderItem, Product.product_id == OrderItem.product_id)
        .group_by(Product.product_id)
        .order_by(func.count(OrderItem.order_id).desc())
        .limit(limit)
        .all()
    )
    return [
        BestSellingProductResponse(
            **product.__dict__,
            orders_count=orders_count,
            total_revenue=round(total_revenue, 2),
        )
        for product, orders_count, total_revenue in rows
    ]


# GET /products/{product_id}/sales
@router.get("/{product_id}/sales", response_model=ProductSalesResponse)
def get_product_sales(product_id: str, db: Session = Depends(get_db)):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    row = (
        db.query(
            func.count(OrderItem.order_id).label("orders_count"),
            func.sum(OrderItem.price_brl).label("total_revenue"),
            func.sum(OrderItem.freight_price).label("total_freight"),
        )
        .filter(OrderItem.product_id == product_id)
        .one()
    )
    return ProductSalesResponse(
        product_id=product_id,
        orders_count=row.orders_count or 0,
        total_revenue=round(row.total_revenue or 0, 2),
        total_freight=round(row.total_freight or 0, 2),
    )


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
    product = Product(product_id=uuid.uuid4().hex, **body.model_dump())
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
