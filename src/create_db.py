import os
from sqlalchemy import create_engine, text

pw = os.getenv("PG_PASSWORD", "postgres")
engine = create_engine(f"postgresql+pg8000://postgres:{pw}@localhost:5432/postgres",
                       isolation_level="AUTOCOMMIT")
with engine.connect() as c:
    c.execute(text("CREATE DATABASE sales_dw"))
    print("Base sales_dw créée")