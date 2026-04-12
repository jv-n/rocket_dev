from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class VendedorBase(BaseModel):
    nome_vendedor: str
    prefixo_cep: str = Field(..., max_length=10)
    cidade: str
    estado: str = Field(..., max_length=2)


class VendedorCreate(VendedorBase):
    pass

class VendedorUpdate(BaseModel):
    nome_vendedor: Optional[str] = None
    prefixo_cep: Optional[str] = Field(None, max_length=10)
    cidade: Optional[str] = None
    estado: Optional[str] = Field(None, max_length=2)

class VendedorResponse(VendedorBase):
    model_config = ConfigDict(from_attributes=True)

    id_vendedor: str
