from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


class CustomerBase(BaseModel):
    name: str
    zip_prefix: str = Field(..., max_length=10)
    city: str
    state: str = Field(..., max_length=2)


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    zip_prefix: Optional[str] = Field(None, max_length=10)
    city: Optional[str] = None
    state: Optional[str] = Field(None, max_length=2)


class CustomerResponse(CustomerBase):
    model_config = ConfigDict(from_attributes=True)

    customer_id: str
