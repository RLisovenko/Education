#**Executor:** LiR  
#**Date:** 01 November 2026

from airflow.sdk import dag, task
from datetime import datetime
import os
import subprocess


SOURCE_FILE = "/opt/project/data/raw/daily_shipments.csv"
SPARK_CONTAINER = "lakehouse-spark"

SPARK_JOB = "/opt/project/spark/jobs/batch_lakehouse_job.py"

SPARK_PACKAGES = (
    "org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.10.1,"
    "org.apache.hadoop:hadoop-aws:3.3.4,"
    "com.amazonaws:aws-java-sdk-bundle:1.12.262"
)


@dag(
    dag_id="logistics_batch_lakehouse_pipeline",
    schedule=None,
    start_date=datetime(2026, 8, 1),
    catchup=False,
    tags=["logistics", "spark", "iceberg", "minio"],
)
def logistics_batch_lakehouse_pipeline():

    @task
    def check_source_file():
        if not os.path.exists(SOURCE_FILE):
            raise FileNotFoundError(
                f"Source shipment file not found: {SOURCE_FILE}"
            )

        if os.path.getsize(SOURCE_FILE) == 0:
            raise ValueError("Source shipment file is empty")

        print("Source shipment batch is available")
        print(f"Source file: {SOURCE_FILE}")

    @task
    def run_spark_lakehouse_job():
        command = [
            "docker",
            "exec",
            SPARK_CONTAINER,
            "/opt/spark/bin/spark-submit",
            "--conf",
            "spark.jars.ivy=/tmp/.ivy2",
            "--packages",
            SPARK_PACKAGES,
            SPARK_JOB,
        ]

        print("Starting Spark lakehouse job")

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
        )

        print(result.stdout)

        if result.stderr:
            print(result.stderr)

        if result.returncode != 0:
            raise RuntimeError(
                f"Spark job failed with exit code {result.returncode}"
            )

        print("Spark lakehouse job completed successfully")

    @task
    def validate_iceberg_table():
        sql_query = (
            "SELECT COUNT(*) AS record_count "
            "FROM demo.logistics.shipment_analytics"
        )
        command = [
            "docker",
            "exec",
            SPARK_CONTAINER,
            "/opt/spark/bin/spark-sql",
            "--master",
            "local[2]",
            "--conf",
            "spark.jars.ivy=/tmp/.ivy2",
            "--packages",
            SPARK_PACKAGES,
            "-e",
            sql_query,
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
        )

        print(result.stdout)

        if result.stderr:
            print(result.stderr)

        if result.returncode != 0:
            raise RuntimeError(
                "Unable to validate the Iceberg table"
            )

        if "8" not in result.stdout:
            raise ValueError(
                "Expected 8 shipment records in the Iceberg table"
            )

        print("Iceberg table validation passed")

    @task
    def pipeline_complete():
        print("=" * 70)
        print("LOGISTICS BATCH LAKEHOUSE PIPELINE COMPLETED")
        print("=" * 70)
        print("Airflow orchestration: SUCCESS")
        print("Spark transformation: SUCCESS")
        print("Iceberg table validation: SUCCESS")
        print("MinIO lakehouse storage: READY")

    source_ready = check_source_file()
    spark_complete = run_spark_lakehouse_job()
    table_validated = validate_iceberg_table()
    completed = pipeline_complete()

    source_ready >> spark_complete >> table_validated >> completed


logistics_batch_lakehouse_pipeline()
