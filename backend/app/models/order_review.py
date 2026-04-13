from datetime import datetime
from typing import Optional

from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class OrderReview(Base):
    __tablename__ = "order_reviews"

    review_id: Mapped[str] = mapped_column(String(32), primary_key=True)
    order_id: Mapped[str] = mapped_column(
        String(32), ForeignKey("orders.order_id"), nullable=False
    )
    rating: Mapped[int] = mapped_column(Integer)
    comment_title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    comment: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    comment_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    response_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
