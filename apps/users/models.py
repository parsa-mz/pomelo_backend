from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float


from core.dependencies.database import metadata


User = Table(
    "users",
    metadata,
    Column("id", String, primary_key=True),
    Column("name", String),
    Column("credit", Float),
    Column("payable", Float)
)


