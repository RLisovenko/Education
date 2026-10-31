# Lakehouse Data Pipelines with Spark and dbt

## Module 3

**Executor:** R. Lisovenko  
**Date:** 30.10.2026

### Running Apache Airflow with Docker Compose

```powershell
    mkdir airflow_docker_compose
    cd airflow_docker_compose
    mkdir dags
```
```
docker --version
docker compose version
dir
```
```
docker compose config --services
```
```text
### Verify Docker Compose Services

Check the services defined in `docker-compose.yaml`:


```powershell
docker compose config --services
```

**Expected output:**

```text
postgres
redis
airflow-init
airflow-api-server
airflow-dag-processor
airflow-scheduler
airflow-triggerer
airflow-worker
```
```text
This command validates the Docker Compose configuration and lists all defined services without starting containers.
```
### Initialize and Start Apache Airflow

Initialize the Airflow metadata database and create the administrator account:

```powershell
docker compose up airflow-init
```

**Result:** Database initialization and migrations completed successfully (`exit code 0`).

Start all services in detached mode and verify their status:

```powershell
docker compose up -d
docker compose ps
```

Access the Airflow Web UI at `http://localhost:8080`.
```
docker info
Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"
docker compose up airflow-init
docker compose up -d
docker compose ps
docker compose ps -a
```

### Start Apache Airflow Web UI

Start all Airflow services in the background:

```powershell
docker compose up -d
```

Verify that the containers are running:

```powershell
docker compose ps
```

Open the Airflow Web UI in your browser:

**URL:** http://localhost:8080

**Default credentials (local development only):**
- Username: `airflow`
- Password: `airflow`

After logging in, the **Airflow Dashboard** displays DAG statistics, execution history, and the health status of core components, including the Metadata Database, Scheduler, Triggerer, and DAG Processor.

### Building an Airflow DAG for a Batch Workflow
DAG Definition — определение рабочего процесса на Python.
Tasks & Operators — создание задач с помощью операторов Airflow.
Task Dependencies — настройка последовательности выполнения задач.
Scheduling — настройка расписания запуска. 
Execution & Monitoring — запуск DAG через Airflow Web UI и анализ результатов.

```
New-Item -Path ".\dags\retail_operations_batch.py" -ItemType File -Force
```

#### DAG — Directed Acyclic Graph

extract → validate → transform → load → quality_check

┌─────────────────────────────────────────┐
│  1. EXTRACT                            │
│  Read operations_raw.csv               │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  2. VALIDATE                           │
│  Check required fields and values      │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  3. TRANSFORM                          │
│  Normalize and format records          │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  4. LOAD                               │
│  Write operations_processed.csv        │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  5. QUALITY CHECK                      │
│  Verify the output file and records    │
└─────────────────────────────────────────┘

-  Check DAG

```text
docker compose exec airflow-dag-processor airflow dags list-import-errors --local

```
docker compose up -d
docker compose ps

docker compose exec airflow-apiserver airflow dags list | Select-String "retail_operations_batch"
docker compose exec airflow-dag-processor ls -l /opt/airflow/dags/
docker compose exec airflow-apiserver airflow dags list

### Enable and Trigger the Airflow DAG

Open the **Apache Airflow Web UI** at `http://localhost:8080` and navigate to **DAGs**.

1. Search for `retail_operations_batch`.
2. Enable the DAG using the **Pause / Unpause** toggle on the right.
3. Click the **Trigger (▶)** button to start the workflow manually.
4. Monitor task execution and verify the results.

![Airflow DAG Management](./pic/airflow-dag-enabled.png)

**DAG Configuration:**

- **DAG ID:** `retail_operations_batch`
- **Tags:** `batch`, `operations`
- **Schedule:** `None` (manual execution)
- **Status:** Enabled (Unpaused)

**Note:** Enabling a DAG does not automatically execute it when `schedule=None`. The workflow must be triggered manually.

## Batch Workflow Execution and Troubleshooting

### Successful DAG Execution

The `retail_operations_batch` DAG was executed manually in Apache Airflow 3.1.7 and completed successfully after resolving a Docker volume configuration issue.

**Execution results:**

| Parameter | Result |
|---|---|
| DAG ID | `retail_operations_batch` |
| Execution Mode | Manual Trigger |
| Tasks Completed | 5/5 |
| DAG Status | Success |
| Run Duration | 16.25 seconds |

**Task Execution Flow:**

```text
extract
   ↓
validate
   ↓
transform
   ↓
load
   ↓
quality_check
   ↓
SUCCESS
```

**Screenshot 1 — Successful DAG Run**

All five tasks completed successfully.

![Successful DAG Execution](./pic/airflow-dag-run-success.png)

