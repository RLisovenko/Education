# Module 3 — Data Pipelines
## 3.3 Building an Orchestrated Batch Lakehouse Pipeline

**Course:** Lakehouse Data Pipelines with Spark and dbt  
**Module:** 3.3 — Data Pipelines  
**Executor:** R. Lisovenko  
**Date:** 01 November 2026

### 1. Introduction

This laboratory demonstrates an orchestrated batch Lakehouse
pipeline for processing daily logistics and shipment data.

#### Business Scenario

A logistics company receives daily shipment data from
multiple distribution centers.

The raw data may contain:
- Inconsistent names.
- Mixed shipment status formats.
- Missing shipping costs.

The pipeline uses Apache Airflow to orchestrate the workflow,
Apache Spark to clean and transform the data, Apache Iceberg
to manage the table, and MinIO to store it.

### 2. Key Components

| Component | Purpose |
|---|---|
| Apache Airflow | Workflow orchestration |
| Apache Spark | Data cleaning and transformation |
| Apache Iceberg | Lakehouse table management |
| MinIO | S3-compatible object storage |
| Docker Compose | Containerized infrastructure |

### 3. Pipeline Workflow

```text
Daily Shipment Data
        |
        v
  Apache Airflow
        |
        v
   Apache Spark
        |
        v
  Apache Iceberg
        |
        v
       MinIO
```

### 4. Structure

```
New-Item -ItemType Directory -Force -Path `
    "data/raw", `
    "data/processed", `
    "spark/jobs" | Out-Null
```
```
New-Item -ItemType File -Force -Path `
    "dags/logistics_lakehouse_pipeline.py", `
    "data/raw/daily_shipments.csv", `
    "spark/spark-defaults.conf"
```
```text
m3_3_Orchestrated Batch Lakehouse Pipeline/
│
├── config/
├── dags/
│   └── logistics_lakehouse_pipeline.py
├── data/
│   ├── raw/
│   │   └── daily_shipments.csv
│   └── processed/
├── logs/
├── plugins/
├── spark/
│   ├── jobs/
│   └── spark-defaults.conf
├── pic/
│
├── docker-compose.yml
├── Scenario.md
└── readme.md
```

### 4. Implementation

The configuration files, DAGs, Spark scripts,
execution commands, and verification results
will be documented during the laboratory.

**Status:** In progress.

### 4.1 Input Dataset — Daily Shipments

**File:** `data/raw/daily_shipments.csv`

The input dataset contains eight shipment records from multiple
distribution centers.

The raw data intentionally includes inconsistent capitalization,
extra whitespace, mixed shipment statuses, and one missing
shipping cost.

These data quality issues will be addressed during the
Apache Spark transformation stage.
```
docker compose config --quiet
docker compose pull minio
docker compose up -d
docker compose ps -a
```

с др лаб http://localhost:8080/
http://localhost:8083/dags

docker compose exec airflow-worker sh -c "command -v docker || echo DOCKER_CLI_MISSING"

docker exec lakehouse-spark /opt/spark/bin/spark-submit --master "local[2]" --conf spark.jars.ivy=/tmp/.ivy2 --packages "org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.10.1,org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.262" /opt/project/spark/jobs/batch_lakehouse_job.py


docker exec lakehouse-spark ls -l /opt/project/data/raw/daily_shipments.csv

docker exec lakehouse-spark /opt/spark/bin/spark-submit --master "local[2]" --conf spark.jars.ivy=/tmp/.ivy2 --packages "org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.10.1,org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.262" /opt/project/spark/jobs/batch_lakehouse_job.py

docker exec lakehouse-spark /opt/spark/bin/spark-submit --master "local[2]" --conf spark.jars.ivy=/tmp/.ivy2 --packages "org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.10.1,org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.262" /opt/project/spark/jobs/batch_lakehouse_job.py
```
$LASTEXITCODE
```

### Airflow Pipeline Execution — Successful

All four tasks completed successfully.

- Source file validation: SUCCESS
- Spark batch processing: SUCCESS
- Iceberg table validation: SUCCESS
- Pipeline completion: SUCCESS

**Validated records:** 8  
**Iceberg table:** `demo.logistics.shipment_analytics`  
**Storage:** MinIO (`warehouse/iceberg/logistics/`)

![Successful Airflow Pipeline](./pic/airflow_pipeline_success.png)


## 5. Troubleshooting and Environment Adaptation

**Date:** 01 November 2026  
**Environment:** Windows, PowerShell, Docker Desktop (WSL2)  
**Lab:** Building an Orchestrated Batch Lakehouse Pipeline  
**Executor:** R. Lisovenko  
**Final Result:** SUCCESS — 4 of 4 Airflow tasks completed

### 5.1 Background

The laboratory environment was reconstructed from the course video and adapted to the existing local Docker setup.

