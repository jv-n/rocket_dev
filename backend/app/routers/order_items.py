from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.order_item import OrderItem
from app.schemas.order_item import OrderItemCreate, OrderItemUpdate, OrderItemResponse

router = APIRouter(prefix="/order_items", tags=["OrderItems"])


# GET /order_items/{order_id}/{item_id}
@router.get("/{order_id}/{item_id}", response_model=OrderItemResponse)
def get_order_item(order_id: str, item_id: int, db: Session = Depends(get_db)):
    item = db.get(OrderItem, (order_id, item_id))
    if not item:
        raise HTTPException(status_code=404, detail="Order item not found")
    return item


# GET /order_items?order_id=...
@router.get("/", response_model=list[OrderItemResponse])
def list_order_items(order_id: str | None = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = db.query(OrderItem)
    if order_id:
        items = items.filter(OrderItem.order_id == order_id)
    return items.offset(skip).limit(limit).all()


# POST /order_items
@router.post("/", response_model=OrderItemResponse, status_code=201)
def create_order_item(body: OrderItemCreate, db: Session = Depends(get_db)):
    item = OrderItem(**body.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


# PATCH /order_items/{order_id}/{item_id}
@router.patch("/{order_id}/{item_id}", response_model=OrderItemResponse)
def patch_order_item(order_id: str, item_id: int, body: OrderItemUpdate, db: Session = Depends(get_db)):
    item = db.get(OrderItem, (order_id, item_id))
    if not item:
        raise HTTPException(status_code=404, detail="Order item not found")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(item, field, value)
    db.commit()
    db.refresh(item)
    return item


# DELETE /order_items/{order_id}/{item_id}
@router.delete("/{order_id}/{item_id}", status_code=204)
def delete_order_item(order_id: str, item_id: int, db: Session = Depends(get_db)):
    item = db.get(OrderItem, (order_id, item_id))
    if not item:
        raise HTTPException(status_code=404, detail="Order item not found")
    db.delete(item)
    db.commit()
