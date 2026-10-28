# Lakehouse Data Pipelines with Spark and dbt

## Module 1 — Distributed Processing with PySpark

**Executor:** R. Lisovenko  
**Date:** 28.10.2026  
**Status:** Completed ✅

---

### 1. Overview

This module focuses on distributed data processing with Apache Spark and PySpark.

The module covers Spark architecture, distributed execution, data locality, DataFrames, CSV/JSON/Parquet processing, Spark SQL, partitions, shuffles, execution plans, caching, persistence, and recomputation.

The goal is to develop practical skills in scalable data processing and understand how Spark executes and optimizes distributed workloads.

#### Tools and Technologies

| Category | Technologies |
|---|---|
| Data Processing | Apache Spark, PySpark |
| Query Engine | Spark SQL |
| Programming | Python |
| Data Formats | CSV, JSON, Apache Parquet |
| Development | VS Code, PowerShell |
| Runtime | Java JDK 17 |
| Version Control | Git, GitHub |

---

### 2. Topics

- Apache Spark Architecture and Execution Flow
- Data Locality and Distributed Processing
- Setting Up PySpark Locally
- Reading CSV, JSON, and Parquet with PySpark
- Transforming Data with PySpark DataFrames
- Narrow and Wide Transformations
- Analysing Data with Spark SQL
- Partitions, Shuffles, and Execution Plans
- Caching, Persistence, and Recomputation
- Distributed Processing with PySpark

---

### 3. Project Structure

The course repository is divided into separate modules.

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
│   │   ├── csv/
│   │   ├── json/
│   │   └── parquet/
│   │
│   ├── docs/
│   ├── output/
│   │
│   ├── scripts/
│   │   ├── ps/
│   │   │   ├── configure_java.ps1
│   │   │   └── configure_pyspark.ps1
│   │   │
│   │   ├── py/
│   │   │   ├── spark_setup_check.py
│   │   │   ├── read_data_formats.py
│   │   │   └── transform_dataframe.py
│   │   │
│   │   ├── spark_sql_analysis.py
│   │   └── partitions_execution_plan.py
│   │
│   ├── requirements.txt
│   └── README.md
│
└── module_2_dbt/
    └── README.md
```

#### Module Organization

- `arch/` — architecture notes and diagrams.
- `data/` — source datasets used in exercises.
- `docs/` — additional module documentation.
- `output/` — generated processing results.
- `scripts/ps/` — PowerShell configuration scripts.
- `scripts/py/` — Python and PySpark scripts.
- `requirements.txt` — Python dependencies for Spark exercises.
- `README.md` — Module 1 documentation.

The shared `.venv` is stored in the course root and is used by the module scripts.

---

### 4. Local Development Environment

#### 4.1 Environment Configuration

**Operating System:** Windows  
**Development Environment:** Visual Studio Code / PowerShell

| Component | Version | Status |
|---|---:|---|
| Python | 3.12.10 | Installed |
| Java JDK | Eclipse Temurin 17.0.20.1 | Installed |
| PySpark | 4.2.0 | Installed |
| Py4J | 0.10.9.9 | Installed |
| Pandas | 3.1.0 | Installed |
| PyArrow | 26.0.0 | Installed |
| NumPy | 2.5.4 | Installed |

#### 4.2 Activate the Shared Virtual Environment

From `module_1_spark`:

```powershell
..\.venv\Scripts\Activate.ps1
```

Verify:

```powershell
python --version
python -c "import sys; print(sys.executable)"
```

Expected interpreter:

```text
...\3_2_DataEng-Lakehouse-Spark-dbt\.venv\Scripts\python.exe
```

---

### 5. Java and PySpark Configuration

#### 5.1 Java

Apache Spark requires a compatible Java Development Kit.

This environment uses:

```text
Eclipse Temurin JDK 17.0.20.1
```

Installation directory:

```text
C:\dev_soft\Java\jdk-17
```

Verify:

```powershell
java -version
javac -version
echo $env:JAVA_HOME
```

#### 5.2 Python Dependencies

Current `requirements.txt`:

```text
# Course — Lakehouse Data Pipelines with Spark and dbt
# Module 1 — Distributed Processing with PySpark
# Python 3.12.10 / Java 17

