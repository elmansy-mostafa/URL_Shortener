from sqlalchemy import Table, column, String, MetaData

metadata = MetaData()
urls = Table(
    "urls",
    metadata,
    column("key", String, primary_key=True, index=True),
    column("long_url", String, unique=True),
        )