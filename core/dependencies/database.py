from sqlalchemy import MetaData, create_engine

from core.settings import settings

metadata = MetaData()

database = create_engine(settings.DB_URL)
metadata.create_all(database)