from tokenize import String

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.image_category import ImageCategory
from app.schemas.image_category import ImageCategoryResponse

router = APIRouter(prefix="/image_categories", tags=["ImageCategories"])


# GET /image_categories/
@router.get("/", response_model=list[ImageCategoryResponse])
def list_image_categories(db: Session = Depends(get_db)):
    return db.query(ImageCategory).all()

#GET /image_categories/{category}
@router.get("/{category}", response_model=ImageCategoryResponse)
def get_image_category(category: str, db: Session = Depends(get_db)):
    return db.get(ImageCategory, category)
