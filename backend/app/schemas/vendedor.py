from pydantic import BaseModel, ConfigDict, Field


class VendedorBase(BaseModel):
    nome_vendedor: str
    prefixo_cep: str = Field(..., max_length=10)
    cidade: str
    estado: str = Field(..., max_length=2)


class VendedorCreate(VendedorBase):
    pass


class VendedorResponse(VendedorBase):
    model_config = ConfigDict(from_attributes=True)

    id_vendedor: str