The original example used Apache Airflow 3.3.1, Apache Spark 3.5.7, Apache Iceberg, MinIO, PostgreSQL, and Redis.

Several configuration issues occurred during deployment. Each was investigated using Docker logs, Spark SQL commands, Airflow task logs, and MinIO Object Browser.

The troubleshooting process provided practical experience in debugging containerized data pipelines, resolving configuration conflicts, and validating individual components before running the complete workflow.

### 5.2 Docker Deployment Issues

| # | Problem | Cause | Resolution |
|---|---|---|---|
| 1 | MinIO image pull failed | `minio/minio:latest` could not be pulled from Docker Hub | Replaced with `cgr.dev/chainguard/minio:latest` |
| 2 | YAML parsing error | Duplicate `image:` keyword in `docker-compose.yml` | Corrected the image declaration |
| 3 | Airflow failed to start | Host port `8080` was already allocated | Changed the host port to `8083` |
| 4 | MinIO failed to start | Host port `9000` was already allocated | Changed host ports to `9002` and `9003` |
| 5 | Several containers remained in `Created` state | Container startup was interrupted by port conflicts | Corrected port mappings and reran Docker Compose |

**Corrected MinIO configuration:**

```yaml
minio:
  image: cgr.dev/chainguard/minio:latest
  container_name: lakehouse-minio
  ports:
    - "127.0.0.1:9002:9000"
    - "127.0.0.1:9003:9001"
  environment:
    MINIO_ROOT_USER: admin
    MINIO_ROOT_PASSWORD: password123
  command: ["server", "/data", "--console-address", ":9001"]
  volumes:
    - minio-data:/data
```

**Corrected Airflow API Server port:**

```yaml
ports:
  - "127.0.0.1:8083:8080"
```

The container-side ports remained unchanged. Only the Windows host port mappings were modified.

**Deployment commands:**

```powershell
docker compose config --quiet
docker compose pull minio
docker compose up -d
docker compose ps -a
```

**Result:** All 10 Docker Compose services completed the startup sequence. The Airflow API Server became healthy, and the DAG was discovered successfully.

The `airflow-init` container exited with code `0`, which is expected after successful database initialization.

### 5.3 Service Addresses and Ports

The laboratory uses the following local development endpoints.

| Service | Windows Host Address | Docker Internal Address | Purpose |
|---|---|---|---|
| Airflow UI / API | `http://localhost:8083` | `http://airflow-apiserver:8080` | DAG orchestration |
| MinIO Console | `http://localhost:9003` | `http://minio:9001` | Object Browser |
| MinIO S3 API | `http://localhost:9002` | `http://minio:9000` | S3-compatible storage |
| PostgreSQL | Not published | `postgres:5432` | Airflow metadata database |
| Redis | Not published | `redis:6379` | Celery message broker |
| Spark | Docker container | `lakehouse-spark` | Batch data processing |

**Local demonstration credentials for MinIO:**

- Username: `admin`
- Password: `password123`

These credentials are intended only for local educational use and must not be reused in production.

**Previously configured laboratory endpoints:**

| Laboratory | Service | Host Address |
|---|---|---|
| Module 3.1 | Airflow | `http://localhost:8080` |
| Module 3.2 | MinIO Console | `http://localhost:9001` |
| Module 3.2 | MinIO S3 API | `http://localhost:9000` |
| Module 3.3 | Airflow | `http://localhost:8083` |
| Module 3.3 | MinIO Console | `http://localhost:9003` |
| Module 3.3 | MinIO S3 API | `http://localhost:9002` |

Docker service names are used for communication between containers instead of fixed container IP addresses.

### 5.4 Airflow and Docker Integration

The Airflow DAG uses `subprocess.run()` to execute Spark commands through `docker exec`.

Before execution, the Airflow Worker was checked for Docker CLI availability, Docker Engine access, and mounted project files.

**Verification commands:**

```powershell
docker compose exec airflow-worker docker version

docker compose exec airflow-worker docker inspect lakehouse-spark --format '{{.State.Status}}'

docker compose exec airflow-worker ls /opt/project/data/raw/daily_shipments.csv

docker exec lakehouse-spark ls /opt/project/spark/jobs/batch_lakehouse_job.py
```

**Results:**

- Docker CLI was available inside the Airflow Worker.
- Docker Engine access was confirmed.
- The Spark container was running.
- Both the input CSV and Spark Job were accessible.

**Security note:** Docker socket access grants broad Docker Engine permissions to the Airflow container. This approach was used only for the isolated local laboratory.

### 5.5 Spark Input File Error

**Error:**

```text
[PATH_NOT_FOUND]
Path does not exist:
file:/home/iceberg/data/raw/daily_shipments.csv
```

**Cause:**

