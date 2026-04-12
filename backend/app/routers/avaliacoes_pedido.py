from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.avaliacao_pedido import AvaliacaoPedido
from app.schemas.avaliacao_pedido import AvaliacaoPedidoCreate, AvaliacaoPedidoResponse

router = APIRouter(prefix="/avaliacoes", tags=["Avaliacoes"])


# GET /avaliacoes/{id_avaliacao}
@router.get("/{id_avaliacao}", response_model=AvaliacaoPedidoResponse)
def get_avaliacao(id_avaliacao: str, db: Session = Depends(get_db)):
    avaliacao = db.get(AvaliacaoPedido, id_avaliacao)
    if not avaliacao:
        raise HTTPException(status_code=404, detail="Avaliação não encontrada")
    return avaliacao


# POST /avaliacoes
@router.post("/", response_model=AvaliacaoPedidoResponse, status_code=201)
def create_avaliacao(body: AvaliacaoPedidoCreate, db: Session = Depends(get_db)):
    avaliacao = AvaliacaoPedido(**body.model_dump())
    db.add(avaliacao)
    db.commit()
    db.refresh(avaliacao)
    return avaliacao
