from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class ImageCategory(Base):
    __tablename__ = "image_categories"

    category_name: Mapped[str] = mapped_column(String(255), primary_key=True)
    image_url: Mapped[str] = mapped_column(String(255))
