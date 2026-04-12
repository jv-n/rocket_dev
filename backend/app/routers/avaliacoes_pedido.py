from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.avaliacao_pedido import AvaliacaoPedido
from app.schemas.avaliacao_pedido import AvaliacaoPedidoCreate, AvaliacaoPedidoUpdate, AvaliacaoPedidoResponse

router = APIRouter(prefix="/avaliacoes", tags=["Avaliacoes"])

# GET /avaliacoes/{id_avaliacao}
@router.get("/{id_avaliacao}", response_model=AvaliacaoPedidoResponse)
def get_avaliacao(id_avaliacao: str, db: Session = Depends(get_db)):
    avaliacao = db.get(AvaliacaoPedido, id_avaliacao)
    if not avaliacao:
        raise HTTPException(status_code=404, detail="Avaliação não encontrada")
    return avaliacao

# GET /avaliacoes?pedido_id=...
@router.get("/", response_model=list[AvaliacaoPedidoResponse])
def list_avaliacoes(pedido_id: str | None = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    avaliacoes = db.query(AvaliacaoPedido)
    if pedido_id:
        avaliacoes = avaliacoes.filter(AvaliacaoPedido.id_pedido == pedido_id)
    return avaliacoes.offset(skip).limit(limit).all()



# POST /avaliacoes
@router.post("/", response_model=AvaliacaoPedidoResponse, status_code=201)
def create_avaliacao(body: AvaliacaoPedidoCreate, db: Session = Depends(get_db)):
    avaliacao = AvaliacaoPedido(**body.model_dump())
    db.add(avaliacao)
    db.commit()
    db.refresh(avaliacao)
    return avaliacao

# PATCH /avaliacoes/{id_avaliacao}
@router.patch("/{id_avaliacao}", response_model=AvaliacaoPedidoResponse)
def update_avaliacao(id_avaliacao: str, body: AvaliacaoPedidoUpdate, db: Session = Depends(get_db)):
    avaliacao = db.get(AvaliacaoPedido, id_avaliacao)
    if not avaliacao:
        raise HTTPException(status_code=404, detail="Avaliação não encontrada")
    for key, value in body.model_dump(exclude_unset=True).items():
        setattr(avaliacao, key, value)
    db.commit()
    db.refresh(avaliacao)
    return avaliacao

# DELETE /avaliacoes/{id_avaliacao}
@router.delete("/{id_avaliacao}", status_code=204)
def delete_avaliacao(id_avaliacao: str, db: Session = Depends(get_db)):
    avaliacao = db.get(AvaliacaoPedido, id_avaliacao)
    if not avaliacao:
        raise HTTPException(status_code=404, detail="Avaliação não encontrada")
    db.delete(avaliacao)
    db.commit()

