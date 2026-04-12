from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.pedido import Pedido
from app.schemas.pedido import PedidoCreate, PedidoResponse

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

@router.get("/{id_pedido}", response_model=PedidoResponse)
def get_pedido(id_pedido: str, db: Session = Depends(get_db)):
    pedido = db.get(Pedido, id_pedido)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return pedido

@router.get("/", response_model=list[PedidoResponse])
def list_pedidos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    pedidos = db.query(Pedido).offset(skip).limit(limit).all()
    return pedidos

@router.post("/", response_model=PedidoResponse, status_code=201)
def create_pedido(body: PedidoCreate, db: Session = Depends(get_db)):
    pedido = Pedido(**body.model_dump())
    db.add(pedido)
    db.commit()
    db.refresh(pedido)
    return pedido

@router.put("/{id_pedido}", response_model=PedidoResponse)
def update_pedido(id_pedido: str, body: PedidoCreate, db: Session = Depends(get_db)):
    pedido = db.get(Pedido, id_pedido)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    for field, value in body.model_dump().items():
        setattr(pedido, field, value)
    db.commit()
    db.refresh(pedido)
    return pedido

@router.delete("/{id_pedido}", status_code=204)
def delete_pedido(id_pedido: str, db: Session = Depends(get_db)):
    pedido = db.get(Pedido, id_pedido)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    db.delete(pedido)
    db.commit()
