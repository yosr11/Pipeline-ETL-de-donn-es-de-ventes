from pyspark.sql import functions as F
from spark_session import get_spark

spark = get_spark("gold")
silver = spark.read.parquet("data/silver/sales")

# Table de faits (les ventes) + 2 dimensions (clients, produits) = modèle en étoile
fact_sales = silver.select("order_id", "order_date", "ship_date",
                           "customer_id", "product_id", "region", "sales")
dim_customer = (silver.select("customer_id", "customer_name", "segment")
                .dropDuplicates(["customer_id"]))
dim_product = (silver.select("product_id", "category", "sub_category", "product_name")
               .dropDuplicates(["product_id"]))

# Table d'indicateurs (agrégation Spark)
kpi_monthly_sales = (silver.groupBy("year", "month")
                     .agg(F.round(F.sum("sales"), 2).alias("total_sales"),
                          F.countDistinct("order_id").alias("nb_orders"))
                     .orderBy("year", "month"))

for name, table in [("fact_sales", fact_sales), ("dim_customer", dim_customer),
                    ("dim_product", dim_product), ("kpi_monthly_sales", kpi_monthly_sales)]:
    table.write.mode("overwrite").parquet(f"data/gold/{name}")
    print(name, "->", table.count(), "lignes")

spark.stop()