# Import all models so that SQLAlchemy and Alembic register them
from app.models.customer import Customer
from app.models.product import Product
from app.models.seller import Seller
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.order_review import OrderReview
from app.models.image_category import ImageCategory

__all__ = [
    "Customer",
    "Product",
    "Seller",
    "Order",
    "OrderItem",
    "OrderReview",
    "ImageCategory",
]
