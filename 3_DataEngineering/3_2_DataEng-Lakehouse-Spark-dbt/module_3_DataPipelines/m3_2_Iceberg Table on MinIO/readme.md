# Lakehouse Data Pipelines with Spark and dbt

## Module 3 — Data Pipelines / 3.2 Creating an Apache Iceberg Table on MinIO

**Course:** Lakehouse Data Pipelines with Spark and dbt  
**Module:** 3.2 — Data Pipelines  
**Executor:** R. Lisovenko  
**Date:** 31 October 2026

### Overview

This laboratory introduces an Apache Iceberg table backed by MinIO object storage and accessed through Apache Spark. Docker Compose provides an isolated environment for Spark, a REST catalog, and an S3-compatible storage service.

**Current status:** The project directory and a draft Docker Compose configuration have been prepared. Container startup, table creation, and data queries have **not yet been verified**. The configuration is adapted from a public Spark–Iceberg–MinIO example; it is not confirmed to be the exact file used in the course video.

### Objectives

- Start the containerized Spark–Iceberg–MinIO environment.
- Verify access to MinIO and the Iceberg catalog.
- Create an Iceberg table and insert sample data.
- Query the table and inspect its metadata and stored objects.
- Record configuration changes, commands, and results.

### Components

| Component | Role |
|---|---|
| Apache Spark | Executes SQL and distributed data processing |
| Apache Iceberg | Table format supporting snapshots, schema evolution, and metadata management |
| Iceberg REST Catalog | Catalog interface used to identify and manage tables |
| MinIO | S3-compatible storage for table data and metadata files |
| Docker Compose | Defines and runs the local containers |

### Project structure

```text
m3_2_Iceberg Table on MinIO/
├── spark/                  # Spark files, if required by the lab
├── docker-compose.yml     # Compose configuration for this lab
└── readme.md              # This document
```

Depending on the Compose volume mappings, additional local folders such as `warehouse/`, `notebooks/`, or `minio-data/` may appear. They are not required to be created manually before validating the configuration.

### 1. Prerequisites

Docker Desktop must be running with Linux containers. From PowerShell:

```powershell
docker --version
docker compose version
docker info
```

The active Python virtual environment on the host does not control Python packages inside the Docker containers.

### 2. Docker Compose configuration

A `docker-compose.yml` file is required in this lab directory. The draft used for the local setup defines these services:

| Service | Purpose |
|---|---|
| `spark-iceberg` | Spark runtime for Iceberg operations |
| `rest` | Iceberg REST Catalog |
| `minio` | S3-compatible object storage |
| `mc` | One-time initialization of the MinIO warehouse bucket |

The local Compose example maps the MinIO Console to port `9001`, the catalog to `8181`, and Spark's container port `8080` to host port `8081` to avoid conflicting with the Airflow lab on host port `8080`.

These values describe the local draft configuration and should be checked against the actual `docker-compose.yml` before use. The development-only MinIO credentials in that draft are `admin` / `password`; they must not be used for a public deployment.

### 3. Validate and start the environment

Run all commands from `m3_2_Iceberg Table on MinIO`, **not** from the previous Airflow lab directory:

```powershell
# Check the available services and YAML syntax
docker compose config --services
docker compose config --quiet

# Start the configured services
docker compose up -d
docker compose pull minio mc

# Inspect running and one-time containers
docker compose ps -a
```

Expected service names for the draft configuration:

```text
spark-iceberg
rest
minio
mc
```

The `mc` container is designed to finish after bucket setup; an `Exited (0)` status for this one-time service may be normal. Other services should remain running.

Check the service logs if startup fails:

```powershell
docker compose logs --tail 80 spark-iceberg rest minio mc
```

### 4. Access points (after successful startup)

| Service | Address | Notes |
|---|---|---|
| MinIO Console | http://localhost:9001 | Login uses the local Compose credentials |
| Iceberg REST Catalog | http://localhost:8181 | Service endpoint, not a full management UI |
| Spark Web UI | http://localhost:8081 | May appear only while a Spark application is active |
| Jupyter | http://localhost:8888 | Access depends on container startup and authentication settings |

These addresses are based on the draft port mappings, **not** on an observed successful container run.
- Open 
http://localhost:9001

- Username: admin
- Password: password

### 5. Iceberg table creation

The practical steps below remain to be completed and documented once the local environment starts successfully:

1. Verify Spark access to the configured Iceberg catalog.
2. Confirm that the warehouse bucket exists in MinIO.
3. Create an Iceberg namespace and table.
4. Insert sample records and execute queries.
5. Inspect the object storage layout and table metadata.

The exact SQL statements and output will be recorded after execution, rather than assumed in advance.

### 6. Managing the environment

Stop this lab's containers without deleting named volumes:

```powershell
docker compose down
```

Avoid adding `-v` unless the intent is to delete associated volumes. Bind-mounted files and directories are managed separately.

### Reference

- [Databricks — docker-spark-iceberg (example environment)](https://github.com/databricks/docker-spark-iceberg)

The Docker Compose configuration may differ from the course author's setup. The observed service states and table operations should determine the remaining documentation.
