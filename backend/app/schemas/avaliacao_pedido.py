from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class AvaliacaoPedidoBase(BaseModel):
    id_pedido: str
    avaliacao: int = Field(ge=1, le=5)
    titulo_comentario: Optional[str] = None
    comentario: Optional[str] = None


class AvaliacaoPedidoCreate(AvaliacaoPedidoBase):
    pass


class AvaliacaoPedidoResponse(AvaliacaoPedidoBase):
    model_config = ConfigDict(from_attributes=True)

    id_avaliacao: str
    data_comentario: Optional[datetime] = None
    data_resposta: Optional[datetime] = None