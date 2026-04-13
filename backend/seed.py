import csv
import uuid
from app.database import SessionLocal, engine, Base
from app.models import (
    Product,
    Seller,
    Customer,
    Order,
    OrderItem,
    OrderReview,
    ImageCategory,
)
from sqlalchemy import text
from datetime import datetime, date

Base.metadata.create_all(bind=engine)

FLOAT_COLS_PRODUCT = {"weight_grams", "length_cm", "height_cm", "width_cm"}
FLOAT_COLS_ORDER = {"delivery_days", "estimated_delivery_days", "delivery_days_diff"}
FLOAT_COLS_ORDER_ITEM = {"price_brl", "freight_price"}
DATETIME_COLS_ORDER = {"purchase_timestamp", "delivered_timestamp"}
DATE_COLS_ORDER = {"estimated_delivery_date"}
DATETIME_COLS_REVIEW = {"comment_date", "response_date"}
NULLABLE_STR_COLS_REVIEW = {"comment_title", "comment"}


def parse_datetime(v: str) -> datetime | None:
    if not v:
        return None
    try:
        return datetime.strptime(v, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None


def parse_date(v: str) -> date | None:
    if not v:
        return None
    try:
        return datetime.strptime(v, "%Y-%m-%d").date()
    except ValueError:
        return None


def clean_row(row: dict, float_cols: set = set(), datetime_cols: set = set(),
              date_cols: set = set(), nullable_str_cols: set = set()) -> dict:
    result = {}
    for k, v in row.items():
        if k in float_cols:
            result[k] = None if v == "" else float(v)
        elif k in datetime_cols:
            result[k] = parse_datetime(v)
        elif k in date_cols:
            result[k] = parse_date(v)
        elif k in nullable_str_cols:
            result[k] = None if v == "" else v
        else:
            result[k] = v
    return result


# Column name mappings from CSV (portuguese) to model fields (english)
SELLER_MAP = {
    "id_vendedor": "seller_id",
    "nome_vendedor": "name",
    "prefixo_cep": "zip_prefix",
    "cidade": "city",
    "estado": "state",
}

CUSTOMER_MAP = {
    "id_consumidor": "customer_id",
    "prefixo_cep": "zip_prefix",
    "nome_consumidor": "name",
    "cidade": "city",
    "estado": "state",
}

PRODUCT_MAP = {
    "id_produto": "product_id",
    "nome_produto": "name",
    "categoria_produto": "category",
    "peso_produto_gramas": "weight_grams",
    "comprimento_centimetros": "length_cm",
    "altura_centimetros": "height_cm",
    "largura_centimetros": "width_cm",
}

ORDER_MAP = {
    "id_pedido": "order_id",
    "id_consumidor": "customer_id",
    "status": "status",
    "pedido_compra_timestamp": "purchase_timestamp",
    "pedido_entregue_timestamp": "delivered_timestamp",
    "data_estimada_entrega": "estimated_delivery_date",
    "tempo_entrega_dias": "delivery_days",
    "tempo_entrega_estimado_dias": "estimated_delivery_days",
    "diferenca_entrega_dias": "delivery_days_diff",
    "entrega_no_prazo": "on_time_delivery",
}

ORDER_ITEM_MAP = {
    "id_pedido": "order_id",
    "id_item": "item_id",
    "id_produto": "product_id",
    "id_vendedor": "seller_id",
    "preco_BRL": "price_brl",
    "preco_frete": "freight_price",
}

ORDER_REVIEW_MAP = {
    "id_avaliacao": "review_id",
    "id_pedido": "order_id",
    "avaliacao": "rating",
    "titulo_comentario": "comment_title",
    "comentario": "comment",
    "data_comentario": "comment_date",
    "data_resposta": "response_date",
}

IMAGE_CATEGORY_MAP = {
    "nome_categoria": "category_name",
    "url_imagem": "image_url",
}


def remap(row: dict, mapping: dict) -> dict:
    return {mapping[k]: v for k, v in row.items() if k in mapping}


db = SessionLocal()

with db:
    db.execute(text("DELETE FROM order_reviews"))
    db.execute(text("DELETE FROM order_items"))
    db.execute(text("DELETE FROM orders"))
    db.execute(text("DELETE FROM customers"))
    db.execute(text("DELETE FROM sellers"))
    db.execute(text("DELETE FROM products"))
    db.execute(text("DELETE FROM image_categories"))
    db.commit()
    print("Cleared all tables")

# Seed Sellers
with open("data/dim_vendedores.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    sellers = [Seller(**remap(row, SELLER_MAP)) for row in reader]
    db.add_all(sellers)
    db.commit()
    print(f"Inserted {len(sellers)} sellers")

# Seed Customers
with open("data/dim_consumidores.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    customers = [Customer(**remap(row, CUSTOMER_MAP)) for row in reader]
    db.add_all(customers)
    db.commit()
    print(f"Inserted {len(customers)} customers")

# Seed Products
with open("data/dim_produtos.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    products = [Product(**clean_row(remap(row, PRODUCT_MAP), FLOAT_COLS_PRODUCT)) for row in reader]
    db.add_all(products)
    db.commit()
    print(f"Inserted {len(products)} products")

# Seed Orders
with open("data/fat_pedidos.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    orders = [
        Order(**clean_row(remap(row, ORDER_MAP), float_cols=FLOAT_COLS_ORDER,
                          datetime_cols=DATETIME_COLS_ORDER,
                          date_cols=DATE_COLS_ORDER))
        for row in reader
    ]
    db.add_all(orders)
    db.commit()
    print(f"Inserted {len(orders)} orders")

# Seed Order Items
with open("data/fat_itens_pedidos.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    order_items = [OrderItem(**clean_row(remap(row, ORDER_ITEM_MAP), float_cols=FLOAT_COLS_ORDER_ITEM)) for row in reader]
    db.add_all(order_items)
    db.commit()
    print(f"Inserted {len(order_items)} order items")

# Seed Order reviews
with open("data/fat_avaliacoes_pedidos.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    seen_ids = set()
    reviews = []
    for row in reader:
        mapped = remap(row, ORDER_REVIEW_MAP)
        if mapped["review_id"] in seen_ids:
            mapped["review_id"] = uuid.uuid4().hex
        seen_ids.add(mapped["review_id"])
        reviews.append(
            OrderReview(**clean_row(mapped, datetime_cols=DATETIME_COLS_REVIEW,
                                    nullable_str_cols=NULLABLE_STR_COLS_REVIEW))
        )
    db.add_all(reviews)
    db.commit()
    print(f"Inserted {len(reviews)} order reviews")

# Seed Image Categories
with open("data/dim_categoria_imagens.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    image_categories = [ImageCategory(**remap(row, IMAGE_CATEGORY_MAP)) for row in reader]
    db.add_all(image_categories)
    db.commit()
    print(f"Inserted {len(image_categories)} image categories")