pyspark==4.2.0
pandas
pyarrow
```

Install dependencies from `module_1_spark`:

```powershell
python -m pip install -r requirements.txt
```

Verify PySpark:

```powershell
python -m pip show pyspark
python -m pip list
```

#### 5.3 PowerShell Configuration Scripts

Configure Java:

```powershell
. .\scripts\ps\configure_java.ps1
```

Configure PySpark:

```powershell
. .\scripts\ps\configure_pyspark.ps1
```

The PySpark configuration script resolves the shared virtual environment from the course root and configures:

```text
PYSPARK_PYTHON
PYSPARK_DRIVER_PYTHON
SPARK_LOCAL_IP
```

The leading dot followed by a space is PowerShell **dot-sourcing**. It executes the script in the current PowerShell session.

---

### 6. Core Spark Concepts

#### 6.1 Spark Architecture

Apache Spark is a distributed data processing engine designed to process large datasets efficiently.

Main components:

| Component | Description |
|---|---|
| Driver | Coordinates Spark application execution |
| SparkSession | Main entry point for Spark SQL and DataFrame operations |
| Executors | Execute tasks and process partitions |
| Worker Nodes | Machines that host executor processes |
| DataFrame | Distributed collection of structured data |
| Partitions | Logical divisions of distributed datasets |
| Transformations | Define operations on data |
| Actions | Trigger actual computation |

Basic execution model:

```text
Python
   ↓
PySpark
   ↓
Py4J
   ↓
JVM / Apache Spark
   ↓
Driver
   ↓
Tasks
   ↓
Executors
```

#### 6.2 Data Locality

Data locality means processing data as close as possible to where it is stored.

Key principles:

- Moving large datasets across a network is expensive.
- Network transfers introduce serialization and coordination overhead.
- More machines do not automatically mean faster processing.
- Data movement between partitions can significantly increase execution cost.

> Move computation closer to data whenever practical rather than moving large datasets between machines.

#### 6.3 Lazy Evaluation

Spark transformations are evaluated lazily.

Examples of transformations:

```text
select()
filter()
withColumn()
groupBy()
```

They define a processing plan but do not immediately execute it.

Actions trigger computation:

```text
show()
count()
collect()
write()
```

Example:

```python
filtered_df = df.filter(df.status == "ACTIVE")
filtered_df.show()
```

The `filter()` defines the transformation.  
The `show()` triggers execution.

#### 6.4 DataFrame Immutability

Spark DataFrames are immutable.

A transformation does not modify the original DataFrame. It creates a new DataFrame representing another logical processing plan.

```python
active_df = df.filter(df.status == "ACTIVE")
```

`df` remains unchanged.

---

### 7. Reading CSV, JSON, and Parquet

PySpark provides the `spark.read` interface for loading structured and semi-structured data.

#### Supported Formats

| Format | Description | PySpark Method |
|---|---|---|
| CSV | Text-based tabular format | `spark.read.csv()` |
| JSON | Structured / semi-structured format | `spark.read.json()` |
| Parquet | Column-oriented analytical format | `spark.read.parquet()` |

#### CSV

```python
df_csv = spark.read.csv(
    "data/csv/operations_data.csv",
    header=True,
    inferSchema=True
)
```

#### JSON

```python
df_json = spark.read.json(
    "data/json/operations_data.json"
)
```

#### Parquet

```python
df_parquet = spark.read.parquet(
    "data/parquet/operations_data.parquet"
)
```

#### Key Concepts

- **Schema** defines column names and data types.
- **Schema inference** automatically determines data types from source data.
- **Parquet** stores schema metadata with the data.
- **Columnar storage** improves many analytical workloads by storing values by column.

#### Run the Exercise

From `module_1_spark`:

```powershell
python .\scripts\py\read_data_formats.py
```

**Result:** CSV, JSON, and Parquet were successfully read with PySpark.

Each test dataset contained:

```text
6 columns
5 records
```

---

### 8. Transforming Data with PySpark DataFrames

The transformation exercise uses:

```text
data/csv/operations_transform.csv
```

Main processing flow:

```text
df
 ↓
