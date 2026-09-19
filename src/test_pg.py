import os
from sqlalchemy import create_engine, text

pw = os.getenv("PG_PASSWORD", "postgres")
engine = create_engine(f"postgresql+pg8000://postgres:{pw}@localhost:5432/sales_dw")
try:
    with engine.connect() as c:
        print("Connexion OK :", c.execute(text("SELECT version()")).scalar())
except Exception as e:
    print("ERREUR :", repr(e))