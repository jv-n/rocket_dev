from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.vendedor import Vendedor
from app.schemas.vendedor import VendedorCreate, VendedorUpdate, VendedorResponse

router = APIRouter(prefix="/vendedores", tags=["Vendedores"])

# GET /vendedores/{id_vendedor}
@router.get("/{id_vendedor}", response_model=VendedorResponse)
def get_vendedor(id_vendedor: str, db: Session = Depends(get_db)):
    vendedor = db.get(Vendedor, id_vendedor)
    if not vendedor:
        raise HTTPException(status_code=404, detail="Vendedor não encontrado")
    return vendedor

# GET /vendedores
@router.get("/", response_model=list[VendedorResponse])
def list_vendedores(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    vendedores = db.query(Vendedor).offset(skip).limit(limit).all()
    return vendedores

# POST /vendedores
@router.post("/", response_model=VendedorResponse, status_code=201)
def create_vendedor(body: VendedorCreate, db: Session = Depends(get_db)):
    vendedor = Vendedor(**body.model_dump())
    db.add(vendedor)
    db.commit()
    db.refresh(vendedor)
    return vendedor

# PATCH /vendedores/{id_vendedor}
@router.patch("/{id_vendedor}", response_model=VendedorResponse)
def patch_vendedor(id_vendedor: str, body: VendedorUpdate, db: Session = Depends(get_db)):
    vendedor = db.get(Vendedor, id_vendedor)
    if not vendedor:
        raise HTTPException(status_code=404, detail="Vendedor não encontrado")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(vendedor, field, value)
    db.commit()
    db.refresh(vendedor)
    return vendedor

# PUT /vendedores/{id_vendedor}
@router.put("/{id_vendedor}", response_model=VendedorResponse)
def update_vendedor(id_vendedor: str, body: VendedorCreate, db: Session = Depends(get_db)):
    vendedor = db.get(Vendedor, id_vendedor)
    if not vendedor:
        raise HTTPException(status_code=404, detail="Vendedor não encontrado")    
    for field, value in body.model_dump().items():
        setattr(vendedor, field, value)
    db.commit()
    db.refresh(vendedor)
    return vendedor

# DELETE /vendedores/{id_vendedor}
@router.delete("/{id_vendedor}", status_code=204)
def delete_vendedor(id_vendedor: str, db: Session = Depends(get_db)):    
    vendedor = db.get(Vendedor, id_vendedor)
    if not vendedor:
        raise HTTPException(status_code=404, detail="Vendedor não encontrado")
    db.delete(vendedor)
    db.commit()