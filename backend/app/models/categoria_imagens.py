from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

class CategoriaImagem(Base):
    __tablename__ = "categoria_imagens"

    nome_categoria: Mapped[str] = mapped_column(String(255), primary_key=True)
    url_imagem: Mapped[str] = mapped_column(String(255))