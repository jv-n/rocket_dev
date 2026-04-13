from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.order_review import OrderReview
from app.schemas.order_review import OrderReviewCreate, OrderReviewUpdate, OrderReviewResponse

router = APIRouter(prefix="/order_reviews", tags=["OrderReviews"])


# GET /order_reviews/{review_id}
@router.get("/{review_id}", response_model=OrderReviewResponse)
def get_review(review_id: str, db: Session = Depends(get_db)):
    review = db.get(OrderReview, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Order review not found")
    return review


# GET /order_reviews?order_id=...
@router.get("/", response_model=list[OrderReviewResponse])
def list_reviews(order_id: str | None = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    reviews = db.query(OrderReview)
    if order_id:
        reviews = reviews.filter(OrderReview.order_id == order_id)
    return reviews.offset(skip).limit(limit).all()


# POST /order_reviews
@router.post("/", response_model=OrderReviewResponse, status_code=201)
def create_review(body: OrderReviewCreate, db: Session = Depends(get_db)):
    review = OrderReview(**body.model_dump())
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


# PATCH /order_reviews/{review_id}
@router.patch("/{review_id}", response_model=OrderReviewResponse)
def update_review(review_id: str, body: OrderReviewUpdate, db: Session = Depends(get_db)):
    review = db.get(OrderReview, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Order review not found")
    for key, value in body.model_dump(exclude_unset=True).items():
        setattr(review, key, value)
    db.commit()
    db.refresh(review)
    return review


# DELETE /order_reviews/{review_id}
@router.delete("/{review_id}", status_code=204)
def delete_review(review_id: str, db: Session = Depends(get_db)):
    review = db.get(OrderReview, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Order review not found")
    db.delete(review)
    db.commit()
