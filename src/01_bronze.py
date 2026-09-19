import re
from pyspark.sql import functions as F
from spark_session import get_spark

spark = get_spark("bronze")

# Extract : lecture du CSV brut (tout en texte, on ne modifie pas les valeurs)
df = (spark.read
      .option("header", True)
      .option("inferSchema", False)
      .csv("data/raw/train.csv"))

# Seule modification en Bronze : les noms de colonnes ("Order ID" -> "order_id"),
# car le format Parquet n'accepte pas les espaces.
for c in df.columns:
    df = df.withColumnRenamed(c, re.sub(r"[^0-9a-zA-Z]+", "_", c).strip("_").lower())

df = df.withColumn("ingestion_ts", F.current_timestamp())

print("Lignes lues :", df.count())
df.printSchema()
df.show(5, truncate=False)

df.write.mode("overwrite").parquet("data/bronze/sales")
spark.stop()