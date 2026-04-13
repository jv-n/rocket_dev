from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.seller import Seller
from app.schemas.seller import SellerCreate, SellerUpdate, SellerResponse

router = APIRouter(prefix="/sellers", tags=["Sellers"])


# GET /sellers/{seller_id}
@router.get("/{seller_id}", response_model=SellerResponse)
def get_seller(seller_id: str, db: Session = Depends(get_db)):
    seller = db.get(Seller, seller_id)
    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")
    return seller


# GET /sellers
@router.get("/", response_model=list[SellerResponse])
def list_sellers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    sellers = db.query(Seller).offset(skip).limit(limit).all()
    return sellers


# POST /sellers
@router.post("/", response_model=SellerResponse, status_code=201)
def create_seller(body: SellerCreate, db: Session = Depends(get_db)):
    seller = Seller(**body.model_dump())
    db.add(seller)
    db.commit()
    db.refresh(seller)
    return seller


# PATCH /sellers/{seller_id}
@router.patch("/{seller_id}", response_model=SellerResponse)
def patch_seller(seller_id: str, body: SellerUpdate, db: Session = Depends(get_db)):
    seller = db.get(Seller, seller_id)
    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(seller, field, value)
    db.commit()
    db.refresh(seller)
    return seller


# PUT /sellers/{seller_id}
@router.put("/{seller_id}", response_model=SellerResponse)
def update_seller(seller_id: str, body: SellerCreate, db: Session = Depends(get_db)):
    seller = db.get(Seller, seller_id)
    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")
    for field, value in body.model_dump().items():
        setattr(seller, field, value)
    db.commit()
    db.refresh(seller)
    return seller


# DELETE /sellers/{seller_id}
@router.delete("/{seller_id}", status_code=204)
def delete_seller(seller_id: str, db: Session = Depends(get_db)):
    seller = db.get(Seller, seller_id)
    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")
    db.delete(seller)
    db.commit()
