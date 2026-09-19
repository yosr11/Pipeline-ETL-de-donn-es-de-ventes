import os
from sqlalchemy import create_engine
from spark_session import get_spark

PG_PASSWORD = os.getenv("PG_PASSWORD", "postgres")   # ne commitez jamais un vrai mot de passe
engine = create_engine(f"postgresql+psycopg2://postgres:{PG_PASSWORD}@localhost:5432/sales_dw")

spark = get_spark("load")
for table in ["fact_sales", "dim_customer", "dim_product", "kpi_monthly_sales"]:
    pdf = spark.read.parquet(f"data/gold/{table}").toPandas()
    pdf.to_sql(table, engine, if_exists="replace", index=False)
    print(f"{table} : {len(pdf)} lignes chargées")
spark.stop()