The Spark Job originally used a file path from the previous laboratory environment. The new Docker Compose mounted the project data directory at `/opt/project/data`.

**Resolution:**

Updated `spark/jobs/batch_lakehouse_job.py`:

```python
INPUT_PATH = "/opt/project/data/raw/daily_shipments.csv"
```

**Verification:**

```powershell
docker exec lakehouse-spark ls /opt/project/data/raw/daily_shipments.csv
```

**Result:** Spark successfully read all eight shipment records.

### 5.6 Iceberg Catalog Configuration Error

**Error:**

```text
invalidDatabaseNameError
database -> demo.logistics
```

**Cause:**

The Iceberg catalog `demo` was not correctly configured in the new Spark environment.

The instructor used a catalog named `local`, while the previous laboratory had used `demo`. The new configuration was standardized on `demo`.

**Resolution:**

Added the Iceberg catalog configuration to `spark/spark-defaults.conf`:

```properties
spark.sql.extensions org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions

spark.sql.catalog.demo org.apache.iceberg.spark.SparkCatalog
spark.sql.catalog.demo.type hadoop
spark.sql.catalog.demo.warehouse s3a://warehouse/iceberg
```

The new laboratory uses an Iceberg Hadoop Catalog backed by MinIO.

**SQL table name:**

```sql
demo.logistics.shipment_analytics
```

### 5.7 MinIO and S3A Storage Errors

**Error:**

```text
java.lang.IllegalArgumentException:
path must be absolute
```

**Cause:**

The Iceberg Hadoop Catalog encountered an error while accessing the root S3A warehouse path.

The initial configuration used:

```properties
spark.sql.catalog.demo.warehouse s3a://warehouse/
```

**Resolution:**

Changed the warehouse location to a dedicated prefix inside the bucket:

```properties
spark.sql.catalog.demo.warehouse s3a://warehouse/iceberg
```

The S3A connection used the following configuration:

```properties
spark.hadoop.fs.s3a.impl org.apache.hadoop.fs.s3a.S3AFileSystem
spark.hadoop.fs.s3a.endpoint http://minio:9000
spark.hadoop.fs.s3a.path.style.access true
spark.hadoop.fs.s3a.connection.ssl.enabled false
spark.hadoop.fs.s3a.access.key admin
spark.hadoop.fs.s3a.secret.key password123
spark.hadoop.fs.s3a.aws.credentials.provider org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider
```

The `warehouse` bucket was created separately in the Module 3.3 MinIO Console.

After changing the warehouse location, the original S3A path error disappeared.

### 5.8 Creating the Iceberg Namespace

**Error:**

```text
NoSuchNamespaceException:
Namespace does not exist
```

**Cause:**

The dedicated warehouse prefix had not yet been initialized with the `logistics` namespace.

**Resolution:**

Executed the following Spark SQL statement:

```sql
CREATE NAMESPACE IF NOT EXISTS demo.logistics;
```

The resulting structure was confirmed using MinIO Object Browser:

```text
warehouse/
└── iceberg/
    └── logistics/
```

**Result:** The namespace was successfully created, and subsequent Iceberg operations became available.

### 5.9 Spark Job Validation

The Spark Job was executed independently before attempting another Airflow run.

**Command:**

```powershell
docker exec lakehouse-spark /opt/spark/bin/spark-submit --master "local[2]" --conf spark.jars.ivy=/tmp/.ivy2 --packages "org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.10.1,org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.262" /opt/project/spark/jobs/batch_lakehouse_job.py
```

The Spark processing completed the following operations:

1. Read eight shipment records from CSV.
2. Validated required source columns.
3. Standardized distribution center names.
4. Normalized shipment statuses.
5. Replaced missing shipping costs with `0.0`.
6. Calculated shipping cost per package.
7. Created and populated the Iceberg table.
8. Validated the processed dataset.

**Successful output:**

```text
LOGISTICS BATCH LAKEHOUSE PIPELINE COMPLETED SUCCESSFULLY
```

**Exit code:**

```powershell
$LASTEXITCODE
# 0
```

The Iceberg table was additionally verified with:

```sql
SELECT COUNT(*) AS record_count
FROM demo.logistics.shipment_analytics;
```

**Result:** `8` records.

### 5.10 Airflow DAG Validation Error

The Airflow pipeline initially failed in the following task:

```text
validate_iceberg_table
RuntimeError: Unable to validate the Iceberg table
```

**Cause and investigation:**

The Spark Job completed successfully, and a separate Spark SQL query returned eight records.

Therefore, the issue was isolated to the DAG validation command rather than the underlying Iceberg table.

**Resolution:**

The DAG validation command was aligned with the successfully tested Spark SQL invocation.

```python
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
```

The failed validation task was cleared and executed again.

**Result:** `validate_iceberg_table` completed successfully.

### 5.11 Python DAG Import Error

