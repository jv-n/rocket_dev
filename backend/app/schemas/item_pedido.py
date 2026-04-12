from pydantic import BaseModel, ConfigDict, Field


class ItemPedidoBase(BaseModel):
    id_pedido: str
    id_produto: str
    id_vendedor: str
    preco_BRL: float = Field(gt=0)
    preco_frete: float = Field(ge=0)


class ItemPedidoCreate(ItemPedidoBase):
    pass


class ItemPedidoResponse(ItemPedidoBase):
    model_config = ConfigDict(from_attributes=True)

    id_item: int
