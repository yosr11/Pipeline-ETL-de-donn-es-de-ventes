from pyspark.sql import functions as F
from spark_session import get_spark

DATE_FORMAT = "dd/MM/yyyy"   # À ADAPTER : regardez vos dates (ex. "M/d/yyyy")

spark = get_spark("silver")
bronze = spark.read.parquet("data/bronze/sales")
n_bronze = bronze.count()

silver = (bronze
    .dropDuplicates(["order_id", "product_id"])                 # doublons
    .withColumn("order_date", F.to_date("order_date", DATE_FORMAT))   # texte -> date
    .withColumn("ship_date", F.to_date("ship_date", DATE_FORMAT))
    .withColumn("sales", F.col("sales").cast("double"))         # texte -> nombre
    .fillna({"postal_code": "UNKNOWN"})                         # valeurs manquantes
    .dropna(subset=["order_id", "order_date", "sales"])         # lignes inutilisables
    .filter(F.col("sales") > 0)
    .withColumn("year", F.year("order_date"))
    .withColumn("month", F.month("order_date"))
)

n_silver = silver.count()
print(f"Bronze : {n_bronze} lignes | Silver : {n_silver} lignes | Supprimées : {n_bronze - n_silver}")

# Sécurité : si le format de date est faux, toutes les lignes disparaissent
if n_silver == 0:
    raise ValueError("Silver est vide : vérifiez DATE_FORMAT")

silver.write.mode("overwrite").parquet("data/silver/sales")
spark.stop()