**Screenshot 2 — DAG Overview**

The latest execution completed successfully. The previous failed run remains visible in the execution history.

![DAG Overview](./pic/airflow-dag-overview-success.png)

### Troubleshooting: Missing Input CSV File

**Problem:**

During the first execution, the `extract` task failed with:

```text
FileNotFoundError: [Errno 2] No such file or directory:
'/opt/airflow/data/operations_raw.csv'
```

**Root Cause:**

The input CSV file existed on the local machine, but the `data` directory was not mounted inside the Airflow Docker container.

The original Docker Compose configuration did not include the required volume mappings for the `data` and `output` directories.

**Solution:**

Add the following entries to the existing `volumes` section under `x-airflow-common` in `docker-compose.yaml`:

```yaml
- ${AIRFLOW_PROJ_DIR:-.}/data:/opt/airflow/data
- ${AIRFLOW_PROJ_DIR:-.}/output:/opt/airflow/output
```

Validate the configuration and recreate the Airflow worker:

```powershell
docker compose config --quiet
docker compose up -d --force-recreate airflow-worker
```

Verify that the CSV file is accessible:

```powershell
docker compose exec airflow-worker ls -l /opt/airflow/data/operations_raw.csv
```

**Final Result:**

After correcting the volume mappings and triggering the DAG again, all five tasks completed successfully.

**Key Takeaway:** Docker containers cannot automatically access arbitrary host directories. Explicit volume mappings are required for file-based data pipelines.



**URL:** http://localhost:8080
find  retail_operations_batch

Test-Path .\data\operations_raw.csv
docker compose exec airflow-worker ls -l /opt/airflow/data/


- change  docker-compose.yaml
```YAML
x-airflow-common:


volumes:
  - ${AIRFLOW_PROJ_DIR:-.}/dags:/opt/airflow/dags
  - ${AIRFLOW_PROJ_DIR:-.}/logs:/opt/airflow/logs
  - ${AIRFLOW_PROJ_DIR:-.}/config:/opt/airflow/config
  - ${AIRFLOW_PROJ_DIR:-.}/plugins:/opt/airflow/plugins
  - ${AIRFLOW_PROJ_DIR:-.}/data:/opt/airflow/data
  - ${AIRFLOW_PROJ_DIR:-.}/output:/opt/airflow/output
```
- Test
docker compose config --quiet
docker compose up -d --force-recreate airflow-worker
or
docker compose up -d
- Check /opt/airflow/data/ in Container
docker compose exec airflow-worker ls -lh /opt/airflow/data/

### DAG Overview and Execution Monitoring

To open the DAG Overview:

1. Open the Airflow Web UI at `http://localhost:8080`.
2. Navigate to **DAGs**.
3. Select `retail_operations_batch`.
4. Open the **Overview** tab and select **Last 24 Hours**.

The Overview dashboard displays:

- **Task Status:** Execution results for each task.
- **Failed Tasks / Runs:** Number of failures within the selected period.
- **Last DAG Runs:** Execution history and duration.
- **Run Duration:** Time required to execute each DAG.
- **Recent Failed Task Logs:** Information for troubleshooting failed tasks.

![Airflow DAG Overview](./pic/airflow-dag-overview.png)
![Airflow DAG Overview](./pic/airflow-dag-running.png)

**Result:** Three DAG runs are displayed: one initial failed run caused by a missing Docker volume mapping, followed by two successful runs after fixing the configuration. All five tasks completed successfully in the latest run.

### Output File Generation

After successful execution of the `retail_operations_batch` DAG, the **Load** task creates the processed CSV file in the `output` directory:

```text
output/
└── operations_processed.csv
```

The file contains **8 processed records** from `operations_raw.csv`, with validated and standardized data.

**Verify the output in PowerShell:**

```powershell
dir .\output
Get-Content .\output\operations_processed.csv
```

**Result:** The successful DAG execution produces `operations_processed.csv`, confirming that the Extract, Validate, Transform, Load, and Quality Check tasks have completed successfully.


### Project Directory Structure

Create the following directories and configuration files for running Apache Airflow with Docker Compose:

```text
airflow_docker_compose/
├── config/                # Airflow configuration
├── dags/                  # DAG definitions (Python)
├── logs/                  # Task execution logs
├── plugins/               # Custom Airflow plugins
├── .env                   # Environment variables
└── docker-compose.yaml    # Docker services configuration
```

**PowerShell commands:**

```powershell
mkdir config, dags, logs, plugins
New-Item .env -ItemType File
New-Item docker-compose.yaml -ItemType File
```

The `docker-compose.yaml` file defines the Airflow services, while `.env` stores environment variables used by Docker Compose.