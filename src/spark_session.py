import os
import sys
from pyspark.sql import SparkSession

# Correctif Windows pour Hadoop / Spark
if os.name == "nt":
    os.environ["HADOOP_HOME"] = r"C:\hadoop"
    os.environ["PATH"] = r"C:\hadoop\bin" + os.pathsep + os.environ["PATH"]

# Utiliser le Python du venv (évite l'erreur "Python worker failed to connect back")
os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

def get_spark(app_name="sales_etl"):
    return (SparkSession.builder
            .appName(app_name)
            .master("local[*]")
            .config("spark.sql.shuffle.partitions", "4")
            .getOrCreate())