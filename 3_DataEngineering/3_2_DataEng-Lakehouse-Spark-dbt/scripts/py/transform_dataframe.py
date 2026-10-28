# Executor: R. Lisovenko
# Date: 28.10.2026

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,                # Reference a DataFrame column / Обращение к столбцу DataFrame
    trim,               # Remove leading/trailing spaces / Удаляет пробелы в начале и конце строки
    initcap,            # Capitalize each word / Делает первую букву каждого слова заглавной
    upper,              # Convert text to uppercase / Переводит текст в верхний регистр
    when,               # Conditional logic, like SQL CASE WHEN / Условная логика, аналог CASE WHEN в SQL
    sum as spark_sum,   # Aggregate sum / Агрегирующая сумма
)

# Create and configure the Spark session for local execution # Создание и настройка Spark-сессии для локального выполнения
# df → selected_df → cleaned_df → active_df → derived_df → summary_df

spark = (
    SparkSession.builder
    .appName("TransformDataFrames")
    .master("local[2]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

print("=" * 70)
print("TRANSFORMING DATA WITH PYSPARK DATAFRAMES")
print("=" * 70)


# Read source CSV / Чтение исходного CSV
df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv("data/csv/operations_transform.csv")
)

print("\nSOURCE DATA")
print("-" * 70)
df.show()


# selected_df → cleaned_df → active_df → derived_df → summary_df

print("\nSELECTED COLUMNS")
print("-" * 70)

selected_df = df.select(
    "record_id",
    "source_system",
    "category",
    "quantity",
    "amount",
    "status",
)

selected_df.show()


# Clean and standardize DataFrame values /
# Очистка и стандартизация значений DataFrame
#
# 1. Normalize category names: trim spaces and capitalize words /
#    Нормализация category: убрать пробелы и привести к Customer, Inventory, Orders
#
# 2. Normalize status values: trim spaces and convert to uppercase /
#    Нормализация status: убрать пробелы и привести к ACTIVE, PENDING, INACTIVE
#
# 3. Replace non-positive quantity values with 1 /
#    Заменить quantity <= 0 на 1
#
# 4. Replace missing amount values with 0.0 /
#    Заменить NULL в amount на 0.0

print("\nCLEANED DATA")
print("-" * 70)

cleaned_df = (
    selected_df
    .withColumn(
        "category",
        initcap(trim(col("category")))
    )
    .withColumn(
        "status",
        upper(trim(col("status")))
    )
    .withColumn(
        "quantity",
        when(col("quantity") <= 0, 1)
        .otherwise(col("quantity"))
    )
    .withColumn(
        "amount",
        when(col("amount").isNull(), 0.0)
        .otherwise(col("amount"))
    )
)

cleaned_df.show()


# Filter only active records / Оставляем только активные записи
print("\nFILTERED ACTIVE RECORDS")
print("-" * 70)

active_df = cleaned_df.filter(
    col("status") == "ACTIVE"
)

active_df.show()


# Create a derived column: quantity * amount /
# Создаём вычисляемый столбец: quantity * amount
print("\nDERIVED COLUMN")
print("-" * 70)

derived_df = active_df.withColumn(
    "total_value",
    col("quantity") * col("amount")
)

derived_df.show()


# Aggregate active records by category /
# Агрегируем активные записи по категориям
print("\nCATEGORY AGGREGATION")
print("-" * 70)

summary_df = (
    derived_df
    .groupBy("category")  # Group rows by category / Группируем строки по category
    .agg(                 # Calculate aggregate values / Рассчитываем агрегированные значения
        spark_sum("quantity").alias("total_quantity"),
        spark_sum("total_value").alias("total_value")
    )
    .orderBy("category")
)

summary_df.show()