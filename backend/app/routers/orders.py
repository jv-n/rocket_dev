import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.order import Order
from app.schemas.order import OrderCreate, OrderUpdate, OrderResponse

router = APIRouter(prefix="/orders", tags=["Orders"])


# GET /orders/{order_id}
@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: str, db: Session = Depends(get_db)):
    order = db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


# GET /orders
@router.get("/", response_model=list[OrderResponse])
def list_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    orders = db.query(Order).offset(skip).limit(limit).all()
    return orders


# POST /orders
@router.post("/", response_model=OrderResponse, status_code=201)
def create_order(body: OrderCreate, db: Session = Depends(get_db)):
    order = Order(order_id=uuid.uuid4().hex, **body.model_dump())
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


# PUT /orders/{order_id}
@router.put("/{order_id}", response_model=OrderResponse)
def update_order(order_id: str, body: OrderCreate, db: Session = Depends(get_db)):
    order = db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    for field, value in body.model_dump().items():
        setattr(order, field, value)
    db.commit()
    db.refresh(order)
    return order


# PATCH /orders/{order_id}
@router.patch("/{order_id}", response_model=OrderResponse)
def patch_order(order_id: str, body: OrderUpdate, db: Session = Depends(get_db)):
    order = db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(order, field, value)
    db.commit()
    db.refresh(order)
    return order


# DELETE /orders/{order_id}
@router.delete("/{order_id}", status_code=204)
def delete_order(order_id: str, db: Session = Depends(get_db)):
    order = db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(order)
    db.commit()
