from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


class OrderItemBase(BaseModel):
    order_id: str
    product_id: str
    seller_id: str
    price_brl: float = Field(gt=0)
    freight_price: float = Field(ge=0)


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemUpdate(BaseModel):
    price_brl: Optional[float] = Field(None, gt=0)
    freight_price: Optional[float] = Field(None, ge=0)


class OrderItemResponse(OrderItemBase):
    model_config = ConfigDict(from_attributes=True)

    item_id: int
