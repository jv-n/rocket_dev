from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class ItemPedidoBase(BaseModel):
    id_pedido: str
    id_produto: str
    id_vendedor: str
    preco_BRL: float = Field(gt=0)
    preco_frete: float = Field(ge=0)


class ItemPedidoCreate(ItemPedidoBase):
    pass

class ItemPedidoUpdate(BaseModel):
    preco_BRL: Optional[float] = Field(None, gt=0)
    preco_frete: Optional[float] = Field(None, ge=0)

class ItemPedidoResponse(ItemPedidoBase):
    model_config = ConfigDict(from_attributes=True)

    id_item: int
