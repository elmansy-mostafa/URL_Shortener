from sqlalchemy import create_engine, MetaData, Table, Column, String, MetaData
from databases import Database

DATABASE_URL = "sqlite:///./test.db"
database = Database(DATABASE_URL)
metadata = MetaData()

urls = Table(
    "urls",
    metadata,
    Column("key", String, primary_key=True),
    Column("long_url", String, unique=True),
        )

engine = create_engine(DATABASE_URL)
metadata.create_all(engine)

