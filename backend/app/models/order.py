from datetime import datetime, date
from typing import Optional

from sqlalchemy import String, Float, DateTime, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Order(Base):
    __tablename__ = "orders"

    order_id: Mapped[str] = mapped_column(String(32), primary_key=True)
    customer_id: Mapped[str] = mapped_column(
        String(32), ForeignKey("customers.customer_id"), nullable=False
    )
    status: Mapped[str] = mapped_column(String(50))
    purchase_timestamp: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    delivered_timestamp: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    estimated_delivery_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    delivery_days: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    estimated_delivery_days: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    delivery_days_diff: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    on_time_delivery: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
