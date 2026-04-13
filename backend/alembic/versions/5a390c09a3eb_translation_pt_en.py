"""Translate schema to English — drop Portuguese tables and create English equivalents

Revision ID: 003
Revises: 2fca5803da0a
Create Date: 2026-04-13

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "003"
down_revision: Union[str, None] = "2fca5803da0a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop old Portuguese-named tables (order matters due to FK constraints)
    op.execute("DELETE FROM avaliacoes_pedidos")
    op.execute("DELETE FROM itens_pedidos")
    op.execute("DELETE FROM pedidos")
    op.execute("DELETE FROM consumidores")
    op.execute("DELETE FROM vendedores")
    op.execute("DELETE FROM produtos")
    op.execute("DELETE FROM categoria_imagens")

    op.drop_table("avaliacoes_pedidos")
    op.drop_table("itens_pedidos")
    op.drop_table("pedidos")
    op.drop_table("consumidores")
    op.drop_table("vendedores")
    op.drop_table("produtos")
    op.drop_table("categoria_imagens")

    # Create new English-named tables
    op.create_table(
        "customers",
        sa.Column("customer_id", sa.String(32), primary_key=True),
        sa.Column("zip_prefix", sa.String(10), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("city", sa.String(100), nullable=False),
        sa.Column("state", sa.String(2), nullable=False),
    )

    op.create_table(
        "products",
        sa.Column("product_id", sa.String(32), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("category", sa.String(100), nullable=False),
        sa.Column("weight_grams", sa.Float(), nullable=True),
        sa.Column("length_cm", sa.Float(), nullable=True),
        sa.Column("height_cm", sa.Float(), nullable=True),
        sa.Column("width_cm", sa.Float(), nullable=True),
    )

    op.create_table(
        "sellers",
        sa.Column("seller_id", sa.String(32), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("zip_prefix", sa.String(10), nullable=False),
        sa.Column("city", sa.String(100), nullable=False),
        sa.Column("state", sa.String(2), nullable=False),
    )

    op.create_table(
        "orders",
        sa.Column("order_id", sa.String(32), primary_key=True),
        sa.Column("customer_id", sa.String(32), sa.ForeignKey("customers.customer_id"), nullable=False),
        sa.Column("status", sa.String(50), nullable=False),
        sa.Column("purchase_timestamp", sa.DateTime(), nullable=True),
        sa.Column("delivered_timestamp", sa.DateTime(), nullable=True),
        sa.Column("estimated_delivery_date", sa.Date(), nullable=True),
        sa.Column("delivery_days", sa.Float(), nullable=True),
        sa.Column("estimated_delivery_days", sa.Float(), nullable=True),
        sa.Column("delivery_days_diff", sa.Float(), nullable=True),
        sa.Column("on_time_delivery", sa.String(10), nullable=True),
    )

    op.create_table(
        "order_items",
        sa.Column("order_id", sa.String(32), sa.ForeignKey("orders.order_id"), nullable=False),
        sa.Column("item_id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.String(32), sa.ForeignKey("products.product_id"), nullable=False),
        sa.Column("seller_id", sa.String(32), sa.ForeignKey("sellers.seller_id"), nullable=False),
        sa.Column("price_brl", sa.Float(), nullable=False),
        sa.Column("freight_price", sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint("order_id", "item_id"),
    )

    op.create_table(
        "order_reviews",
        sa.Column("review_id", sa.String(32), primary_key=True),
        sa.Column("order_id", sa.String(32), sa.ForeignKey("orders.order_id"), nullable=False),
        sa.Column("rating", sa.Integer(), nullable=False),
        sa.Column("comment_title", sa.String(255), nullable=True),
        sa.Column("comment", sa.String(1000), nullable=True),
        sa.Column("comment_date", sa.DateTime(), nullable=True),
        sa.Column("response_date", sa.DateTime(), nullable=True),
    )

    op.create_table(
        "image_categories",
        sa.Column("category_name", sa.String(255), primary_key=True),
        sa.Column("image_url", sa.String(255), nullable=False),
    )


def downgrade() -> None:
    # Drop English-named tables (order matters due to FK constraints)
    op.drop_table("order_reviews")
    op.drop_table("order_items")
    op.drop_table("orders")
    op.drop_table("sellers")
    op.drop_table("products")
    op.drop_table("customers")
    op.drop_table("image_categories")

    # Recreate Portuguese-named tables
    op.create_table(
        "consumidores",
        sa.Column("id_consumidor", sa.String(32), primary_key=True),
        sa.Column("prefixo_cep", sa.String(10), nullable=False),
        sa.Column("nome_consumidor", sa.String(255), nullable=False),
        sa.Column("cidade", sa.String(100), nullable=False),
        sa.Column("estado", sa.String(2), nullable=False),
    )

    op.create_table(
        "produtos",
        sa.Column("id_produto", sa.String(32), primary_key=True),
        sa.Column("nome_produto", sa.String(255), nullable=False),
        sa.Column("categoria_produto", sa.String(100), nullable=False),
        sa.Column("peso_produto_gramas", sa.Float(), nullable=True),
        sa.Column("comprimento_centimetros", sa.Float(), nullable=True),
        sa.Column("altura_centimetros", sa.Float(), nullable=True),
        sa.Column("largura_centimetros", sa.Float(), nullable=True),
    )

    op.create_table(
        "vendedores",
        sa.Column("id_vendedor", sa.String(32), primary_key=True),
        sa.Column("nome_vendedor", sa.String(255), nullable=False),
        sa.Column("prefixo_cep", sa.String(10), nullable=False),
        sa.Column("cidade", sa.String(100), nullable=False),
        sa.Column("estado", sa.String(2), nullable=False),
    )

    op.create_table(
        "pedidos",
        sa.Column("id_pedido", sa.String(32), primary_key=True),
        sa.Column("id_consumidor", sa.String(32), sa.ForeignKey("consumidores.id_consumidor"), nullable=False),
        sa.Column("status", sa.String(50), nullable=False),
        sa.Column("pedido_compra_timestamp", sa.DateTime(), nullable=True),
        sa.Column("pedido_entregue_timestamp", sa.DateTime(), nullable=True),
        sa.Column("data_estimada_entrega", sa.Date(), nullable=True),
        sa.Column("tempo_entrega_dias", sa.Float(), nullable=True),
        sa.Column("tempo_entrega_estimado_dias", sa.Float(), nullable=True),
        sa.Column("diferenca_entrega_dias", sa.Float(), nullable=True),
        sa.Column("entrega_no_prazo", sa.String(10), nullable=True),
    )

    op.create_table(
        "itens_pedidos",
        sa.Column("id_pedido", sa.String(32), sa.ForeignKey("pedidos.id_pedido"), nullable=False),
        sa.Column("id_item", sa.Integer(), nullable=False),
        sa.Column("id_produto", sa.String(32), sa.ForeignKey("produtos.id_produto"), nullable=False),
        sa.Column("id_vendedor", sa.String(32), sa.ForeignKey("vendedores.id_vendedor"), nullable=False),
        sa.Column("preco_BRL", sa.Float(), nullable=False),
        sa.Column("preco_frete", sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint("id_pedido", "id_item"),
    )

    op.create_table(
        "avaliacoes_pedidos",
        sa.Column("id_avaliacao", sa.String(32), primary_key=True),
        sa.Column("id_pedido", sa.String(32), sa.ForeignKey("pedidos.id_pedido"), nullable=False),
        sa.Column("avaliacao", sa.Integer(), nullable=False),
        sa.Column("titulo_comentario", sa.String(255), nullable=True),
        sa.Column("comentario", sa.String(1000), nullable=True),
        sa.Column("data_comentario", sa.DateTime(), nullable=True),
        sa.Column("data_resposta", sa.DateTime(), nullable=True),
    )

    op.create_table(
        "categoria_imagens",
        sa.Column("nome_categoria", sa.String(255), primary_key=True),
        sa.Column("url_imagem", sa.String(255), nullable=False),
    )
