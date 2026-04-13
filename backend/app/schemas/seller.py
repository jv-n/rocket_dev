from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


class SellerBase(BaseModel):
    name: str
    zip_prefix: str = Field(..., max_length=10)
    city: str
    state: str = Field(..., max_length=2)


class SellerCreate(SellerBase):
    pass


class SellerUpdate(BaseModel):
    name: Optional[str] = None
    zip_prefix: Optional[str] = Field(None, max_length=10)
    city: Optional[str] = None
    state: Optional[str] = Field(None, max_length=2)


class SellerResponse(SellerBase):
    model_config = ConfigDict(from_attributes=True)

    seller_id: str