selected_df
 ↓
cleaned_df
 ↓
active_df
 ↓
derived_df
 ↓
summary_df
```

Equivalent logical stages:

```text
SOURCE DATA
   ↓
SELECTED COLUMNS
   ↓
CLEANED DATA
   ↓
FILTERED ACTIVE RECORDS
   ↓
DERIVED COLUMN
   ↓
CATEGORY AGGREGATION
```

#### Transformation Functions

```python
from pyspark.sql.functions import (
    col,
    trim,
    initcap,
    upper,
    when,
    sum as spark_sum,
)
```

Functions used:

- `col()` — reference a DataFrame column.
- `trim()` — remove leading and trailing spaces.
- `initcap()` — capitalize words.
- `upper()` — convert text to uppercase.
- `when()` — conditional logic similar to SQL `CASE WHEN`.
- `spark_sum()` — aggregate numeric values.

#### Cleaning Rules

1. Normalize `category` values.
2. Normalize `status` values.
3. Replace `quantity <= 0` with `1`.
4. Replace missing `amount` values with `0.0`.

#### Filter Active Records

```python
active_df = cleaned_df.filter(
    col("status") == "ACTIVE"
)
```

#### Derived Column

```python
derived_df = active_df.withColumn(
    "total_value",
    col("quantity") * col("amount")
)
```

#### Aggregation

```python
summary_df = (
    derived_df
    .groupBy("category")
    .agg(
        spark_sum("quantity").alias("total_quantity"),
        spark_sum("total_value").alias("total_value")
    )
    .orderBy("category")
)
```

Logical sequence:

```text
groupBy → agg → orderBy
```

#### Run the Script

Using Python:

```powershell
python .\scripts\py\transform_dataframe.py
```

Using Spark Submit:

```powershell
spark-submit .\scripts\py\transform_dataframe.py
```

---

### 9. Analysing Data with Spark SQL

Spark DataFrames can be registered as temporary SQL views:

```python
operations_df.createOrReplaceTempView("operations")
systems_df.createOrReplaceTempView("systems")
```

This allows DataFrames to be queried using Spark SQL.

Processing flow:

```text
SparkSession
   ↓
operations.csv + systems.csv
   ↓
Temporary Views
operations / systems
   ↓
ACTIVE RECORDS
   ↓
CATEGORY METRICS
   ↓
SYSTEM OWNERSHIP JOIN
   ↓
SYSTEM-LEVEL METRICS
   ↓
OVERALL METRICS
   ↓
spark.stop()
```

#### Active Records

```sql
SELECT
    record_id,
    source_system,
    category,
    quantity,
    amount
FROM operations
WHERE status = 'ACTIVE'
ORDER BY record_id
```

#### Category Metrics

```sql
SELECT
    category,
    COUNT(*) AS record_count,
    SUM(quantity) AS total_quantity,
    SUM(quantity * amount) AS total_value
FROM operations
WHERE status = 'ACTIVE'
GROUP BY category
ORDER BY total_value DESC
```

The total value is calculated by multiplying `quantity` by `amount` before applying `SUM()`:

```sql
SUM(quantity * amount)
```

#### Join with System Information

```sql
SELECT
    o.record_id,
    o.source_system,
    s.system_name,
    s.owner_team,
    o.category,
    o.quantity,
    o.amount,
    o.status
FROM operations o
INNER JOIN systems s
    ON o.source_system = s.source_system
