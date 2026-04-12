from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.produto import Produto
from app.schemas.produto import ProdutoCreate, ProdutoUpdate, ProdutoResponse

router = APIRouter(prefix="/produtos", tags=["Produtos"])

# GET /produtos/search/?query=...
@router.get("/search/", response_model=list[ProdutoResponse])
def search_produtos(query: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    produtos = db.query(Produto).filter(Produto.nome_produto.contains(query)).offset(skip).limit(limit).all()
    return produtos

# GET /produtos?categoria=...
@router.get("/", response_model=list[ProdutoResponse])
def list_produtos(categoria: str | None = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    produtos = db.query(Produto)
    if categoria:
        produtos = produtos.filter(Produto.categoria_produto == categoria)
    return produtos.offset(skip).limit(limit).all()

# GET /produtos/{id_produto}
@router.get("/{id_produto}", response_model=ProdutoResponse)
def get_produto(id_produto: str, db: Session = Depends(get_db)):
    produto = db.get(Produto, id_produto)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto

# POST /produtos
@router.post("/", response_model=ProdutoResponse, status_code=201)
def create_produto(body: ProdutoCreate, db: Session = Depends(get_db)):
    produto = Produto(**body.model_dump())
    db.add(produto)
    db.commit()
    db.refresh(produto)
    return produto

# PATCH /produtos/{id_produto}
@router.patch("/{id_produto}", response_model=ProdutoResponse)
def patch_produto(id_produto: str, body: ProdutoUpdate, db: Session = Depends(get_db)):
    produto = db.get(Produto, id_produto)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(produto, field, value)
    db.commit()
    db.refresh(produto)
    return produto

#DELETE /produtos/{id_produto}
@router.delete("/{id_produto}", status_code=204)
def delete_produto(id_produto: str, db: Session = Depends(get_db)):
    produto = db.get(Produto, id_produto)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    db.delete(produto)
    db.commit()