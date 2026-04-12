from pydantic import BaseModel, ConfigDict, Field

from typing import Optional

class ConsumidorBase(BaseModel):
    nome_consumidor: str
    prefixo_cep: str = Field(..., max_length=10)
    cidade: str
    estado: str = Field(..., max_length=2)

class ConsumidorCreate(ConsumidorBase):
    pass

class ConsumidorResponse(ConsumidorBase):
    id_consumidor: str
    model_config = ConfigDict(from_attributes=True)
