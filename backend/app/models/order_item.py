from sqlalchemy import String, Float, Integer, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class OrderItem(Base):
    __tablename__ = "order_items"

    order_id: Mapped[str] = mapped_column(
        String(32), ForeignKey("orders.order_id"), nullable=False
    )
    item_id: Mapped[int] = mapped_column(Integer, nullable=False)
    product_id: Mapped[str] = mapped_column(
        String(32), ForeignKey("products.product_id"), nullable=False
    )
    seller_id: Mapped[str] = mapped_column(
        String(32), ForeignKey("sellers.seller_id"), nullable=False
    )
    price_brl: Mapped[float] = mapped_column(Float)
    freight_price: Mapped[float] = mapped_column(Float)

    __table_args__ = (
        PrimaryKeyConstraint("order_id", "item_id"),
    )
