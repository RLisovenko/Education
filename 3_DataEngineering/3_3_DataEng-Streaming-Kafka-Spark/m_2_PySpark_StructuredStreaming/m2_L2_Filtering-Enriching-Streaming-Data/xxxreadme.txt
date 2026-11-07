docker ps
узнать Версии пайтон py -0p
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip

установим кафка и Спарк
.\.venv\Scripts\python.exe -m pip install pyspark==3.5.7 kafka-python==2.2.15
проверим
.\.venv\Scripts\python.exe -c "from pyspark.sql import SparkSession; from pyspark.sql.functions import col, from_json, when; from pyspark.sql.types import StructType, StructField, StringType, DoubleType; print('PySpark imports OK')"

docker exec -it filtering-enrichment-spark /opt/spark/bin/spark-submit --conf spark.jars.ivy=/tmp/.ivy2 --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.7 /opt/project/filtering_enrichment.py
docker compose config --services
docker compose up -d spark
docker compose ps
docker update --cpus=2 --memory=3g --memory-swap=4g filtering-enrichment-spark
docker network connect runningapachekafkalocally_default filtering-enrichment-spark