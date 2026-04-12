from pydantic import BaseModel, ConfigDict, Field

class CategoriaImagemBase(BaseModel):
    nome_categoria: str
    url_imagem: str

class CategoriaImagemCreate(CategoriaImagemBase):
    pass

class CategoriaImagemResponse(CategoriaImagemBase):
    model_config = ConfigDict(from_attributes=True)