ORDER BY o.record_id
```

#### Run the Script

From `module_1_spark`:

```powershell
python .\scripts\spark_sql_analysis.py
```

---

### 10. Partitions, Shuffles, and Execution Plans

#### 10.1 Partitions

Spark divides datasets into logical units called **partitions**.

Different partitions can be processed in parallel by different executor tasks.

Efficient partitioning helps distribute work across available resources.

#### 10.2 Partition Skew

Partition skew occurs when data is distributed unevenly.

Example:

```text
Partition 1 → 100 MB
Partition 2 → 110 MB
Partition 3 → 95 MB
Partition 4 → 5 GB
```

The largest partition becomes a bottleneck because the whole job must wait for its processing to finish.

#### 10.3 Narrow Transformations

A narrow transformation can usually process each input partition without moving data between partitions.

Examples:

```text
select
filter
withColumn
map
```

#### 10.4 Wide Transformations

Wide transformations may require data to move between partitions.

Examples:

```text
groupBy
join
orderBy
distinct
```

These operations may trigger a **shuffle**.

#### 10.5 Shuffle

Shuffle redistributes related data between partitions and executors.

It can increase:

- network communication;
- serialization overhead;
- memory usage;
- disk activity;
- execution time.

Therefore, unnecessary shuffles should be avoided.

#### 10.6 Execution Plans

Spark builds logical and physical execution plans before running a job.

Execution plans can be inspected using:

```python
df.explain()
```

This helps identify:

- scans;
- filters;
- joins;
- exchanges;
- shuffles;
- aggregation stages;
- execution strategy.

---

### 11. Caching, Persistence, and Recomputation

Spark may recompute intermediate DataFrames when the same transformation chain is required by multiple actions.

Caching allows selected intermediate results to be retained for reuse.

Example:

```python
df.cache()
```

Persistence can use different storage strategies depending on memory and disk requirements.

Caching is most useful when:

- a DataFrame is reused multiple times;
- recomputation is expensive;
- enough memory or storage is available.

The optimization decision can be viewed as:

```text
Recomputation Cost
        ↕
Storage Cost
        ↕
