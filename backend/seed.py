import csv
import uuid
from app.database import SessionLocal, engine, Base
from app.models import (
    Produto,
    Vendedor,
    Consumidor,
    Pedido,
    ItemPedido,
    AvaliacaoPedido,
    CategoriaImagem,
)
from sqlalchemy import text
from datetime import datetime, date

Base.metadata.create_all(bind=engine)

FLOAT_COLS_PROD = {"peso_produto_gramas", "comprimento_centimetros", "altura_centimetros", "largura_centimetros"}
FLOAT_COLS_PEDIDO = {"tempo_entrega_dias", "tempo_entrega_estimado_dias", "diferenca_entrega_dias"}
FLOAT_COLS_ITEM = {"preco_BRL", "preco_frete"}
DATETIME_COLS_PEDIDO = {"pedido_compra_timestamp", "pedido_entregue_timestamp"}
DATE_COLS_PEDIDO = {"data_estimada_entrega"}
DATETIME_COLS_AVALIACAO = {"data_comentario", "data_resposta"}
NULLABLE_STR_COLS_AVALIACAO = {"titulo_comentario", "comentario"}

def clean_row(row: dict, float_cols: set) -> dict:
    """Convert empty strings to None for float columns."""
    return {
        k: (None if k in float_cols and v == "" else v)
        for k, v in row.items()
    }

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

db = SessionLocal()

with db:
    db.execute(text("DELETE FROM avaliacoes_pedidos"))
    db.execute(text("DELETE FROM itens_pedidos"))
    db.execute(text("DELETE FROM pedidos"))
    db.execute(text("DELETE FROM consumidores"))
    db.execute(text("DELETE FROM vendedores"))
    db.execute(text("DELETE FROM produtos"))
    db.execute(text("DELETE FROM categoria_imagens"))
    db.commit()
    print("Cleared all tables")

# Seed Vendedores
with open("data/dim_vendedores.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    vendedores = [Vendedor(**row) for row in reader]
    db.add_all(vendedores)
    db.commit()
    print(f"Inserted {len(vendedores)} vendedores")

# Seed Consumidores
with open("data/dim_consumidores.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    consumidores = [Consumidor(**row) for row in reader]
    db.add_all(consumidores)
    db.commit()
    print(f"Inserted {len(consumidores)} consumidores")

# Seed Produtos
with open("data/dim_produtos.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    produtos = [Produto(**clean_row(row, FLOAT_COLS_PROD)) for row in reader]
    db.add_all(produtos)
    db.commit()
    print(f"Inserted {len(produtos)} produtos")

# Seed Pedidos
with open("data/fat_pedidos.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    pedidos = [
        Pedido(**clean_row(row, float_cols=FLOAT_COLS_PEDIDO,
                           datetime_cols=DATETIME_COLS_PEDIDO,
                           date_cols=DATE_COLS_PEDIDO))
        for row in reader
    ]
    db.add_all(pedidos)
    db.commit()
    print(f"Inserted {len(pedidos)} pedidos")

# Seed Itens de Pedido
with open("data/fat_itens_pedidos.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    itens = [ItemPedido(**clean_row(row, float_cols=FLOAT_COLS_ITEM)) for row in reader]
    db.add_all(itens)
    db.commit()
    print(f"Inserted {len(itens)} itens de pedido")

# Seed Avaliações
with open("data/fat_avaliacoes_pedidos.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    seen_ids = set()
    avaliacoes = []
    for row in reader:
        if row["id_avaliacao"] in seen_ids:
            row["id_avaliacao"] = uuid.uuid4().hex 
        seen_ids.add(row["id_avaliacao"])
        avaliacoes.append(
            AvaliacaoPedido(**clean_row(row, datetime_cols=DATETIME_COLS_AVALIACAO,
                                       nullable_str_cols=NULLABLE_STR_COLS_AVALIACAO))
        )
    db.add_all(avaliacoes)
    db.commit()
    print(f"Inserted {len(avaliacoes)} avaliações")

#Seed Categoria Imagens
with open("data/dim_categoria_imagens.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    categorias = [CategoriaImagem(**row) for row in reader]
    db.add_all(categorias)
    db.commit()
    print(f"Inserted {len(categorias)} categorias de imagens")
