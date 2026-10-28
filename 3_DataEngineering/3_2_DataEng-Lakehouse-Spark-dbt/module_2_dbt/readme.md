# Lakehouse Data Pipelines with Spark and dbt

## Module 2 — Transformation Engineering with dbt

**Executor:** R. Lisovenko  
**Date:** 28.10.2026

This module focuses on transformation engineering with dbt Core.

### Topics

- ETL, ELT, and Analytics Engineering
- Layered Modelling with dbt Core
- Model Materialization Strategies
- Setting Up dbt Core with PostgreSQL
- Staging and Intermediate Models
- Fact and Dimension Models
- Testing and Documentation
- Data Contracts and Change Management

### Structure

```text
module_2_dbt/
├── README.md
├── dbt_project/
├── models/
├── seeds/
└── tests/
```

### Goal

Build a structured dbt project with reusable transformation models, tests, documentation, and analytics-ready datasets.

### 2.3 Model Materialization Strategies in dbt

dbt models are written in SQL, but their results can be represented in different ways in the target database. These options are called **materializations**.

The main materialization strategies are:

| Materialization | Description | Best Use |
|---|---|---|
| `view` | Stores the SQL definition; data is calculated when queried | Lightweight and frequently changing transformations |
| `table` | Stores the complete transformed result physically | Frequently queried and stable analytical models |
| `incremental` | Processes only new or changed records after the initial build | Large and continuously growing datasets |
| `ephemeral` | Exists only as reusable SQL compiled into downstream models | Small reusable intermediate transformations |

#### Selection Principle

Materialization should be selected based on:

- dataset size;
- frequency of reuse;
- transformation cost;
- query performance requirements;
- storage requirements.

Typical approach:

```text
Lightweight transformation → view
Frequently reused model     → table
Large growing dataset       → incremental
Reusable helper logic       → ephemeral
```

#### Key Takeaway

There is no single best materialization for every model.

The goal is to balance:

```text
Query Performance ↔ Storage Cost ↔ Rebuild Cost ↔ Maintainability
```

Thoughtful materialization choices make dbt projects more efficient, scalable, and easier to maintain.

### 2.4 Setting Up dbt Core with PostgreSQL

#### Environment Check

The existing shared Python virtual environment and PostgreSQL installation are reused for Module 2.


```powershell
deactivate
..\.venv\Scripts\Activate.ps1
python --version
psql --version
```

**Official Documentation:** [dbt PostgreSQL Setup](https://docs.getdbt.com/docs/local/connect-data-platform/postgres-setup)

This official dbt documentation explains how to connect dbt Core to PostgreSQL. It covers installation of the PostgreSQL adapter, connection configuration, database credentials, and the basic setup required to run dbt projects with PostgreSQL.

```
python -m pip install --upgrade pip
python -m pip install dbt-postgres
dbt --version
where.exe dbt
```

```
cd 3_2_DataEng-Lakehouse-Spark-dbt\module_2_dbt
type requirements.txt
```
- Change pswd 
psql -U postgres -d postgres
```sql
ALTER USER postgres WITH PASSWORD 'NewStrongPassword';
CREATE DATABASE dbt_m2;
```
\l  - list DB
\q  -  Quit 

```
dbt init transformation_project
```
```
Enter a number: 1
host:     localhost
port:     5432
user:     postgres
dbname:   dbt_m2
schema:   analytics
threads:  1

```
-  dir
```text
module_2_dbt/
└── transformation_project/
    ├── analyses/
    ├── macros/
    ├── models/
    ├── seeds/
    ├── snapshots/
    ├── tests/
    └── dbt_project.yml
```

```
cd 3_2_DataEng-Lakehouse-Spark-dbt\module_2_dbt\transformation_project
dbt debug
```
- Connect to dbt_m2
- Check

```
\c dbt_m2
psql -U postgres -d dbt_m2
\dn
\dt
```
This confirms that dbt is connected to the correct database and is ready for the transformation workflow.

The dbt debug output confirms that the project is configured correctly: the dbt project was created, the PostgreSQL profile is configured, the database connection works, and all configuration checks passed.

The local dbt environment is now ready for transformation development.

In this setup, dbt Core and the PostgreSQL adapter were installed, a dbt project was created, and the PostgreSQL connection profile was configured.