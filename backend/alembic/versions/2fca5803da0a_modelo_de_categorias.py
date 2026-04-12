"""Modelo de categorias

Revision ID: 2fca5803da0a
Revises: 001
Create Date: 2026-04-11 20:20:21.770097

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '2fca5803da0a'
down_revision: Union[str, None] = '001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "categoria_imagens",
        sa.Column("nome_categoria", sa.String(255), primary_key=True),
        sa.Column("url_imagem", sa.String(255), nullable=False),
        sa.PrimaryKeyConstraint("nome_categoria"),
        if_not_exists=True
    )

def downgrade() -> None:
    op.drop_table('categoria_imagens')

