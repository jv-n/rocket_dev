from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.consumidor import Consumidor
from app.schemas.consumidor import ConsumidorCreate, ConsumidorUpdate, ConsumidorResponse

router = APIRouter(prefix="/consumidores", tags=["Consumidores"])

# GET /consumidores/{id_consumidor}
@router.get("/{id_consumidor}", response_model=ConsumidorResponse)
def get_consumidor(id_consumidor: str, db: Session = Depends(get_db)):
    consumidor = db.get(Consumidor, id_consumidor)
    if not consumidor:
        raise HTTPException(status_code=404, detail="Consumidor não encontrado")
    return consumidor

# GET /consumidores
@router.get("/", response_model=list[ConsumidorResponse])
def list_consumidores(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    consumidores = db.query(Consumidor).offset(skip).limit(limit).all()
    return consumidores

# POST /consumidores
@router.post("/", response_model=ConsumidorResponse, status_code=201)
def create_consumidor(body: ConsumidorCreate, db: Session = Depends(get_db)):
    consumidor = Consumidor(**body.model_dump())
    db.add(consumidor)
    db.commit()
    db.refresh(consumidor)
    return consumidor

# PATCH /consumidores/{id_consumidor}
@router.patch("/{id_consumidor}", response_model=ConsumidorResponse)
def patch_consumidor(id_consumidor: str, body: ConsumidorUpdate, db: Session = Depends(get_db)):
    consumidor = db.get(Consumidor, id_consumidor)
    if not consumidor:
        raise HTTPException(status_code=404, detail="Consumidor não encontrado")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(consumidor, field, value)
    db.commit()
    db.refresh(consumidor)
    return consumidor

# PUT /consumidores/{id_consumidor}
@router.put("/{id_consumidor}", response_model=ConsumidorResponse)
def update_consumidor(id_consumidor: str, body: ConsumidorCreate, db: Session = Depends(get_db)):
    consumidor = db.get(Consumidor, id_consumidor)
    if not consumidor:
        raise HTTPException(status_code=404, detail="Consumidor não encontrado")    
    for field, value in body.model_dump().items():
        setattr(consumidor, field, value)
    db.commit()
    db.refresh(consumidor)
    return consumidor

# DELETE /consumidores/{id_consumidor}
@router.delete("/{id_consumidor}", status_code=204)
def delete_consumidor(id_consumidor: str, db: Session = Depends(get_db)):
    consumidor = db.get(Consumidor, id_consumidor)
    if not consumidor:
        raise HTTPException(status_code=404, detail="Consumidor não encontrado")
    db.delete(consumidor)
    db.commit()