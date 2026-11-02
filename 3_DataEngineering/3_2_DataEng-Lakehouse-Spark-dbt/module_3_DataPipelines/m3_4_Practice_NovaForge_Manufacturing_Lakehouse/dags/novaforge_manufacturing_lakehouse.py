"""Airflow 3 orchestration for the NovaForge sample manufacturing lakehouse.

Execution uses Docker SDK via a mounted local Docker socket. Local training only.
"""
from datetime import datetime, timedelta
from pathlib import Path
import re
import docker
from airflow.sdk import dag, task, get_current_context

SPARK_CONTAINER="novaforge-spark"
DBT_CONTAINER="novaforge-dbt"
POSTGRES_CONTAINER="novaforge-postgres"
SPARK_SUBMIT="/opt/spark/bin/spark-submit"
SPARK_PACKAGES=(
    "org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.10.1,"
    "org.apache.hadoop:hadoop-aws:3.3.4,"
    "com.amazonaws:aws-java-sdk-bundle:1.12.262,"
    "org.postgresql:postgresql:42.7.5"
)

def execute(container_name, command):
    client=docker.from_env()
    try:
        container=client.containers.get(container_name)
        if container.status != "running":
            raise RuntimeError(f"Container {container_name} is not running")
        result=container.exec_run(command, stream=False, demux=False)
        output=result.output.decode("utf-8",errors="replace") if result.output else ""
        print(output[-25000:])
        print(f"Command exit code: {result.exit_code}")
        if result.exit_code != 0:
            raise RuntimeError(f"{container_name} returned exit code {result.exit_code}")
    finally:
        client.close()

def spark_job(filename, *args):
    cmd=[SPARK_SUBMIT, "--master", "local[2]", "--conf", "spark.jars.ivy=/tmp/.ivy2",
         "--packages", SPARK_PACKAGES, f"/opt/project/spark/jobs/{filename}", *args]
    execute(SPARK_CONTAINER,cmd)

def dbt_job(*args):
    execute(DBT_CONTAINER,["dbt", *args, "--project-dir", "/usr/app", "--profiles-dir", "/usr/app"])

@dag(
    dag_id="novaforge_manufacturing_lakehouse",
    schedule=None,  # manual lab runs; see docs/BACKFILL.md for production schedule considerations
    start_date=datetime(2026,10,1),
    catchup=False,
    default_args={"owner":"R. Lisovenko", "retries":1,
                  "retry_delay":timedelta(minutes=2)},
    tags=["novaforge","manufacturing","demo","pyspark","dbt","iceberg","minio"],
)
def novaforge_manufacturing_lakehouse():
    @task
    def check_source_files():
        files=[
            "raw/production_orders.csv", "raw/machine_operations.jsonl",
            "seed/quality_inspections.jsonl", "raw/maintenance_records.csv",
            "raw/facilities.csv", "raw/production_lines.csv", "raw/machines.csv",
            "raw/products.csv",
        ]
        root=Path("/opt/project/data")
        for name in files:
            path=root/name
            if not path.exists() or path.stat().st_size == 0:
                raise FileNotFoundError(f"Missing or empty source: {path}")
        conf=get_current_context()["dag_run"].conf or {}
        batch_date=conf.get("batch_date")
        if batch_date:
            if not isinstance(batch_date,str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", batch_date):
                raise ValueError("batch_date must be YYYY-MM-DD")
            datetime.strptime(batch_date,"%Y-%m-%d")
        print("Source checks completed", "batch_date:",batch_date or "all")
        return batch_date

    @task
    def prepare_parquet_source():
        spark_job("bootstrap_quality_parquet.py")

    @task
    def run_pyspark_processing(batch_date):
        # Preserve raw table definitions and dbt views; clear rows before Spark append.
        tables = ["production_orders","machine_operations","quality_inspections",
                  "facilities","production_lines","machines","products","maintenance_records"]
        sql = "TRUNCATE TABLE " + ", ".join("raw." + name for name in tables) + ";"
        execute(POSTGRES_CONTAINER,["psql","-U","novaforge","-d","manufacturing","-c",sql])
        args=["--batch-date",batch_date] if batch_date else []
        spark_job("ingest_manufacturing.py",*args)

    @task
    def run_dbt_transformations():
        dbt_job("run")

    @task
    def run_dbt_tests():
        dbt_job("test")

    @task
    def write_iceberg_output():
        spark_job("export_to_iceberg.py")

    @task
    def validate_final_results():
        spark_job("validate_lakehouse.py")
        print("NOVAFORGE ORCHESTRATED PIPELINE COMPLETED SUCCESSFULLY")

    batch=check_source_files()
    parquet=prepare_parquet_source()
    processed=run_pyspark_processing(batch)
    dbt_run=run_dbt_transformations()
    tests=run_dbt_tests()
    output=write_iceberg_output()
    validated=validate_final_results()
    batch >> parquet >> processed >> dbt_run >> tests >> output >> validated

novaforge_manufacturing_lakehouse()