Frequency of Reuse
```

Caching should therefore be a deliberate optimization decision rather than a default step for every DataFrame.

---

### 12. Local Spark Resource Optimization

For local development, Spark can be limited to a small number of CPU threads.

Default:

```python
.master("local[*]")
```

This allows Spark to use all available logical CPU cores.

Alternative for small local exercises:

```python
.master("local[2]")
```

Example configuration:

```python
spark = (
    SparkSession.builder
    .appName("Lakehouse-Setup")
    .master("local[2]")
    .config("spark.driver.memory", "1g")
    .config("spark.sql.shuffle.partitions", "2")
    .getOrCreate()
)
```

| Parameter | Value | Purpose |
|---|---:|---|
| `local[2]` | 2 threads | Limit local task concurrency |
| `spark.driver.memory` | 1 GB | Configure driver JVM heap |
| `spark.sql.shuffle.partitions` | 2 | Reduce shuffle partitions for small datasets |

These values are useful for small local exercises and are not universal production settings.

---

### 13. Environment Verification

The local PySpark environment was verified by:

- creating a SparkSession;
- checking the Spark version;
- creating a test DataFrame;
- executing DataFrame operations;
- displaying results;
- stopping the SparkSession.

Run:

```powershell
python .\scripts\py\spark_setup_check.py
```

Verified components:

| Component | Result | Status |
|---|---|---|
| Python 3.12.10 | Virtual environment | Passed |
| Java JDK 17.0.20.1 | JVM initialization | Passed |
| PySpark 4.2.0 | SparkSession initialization | Passed |
| Spark DataFrame | Creation and processing | Passed |
| `DataFrame.show()` | Correct output | Passed |
| `SparkSession.stop()` | Clean completion | Passed |

---

### 14. Troubleshooting

#### 14.1 Java Is Not Recognized

Error:

```text
java: The term 'java' is not recognized
```

Verify:

```powershell
$env:JAVA_HOME = "C:\dev_soft\Java\jdk-17"
$env:Path = "$env:JAVA_HOME\bin;$env:Path"
```

Then:

```powershell
java -version
javac -version
```

---

#### 14.2 Java Gateway Exited

Possible error:

```text
PySparkRuntimeError: [JAVA_GATEWAY_EXITED]
```

Verify:

- Java installation;
- `JAVA_HOME`;
- `PATH`;
- PySpark environment configuration.

---

#### 14.3 Python Worker Failed to Connect

Possible error:

```text
Python worker failed to connect back
```

Configure PySpark:

```powershell
. .\scripts\ps\configure_pyspark.ps1
```

The configuration ensures that Spark uses:

```text
...\3_2_DataEng-Lakehouse-Spark-dbt\.venv\Scripts\python.exe
```

for both the driver and Python worker processes.

---

#### 14.4 Incorrect Working Directory

Scripts in this README assume that the current directory is:

```text
module_1_spark
```

Example:

```powershell
cd .\module_1_spark
python .\scripts\py\transform_dataframe.py
```

Relative dataset paths such as:

```text
data/csv/operations_transform.csv
```

are resolved from this directory.

---

#### 14.5 Hadoop Windows Utilities and Parquet Writing

**Environment:** Windows, PySpark 4.2.0.

Local Spark initialization, DataFrame processing, and CSV/JSON reading were successful.

Writing Parquet directly with Spark encountered the Windows Hadoop utilities issue:

```text
HADOOP_HOME and hadoop.home.dir are unset
```

For the reading exercise, a Parquet file was generated with Pandas/PyArrow and successfully read with PySpark.

Example:

```powershell
python -c "import pandas as pd; df = pd.read_csv('data/csv/operations_data.csv'); df.to_parquet('data/parquet/operations_data.parquet', engine='pyarrow', index=False)"
```

Then:

```powershell
python .\scripts\py\read_data_formats.py
```

Important distinction:

- Spark `DataFrameWriter.parquet(...)` normally creates a directory containing `part-*.parquet` files.
- PyArrow `DataFrame.to_parquet(...)` creates a single Parquet file.

**Result:** PySpark successfully read the PyArrow-generated Parquet file.

Spark-based Parquet writing on this Windows environment remains a documented local limitation.

---

#### 14.6 Pandas Compatibility Warning

Current environment:

```text
Pandas 3.1.0
```

Some PySpark/Pandas integration functionality may report compatibility warnings with Pandas 3.x.

This did not prevent the PySpark exercises in Module 1 from being completed.

---

### 15. Key Takeaways

After completing this module:

- Spark applications can distribute processing across partitions and executors.
- DataFrames provide a structured distributed data abstraction.
- Transformations are evaluated lazily.
- Actions trigger Spark execution.
- DataFrames are immutable.
- Parquet contains schema metadata and is optimized for analytical processing.
- `groupBy`, `join`, and `orderBy` can trigger expensive shuffle operations.
- Uneven partition sizes can cause data skew and processing bottlenecks.
- Spark SQL allows DataFrames to be queried using SQL syntax.
- Execution plans help explain how Spark processes a query.
- Caching can reduce repeated computation when intermediate results are reused.
- Resource configuration should reflect the workload and development environment.

---

### 16. Module Progress

| Date | Activity | Status |
|---|---|---|
| 27.10.2026 | Python 3.12 virtual environment | Completed |
| 27.10.2026 | Java JDK 17 configuration | Completed |
| 27.10.2026 | PySpark 4.2.0 installation | Completed |
| 27.10.2026 | SparkSession verification | Completed |
| 27.10.2026 | CSV, JSON, and Parquet processing | Completed |
| 28.10.2026 | DataFrame transformations | Completed |
| 28.10.2026 | Spark SQL analysis | Completed |
| 28.10.2026 | Partitions, shuffles, and execution plans | Completed |
| 28.10.2026 | Module 1 knowledge checks | Completed |
| 28.10.2026 | Distributed Processing with PySpark graded assignment | Completed |
| 28.10.2026 | **Module 1 — Distributed Processing with PySpark** | **Completed ✅** |

---

### 17. Final Status

**Last Updated:** 28.10.2026  
**Module Status:** Completed ✅

Module 1 established the practical foundation for distributed data processing with Apache Spark and PySpark.

The environment was configured and verified locally, multiple data formats were processed, DataFrame transformations were implemented, Spark SQL was used for analytical queries, and distributed execution concepts such as partitions, shuffles, data skew, execution plans, caching, and recomputation were studied.

**Next Step:** Module 2 — Transformation Engineering with dbt.

---

**Executor:** R. Lisovenko  
**Course:** Lakehouse Data Pipelines with Spark and dbt  
**Specialization:** Data Engineering with Open Source Tools