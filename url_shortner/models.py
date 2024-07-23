from sqlalchemy import Table, Column, String, MetaData

metadata = MetaData()
urls = Table(
    "urls",
    metadata,
    Column("key", String, primary_key=True),
    Column("long_url", String, unique=True),
        )