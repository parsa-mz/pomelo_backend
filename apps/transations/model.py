from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float

from core.settings import settings

# from core.dependencies.database import metadata

metadata = MetaData()

Transaction = Table(
    "transactions",
    metadata,
    Column("txn_id", String, primary_key=True),
    Column("event_type", String),
    Column("event_time", Integer),
    Column("amount", Float),
)

PendingTransaction = Table(
    "pending_transactions",
    metadata,
    Column("id", String, primary_key=True),
    Column("amount", Float),
    Column("time", Integer),
    Column("user_id", String),
)

SettledTransaction = Table(
    "settled_transactions",
    metadata,
    Column("id", String, primary_key=True),
    Column("amount", Float),
    Column("initial_time", Integer),
    Column("final_time", Integer),
    Column("user_id", String),
)

database = create_engine(settings.DB_URL)
metadata.create_all(database)
