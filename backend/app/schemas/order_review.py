from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class OrderReviewBase(BaseModel):
    order_id: str
    rating: int = Field(ge=1, le=5)
    comment_title: Optional[str] = None
    comment: Optional[str] = None


class OrderReviewCreate(OrderReviewBase):
    pass


class OrderReviewUpdate(BaseModel):
    rating: Optional[int] = Field(None, ge=1, le=5)
    comment_title: Optional[str] = None
    comment: Optional[str] = None


class OrderReviewResponse(OrderReviewBase):
    model_config = ConfigDict(from_attributes=True)

    review_id: str
    comment_date: Optional[datetime] = None
    response_date: Optional[datetime] = None
