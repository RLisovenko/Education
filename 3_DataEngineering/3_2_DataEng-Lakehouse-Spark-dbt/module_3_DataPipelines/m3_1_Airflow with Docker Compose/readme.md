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