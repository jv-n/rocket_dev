from typing import Optional

from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    name: str
    category: str
    weight_grams: Optional[float] = None
    length_cm: Optional[float] = None
    height_cm: Optional[float] = None
    width_cm: Optional[float] = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    weight_grams: Optional[float] = None
    length_cm: Optional[float] = None
    height_cm: Optional[float] = None
    width_cm: Optional[float] = None


class ProductResponse(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    product_id: str


class BestSellingProductResponse(ProductResponse):
    orders_count: int
    total_revenue: float


class ProductSalesResponse(BaseModel):
    product_id: str
    orders_count: int
    total_revenue: float
    total_freight: float
