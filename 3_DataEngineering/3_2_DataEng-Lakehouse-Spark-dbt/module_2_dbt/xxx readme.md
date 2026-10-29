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

#### Building Staging and Intermediate Models

```
\q
dbt debug
```
```
psql -U postgres -d postgres
\c dbt_m2
```

```sql
CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA
```
```
\dn
```

```sql
CREATE TABLE raw.operations_raw (
    record_id INTEGER,
    source_system VARCHAR(50),
    category VARCHAR(100),
    quantity INTEGER,
    amount NUMERIC(10,2),
    status VARCHAR(50)
);
```

```
\d raw.operations_raw
```

```sql
INSERT INTO raw.operations_raw VALUES
(1, 'CRM', ' customer ', 12, 1500.50, 'active'),
(2, 'ERP', 'Inventory', 8, 2400.00, 'ACTIVE'),
(3, 'API', 'Orders', 15, 3200.75, 'pending'),
(4, 'CRM', 'Customer', 10, NULL, 'active'),
(5, 'ERP', ' inventory ', 20, 4100.00, 'ACTIVE'),
(6, 'API', 'Orders', 5, 2800.00, 'inactive'),
(7, 'CRM', 'Customer', 7, 1750.00, 'active'),
(8, 'ERP', 'Inventory', 6, 2200.00, 'pending');

```

```sql
SELECT * FROM raw.operations_raw;
```

#### Create 
- sources.yml
```
version: 2

sources:
  - name: raw
    schema: raw
    tables:
      - name: operations_raw
```
- stg_operations.sql
```sql
select
    record_id,
    upper(trim(source_system)) as source_system,
    initcap(trim(category)) as category,
    case
        when quantity <= 0 then 1
        else quantity
    end as quantity,
    coalesce(amount, 0) as amount,
    upper(trim(status)) as status
from {{ source('raw', 'operations_raw') }}
``` 
- int_operations_enriched.sql
```sql
select
    record_id,
    source_system,
    category,
    quantity,
    amount,
    status,
    quantity * amount as total_value
from {{ ref('stg_operations') }}
```
- dbt_project.yml
```text
name: 'transformation_project'
version: '1.0.0'
config-version: 2

profile: 'transformation_project'

model-paths: ["models"]
analysis-paths: ["analyses"]
test-paths: ["tests"]
seed-paths: ["seeds"]
macro-paths: ["macros"]
snapshot-paths: ["snapshots"]

target-path: "target"
clean-targets:
  - "target"
  - "dbt_packages"

models:
  transformation_project:
    staging:
      +materialized: view
    intermediate:
      +materialized: view

```
- run Dbt without psql and Education\3_DataEngineering\3_2_DataEng-Lakehouse-Spark-dbt> 
```
dbt run --project-dir .\module_2_dbt\transformation_project
```
```
cd module_2_dbt\transformation_project
dbt run
dbt ls
```
```
psql -U postgres -d dbt_m2
```

```sql
SELECT *
FROM analytics.stg_operations
ORDER BY record_id;

SELECT *
FROM analytics.int_operations_enriched
ORDER BY record_id;
```
### 2.5 Building Staging and Intermediate Models

- measurement model: Cr models\marts\dim_source_system.sql 
```sql
select distinct
    source_system,
    case
        when source_system = 'CRM' then 'Customer Operations'
        when source_system = 'ERP' then 'Supply Operations'
        when source_system = 'API' then 'Platform Engineering'
        else 'Unknown'
    end as owner_team
from {{ ref('int_operations_enriched') }}
```
- fact model: `fct_operations.sql` creates a fact model from the enriched intermediate operations data. It exposes the main operational measures and attributes, including quantity, amount, status, and calculated total value, for analytical use.

```SQL
select
    record_id,
    source_system,
    category,
    quantity,
    amount,
    status,
    total_value
from {{ ref('int_operations_enriched') }}
```
- dbt run
- dbt ls 
-  psql -U postgres -d dbt_m2

```sql
SELECT *
FROM analytics.dim_source_system
ORDER BY source_system;
```

```sql
SELECT *
FROM analytics.fct_operations
ORDER BY record_id;
```
### 2.6 Building Fact and Dimension Models

```
\q
```
```text
dbt debug

```

- CR Schema.yml
```text
dbt test

```
psql -U postgres -d dbt_m2

```sql
INSERT INTO analytics.fct_operations
(
    record_id,
    source_system,
    category,
    quantity,
    amount,
    total_value,
    is_active
)
VALUES
(
    999,
    'LEGACY',
    'Orders',
    2,
    1000.00,
    2000.00,
    true
);
```
```sql
select * 
from analytics.fct_operations
where record_id = 999;
```
\q
тест связи должен завершиться неудачей, поскольку  у legacy нет соответствующей записи в dim  underscore source underscore system.
dbt test --select fct_operations
psql -U postgres -d dbt_m2

```sql
delete from analytics.fct_operations 
where record_id = 999;

select * 
from analytics.fct_operations
where record_id = 999;
```
\q
dbt test 


- CR docs
```
dbt docs generate
dbt docs serve
```

```text
dbt docs generate
        ↓
создаются catalog.json / manifest.json
        ↓
dbt docs serve
        ↓
запускается локальный сайт
        ↓
браузер открывает документацию dbt
```

```sql
SELECT *
FROM analytics.fct_operations
WHERE source_system NOT IN (
    SELECT source_system
    FROM analytics.dim_source_system
);
```
```text
raw.operations_raw
        ↓
stg_operations
        ↓
int_operations_enriched
      ↙            ↘
dim_source_system  fct_operations
```
### dbt Documentation and Lineage

The generated dbt documentation provides an overview of the transformation models, their dependencies, tests, and lineage.

#### dbt Model Details

This view shows the generated dbt documentation for the model, including its metadata, columns, tests, and dependencies.

![dbt Model Details](pic/dbt_docs_model_details.png)

#### Staging Model


![dbt Staging Model](pic/dbt_stg_operations.png)

#### Intermediate Model

The `int_operations_enriched` model enriches the staging data and serves as the reusable transformation layer for downstream fact and dimension models.

![dbt Intermediate Model](pic/dbt_int_operations_enriched.png)

#### Dimension Model

The `dim_source_system` model represents the source-system dimension and includes data quality tests and dependency information.

![dbt Dimension Model](pic/dbt_dim_source_system.png)

#### Fact Model

The `fct_operations` model contains the analytical operational facts and derived measures used for reporting and analysis.

![dbt Fact Model](pic/dbt_fct_operations.png)

#### dbt Documentation Overview

dbt Docs provides a generated interface for exploring project models, database objects, dependencies, tests, and lineage.

![dbt Documentation Overview](pic/dbt_docs_overview.png)

#### dbt Lineage Graph

The lineage graph shows the complete transformation flow from the raw source data through staging and intermediate layers to the final fact and dimension models.

![dbt Lineage Graph](pic/dbt_lineage_graph.png)