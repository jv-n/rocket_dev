from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.item_pedido import ItemPedido
from app.schemas.item_pedido import ItemPedidoCreate, ItemPedidoUpdate, ItemPedidoResponse

router = APIRouter(prefix="/itens_pedidos", tags=["ItensPedidos"])

# GET /itens_pedidos/{id_pedido}/(id_item)
@router.get("/{id_pedido}/{id_item}", response_model=ItemPedidoResponse)
def get_item(id_pedido: str, id_item: int, db: Session = Depends(get_db)):
    item = db.get(ItemPedido, (id_pedido, id_item))
    if not item:
        raise HTTPException(status_code=404, detail="Item do pedido não encontrado")
    return item

#GET /itens_pedidos?id_pedido=...
@router.get("/", response_model=list[ItemPedidoResponse])
def list_itens(id_pedido: str | None = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    itens = db.query(ItemPedido)
    if id_pedido:
        itens = itens.filter(ItemPedido.id_pedido == id_pedido)
    return itens.offset(skip).limit(limit).all()

# POST /itens_pedidos
@router.post("/", response_model=ItemPedidoResponse, status_code=201)
def create_item(body: ItemPedidoCreate, db: Session = Depends(get_db)):
    item = ItemPedido(**body.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

# PATCH /itens_pedidos/{id_pedido}/{id_item}
@router.patch("/{id_pedido}/{id_item}", response_model=ItemPedidoResponse)
def patch_item(id_pedido: str, id_item: int, body: ItemPedidoUpdate, db: Session = Depends(get_db)):
    item = db.get(ItemPedido, (id_pedido, id_item))
    if not item:
        raise HTTPException(status_code=404, detail="Item do pedido não encontrado")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(item, field, value)
    db.commit()
    db.refresh(item)
    return item

# DELETE /itens_pedidos/{id_pedido}/{id_item}
@router.delete("/{id_pedido}/{id_item}", status_code=204)
def delete_item(id_pedido: str, id_item: int, db: Session = Depends(get_db)):
    item = db.get(ItemPedido, (id_pedido, id_item))
    if not item:
        raise HTTPException(status_code=404, detail="Item do pedido não encontrado")
    db.delete(item)
    db.commit()