During a modification to the DAG validation function, a closing parenthesis was accidentally omitted.

**Symptoms:**

```text
Dag Import Error
Deactivated
404 Not Found — DAG not found
```

**Cause:**

The modified Python file contained a syntax error, preventing Airflow from importing the updated DAG.

**Resolution:**

The missing parenthesis was restored, and the task execution was repeated.

**Recommended verification commands:**

```powershell
docker compose exec airflow-dag-processor python -m py_compile /opt/airflow/dags/logistics_lakehouse_pipeline.py

docker compose exec airflow-dag-processor airflow dags list-import-errors
```

The final run succeeded. A historical `Dag Import Error` / `Deactivated` indicator remained visible in the Airflow interface at the time of the final screenshot, so its cleanup should be verified separately.

### 5.12 Final Pipeline Execution

**DAG:** `logistics_batch_lakehouse_pipeline`

All four Airflow tasks completed successfully.

| Task | Description | Final Status |
|---|---|---|
| `check_source_file` | Validate source CSV availability | SUCCESS |
| `run_spark_lakehouse_job` | Execute Spark batch transformation | SUCCESS |
| `validate_iceberg_table` | Verify eight records in Iceberg | SUCCESS |
| `pipeline_complete` | Confirm successful completion | SUCCESS |

**Final execution result:**

```text
DAG Run: SUCCESS

check_source_file          SUCCESS
run_spark_lakehouse_job    SUCCESS
validate_iceberg_table     SUCCESS
pipeline_complete          SUCCESS

4 / 4 TASKS SUCCESSFUL
```

**Technical summary:**

| Component | Verified Result |
|---|---|
| Apache Airflow 3.3.1 | DAG execution successful |
| Apache Spark 3.5.7 | Batch transformation successful |
| Apache Iceberg | Table created and validated |
| MinIO | Warehouse bucket and namespace created |
| Input records | 8 |
| Validated table records | 8 |
| Spark Job exit code | 0 |

**Completed data flow:**

```text
daily_shipments.csv
        |
        v
Apache Airflow
        |
        v
Apache Spark
  - Read
  - Validate
  - Clean
  - Transform
        |
        v
Apache Iceberg
demo.logistics.shipment_analytics
        |
        v
MinIO Object Storage
warehouse/iceberg/logistics/
        |
        v
Airflow Validation
        |
        v
PIPELINE SUCCESS
```

![Successful Airflow Pipeline](./pic/airflow_pipeline_success.png)

### 5.13 Lessons Learned

The laboratory demonstrated several practical aspects of Data Engineering:

- Docker images and host port mappings must be compatible with the local environment.
- Mounted container paths must match the paths used in application code.
- Spark, Iceberg, and object storage configuration should be validated independently.
- Processing errors should be isolated before rerunning the complete DAG.
- Spark SQL commands provide an effective way to verify Iceberg tables.
- Airflow logs help identify failures at individual workflow stages.
- Reproducible configuration and troubleshooting documentation are essential for maintaining data pipelines.

**Final outcome:** A functional orchestrated batch Lakehouse pipeline was implemented using Apache Airflow, Apache Spark, Apache Iceberg, and MinIO.


### Starting the Spark SQL CLI

Launch the interactive Spark SQL interface inside the
`lakehouse-spark` Docker container.

The command loads the Apache Iceberg runtime, Hadoop AWS
libraries, and the AWS Java SDK to work with Iceberg tables
stored in MinIO.

After startup, Spark SQL can be used to query and validate
the `demo.logistics.shipment_analytics` table.

### MinIO Object Storage Verification

The successful execution of the Spark Job and Airflow pipeline
was verified using the MinIO Object Browser.

**MinIO Console:** http://localhost:9003

**Iceberg Table:** `demo.logistics.shipment_analytics`

**Warehouse:** `s3a://warehouse/iceberg`

#### Iceberg Table Structure

The table contains two directories:
- `data/` — stores processed shipment data in Parquet format.
- `metadata/` — stores Iceberg table metadata and snapshot information.

![Iceberg Table Structure](./pic/minio_iceberg_table_structure.png)

#### Parquet Data Files

Two Parquet files were observed in the MinIO Object Browser.
The Iceberg table was independently validated with 8 records.

![Parquet Data Files](./pic/minio_iceberg_parquet_files.png)

#### Iceberg Metadata Files

The metadata directory contains Avro manifest-related files,
snapshot information, metadata JSON files and a version hint.

![Iceberg Metadata Files](./pic/minio_iceberg_metadata_files.png)

#### Final Result

- Apache Spark batch processing: SUCCESS
- Iceberg table creation: SUCCESS
- SQL record validation: 8 records
- MinIO object storage: VERIFIED
- Apache Airflow execution: 4/4 TASKS SUCCESSFUL