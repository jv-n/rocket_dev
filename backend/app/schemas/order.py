from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel, ConfigDict


class OrderBase(BaseModel):
    customer_id: str
    status: str
    purchase_timestamp: Optional[datetime] = None
    delivered_timestamp: Optional[datetime] = None
    estimated_delivery_date: Optional[date] = None
    delivery_days: Optional[float] = None
    estimated_delivery_days: Optional[float] = None
    delivery_days_diff: Optional[float] = None
    on_time_delivery: Optional[str] = None


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    status: Optional[str] = None
    purchase_timestamp: Optional[datetime] = None
    delivered_timestamp: Optional[datetime] = None
    estimated_delivery_date: Optional[date] = None
    delivery_days: Optional[float] = None
    estimated_delivery_days: Optional[float] = None
    delivery_days_diff: Optional[float] = None
    on_time_delivery: Optional[str] = None


class OrderResponse(OrderBase):
    model_config = ConfigDict(from_attributes=True)

    order_id: str
