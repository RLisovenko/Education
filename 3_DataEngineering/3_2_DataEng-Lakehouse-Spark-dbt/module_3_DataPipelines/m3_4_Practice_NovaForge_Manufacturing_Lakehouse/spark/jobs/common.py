"""Shared Spark configuration for the NovaForge training project."""
import os
from pyspark.sql import SparkSession

PACKAGES = (
    "org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.10.1,"
    "org.apache.hadoop:hadoop-aws:3.3.4,"
    "com.amazonaws:aws-java-sdk-bundle:1.12.262,"
    "org.postgresql:postgresql:42.7.5"
)
JDBC_OPTIONS = {
    "url": os.environ.get("PG_URL", "jdbc:postgresql://postgres:5432/manufacturing"),
    "user": os.environ.get("PG_USER", "novaforge"),
    "password": os.environ.get("PG_PASSWORD", "novaforge_dev_2026"),
    "driver": "org.postgresql.Driver",
}

def spark_session(name):
    session = (SparkSession.builder
               .appName(name)
               .master("local[2]")
               .getOrCreate())
    session.sparkContext.setLogLevel("WARN")
    return session

def load_jdbc(spark, relation):
    return spark.read.format("jdbc").options(**JDBC_OPTIONS, dbtable=relation).load()

def write_jdbc(df, relation):
    # Raw tables are created by postgres-init and cleared by Airflow BEFORE ingestion.
    # Append avoids DROP TABLE operations, which would invalidate downstream dbt views.
    (df.write.format("jdbc")
     .options(**JDBC_OPTIONS, dbtable=relation)
     .mode("append")
     .save())
