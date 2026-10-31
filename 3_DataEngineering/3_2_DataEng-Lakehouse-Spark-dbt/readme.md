# Lakehouse Data Pipelines with Spark and dbt

## Module 3: 3.2.  Creating an Apache Iceberg Table on MinIO

## Introduction

This lab demonstrates how to create and manage an **Apache Iceberg table** using **Apache Spark** and **MinIO** as an S3-compatible object storage system.

The objective is to explore how a modern Lakehouse architecture combines scalable object storage, structured table metadata, and distributed data processing.

### Technologies

| Technology | Purpose |
|---|---|
| **Apache Spark** | Distributed data processing and SQL operations |
| **Apache Iceberg** | Lakehouse table format with metadata and snapshot management |
| **MinIO** | S3-compatible object storage for table data |
| **Docker Compose** | Containerized environment configuration and execution |
| **Apache Parquet** | Columnar storage format for analytical datasets |

## Lab Objectives

- Configure a local Spark and MinIO environment.
- Start the required services using Docker Compose.
- Configure Spark to work with Apache Iceberg.
- Create and query an Iceberg table.
- Explore table metadata and object storage.
- Verify the results of data operations.

## Project Structure

```text
m3_2_Iceberg Table on MinIO/
├── spark/
│   └── spark-defaults.conf
├── docker-compose.yml
└── readme.md
```

Additional files and directories will be documented as the lab progresses.

## Environment Setup

### 1. Prerequisites

The following tools are required:

- Docker Desktop
- Docker Compose
- Visual Studio Code
- PowerShell

### 2. Start Docker Services

From the project directory, validate the Docker Compose configuration:

```powershell
docker compose config --services
docker compose config --quiet
```

Start the configured services in detached mode:

```powershell
docker compose up -d
```

Verify the container status:

```powershell
docker compose ps
```

### 3. Verify the Environment

Before creating an Iceberg table, confirm that the required containers are running and that Spark can access the configured object storage.

The Spark configuration, Iceberg catalog, and MinIO connection settings will be documented in the following steps.




## Project Structure

```text
3_2_DataEng-Lakehouse-Spark-dbt/
│
├── .venv/
├── .gitignore
├── README.md
│
├── module_1_spark/
│   ├── arch/
│   ├── data/
│   ├── docs/
│   ├── output/
│   ├── scripts/
│   ├── requirements.txt
│   └── README.md
│
└── module_2_dbt/
    └── README.md
└── module_3_DataPipelines/
    └── README.md    
