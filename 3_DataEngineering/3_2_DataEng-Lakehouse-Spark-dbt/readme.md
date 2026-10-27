# Lakehouse Data Pipelines with Spark and dbt

**Specialization:** Data Engineering with Open Source Tools  
**Performed by:** R. Lisovenko  
**Started:** 27.10.2026  
**Status:** In Progress

---

## 1. Overview

This course focuses on building scalable batch data pipelines using open-source technologies.

It covers distributed data processing with Apache Spark and PySpark, analytical transformations with dbt Core, workflow orchestration with Apache Airflow, and lakehouse storage using MinIO and Apache Iceberg.

The goal is to develop practical skills in data processing, transformation, orchestration, and analytical data management.

### Tools and Technologies

| Category | Technologies |
|---|---|
| Data Processing | Apache Spark, PySpark, Spark SQL |
| Data Transformation | dbt Core, SQL |
| Database | PostgreSQL |
| Orchestration | Apache Airflow |
| Data Storage | MinIO, Apache Iceberg, Apache Parquet |
| Development | Python, VS Code |
| Infrastructure | Docker, Docker Compose |
| Version Control | Git, GitHub |

---

## 2. Course Modules

| Module | Topic | Duration | Status |
|---|---|---|---|
| 1 | Distributed Processing with PySpark | 2 hours | In Progress |
| 2 | Transformation Engineering with dbt | 1 hour | Not Started |
| 3 | Orchestration and Lakehouse Foundations | 2 hours | Not Started |
| **Total** | | **5 hours** | |

---

## 3. Key Concepts

### 3.1 Data Locality

**Module 1 — Distributed Processing with PySpark**

Data locality is an important principle in distributed data processing.

**Key Takeaways:**

- **Data locality:** Processing data close to where it is stored reduces unnecessary network transfers.
- **Data movement:** Transferring data between workers introduces network, serialization, and coordination overhead.
- **Scalability:** Adding more machines does not always improve performance, especially for small workloads.
- **Spark processing:** Operations involving data movement between partitions can increase execution costs.

**Key Principle:**

> Move computation closer to data whenever practical, rather than moving large datasets between machines.

### 3.2 Distributed Processing with Apache Spark

Apache Spark is a distributed data processing engine designed to process large datasets efficiently.

Spark can distribute computations across multiple CPU cores or machines.

**Main Components:**

| Component | Description |
|---|---|
| Spark Driver | Coordinates Spark application execution |
| SparkSession | Main entry point for Spark SQL and DataFrame operations |
| Executors | Execute tasks and process data |
| DataFrame | Distributed collection of structured data |
| Partitions | Logical divisions of distributed datasets |
| Transformations | Define operations on distributed data |
| Actions | Trigger execution of Spark computations |

**Important:** Spark introduces additional resource overhead compared with Pandas. For small datasets, Pandas may be more efficient.

---

## 4. Local Development Environment

### 4.1 Environment Configuration

**Operating System:** Windows  
**Development Environment:** Visual Studio Code / PowerShell

| Component | Version | Status |
|---|---|---|
| Python | 3.12.10 | Installed |
| Java JDK | Eclipse Temurin 17.0.20.1 | Installed |
| PySpark | 4.2.0 | Installed |
| Py4J | 0.10.9.9 | Installed |
| Pandas | 3.1.0 | Installed |
| PyArrow | 26.0.0 | Installed |
| NumPy | 2.5.4 | Installed |

**Note:** PySpark 4.2.0 reports a compatibility warning for Pandas 3.x. If Pandas integration is required, use a compatible Pandas version.

### 4.2 Project Structure

```text
3_2_DataEng-Lakehouse-Spark-dbt/
│
├── .venv/
│   └── Scripts/
│       └── python.exe
│
├── data/
│
├── output/
│
├── scripts/
│   ├── ps/
│   │   ├── configure_java.ps1
│   │   └── configure_pyspark.ps1
│   │
│   └── py/
│       └── spark_setup_check.py
│
├── .gitignore
├── requirements.txt
└── README.md
```

**Project Organization:**

- `.venv/` — Isolated Python environment.
- `data/` — Input datasets.
- `output/` — Generated processing results.
- `scripts/ps/` — PowerShell environment configuration scripts.
- `scripts/py/` — Python and PySpark scripts.
- `requirements.txt` — Python dependencies.
- `.gitignore` — Excluded files and directories.
- `README.md` — Project documentation.

---

## 5. Python Installation and Virtual Environment

### 5.1 Python Installation

The project uses Python 3.12.10.

Official Python distribution:

https://www.python.org/downloads/release/python-31210/

Verify the installed Python versions:

```powershell
python --version
py --list
where.exe python
```

### 5.2 Create a Virtual Environment

From the project root directory:

```powershell
# Create a Python virtual environment.
py -3.12 -m venv .venv
```

Activate the environment:

```powershell
# Activate the virtual environment.
.\.venv\Scripts\Activate.ps1
```

Verify the Python interpreter:

```powershell
python --version
python -c "import sys; print(sys.executable)"
```

Expected Python executable:

```text
...\3_2_DataEng-Lakehouse-Spark-dbt\.venv\Scripts\python.exe
```

**Note:** Always activate the project virtual environment before installing Python dependencies.

---

## 6. Java JDK Installation

### 6.1 Install Java 17

Apache Spark requires a compatible Java Development Kit.

This project uses:

**Eclipse Temurin JDK 17.0.20.1**

Official download:

https://adoptium.net/temurin/releases/?version=17

Installation directory:

```text
C:\dev_soft\Java\jdk-17
```

### 6.2 Configure Java Environment Variables Permanently

1. Press **Win + R**.
2. Enter `sysdm.cpl`.
3. Open **Advanced → Environment Variables**.
4. Under **User variables**, create or update:

   **Variable:**

   ```text
   JAVA_HOME
   ```

   **Value:**

   ```text
   C:\dev_soft\Java\jdk-17
   ```

5. Edit the **Path** variable.
6. Add:

   ```text
   %JAVA_HOME%\bin
   ```

7. Save the configuration.
8. Restart VS Code.

**Important:** Do not delete existing Path entries or duplicate the JAVA_HOME variable.

### 6.3 Verify Java Installation

```powershell
java -version
javac -version
echo $env:JAVA_HOME
```

Expected result:

```text
openjdk version "17.0.20.1"
javac 17.0.20.1
C:\dev_soft\Java\jdk-17
```

---

## 7. Install PySpark

### 7.1 Python Dependencies

The project uses `requirements.txt` to manage Python dependencies.

Current configuration:

```text
# Course 2 — Lakehouse Data Pipelines with Spark and dbt
# Python 3.12.10 / Java 17

# Module 1 — Distributed Processing with PySpark
pyspark==4.2.0
pandas
pyarrow
```

### 7.2 Install Dependencies

Activate the virtual environment and execute:

```powershell
# Install project dependencies.
python -m pip install -r requirements.txt
```

Verify PySpark:

```powershell
python -m pip show pyspark
```

Check installed packages:

```powershell
python -m pip list
```

---

## 8. PowerShell Configuration Scripts

Two PowerShell scripts are used to configure Java and PySpark.

### 8.1 configure_java.ps1

**Location:** `scripts/ps/configure_java.ps1`

**Purpose:** Configure Java JDK 17 for Apache Spark.

```powershell
# ------------------------------------------------------------
# Course: Lakehouse Data Pipelines with Spark and dbt
# Script: configure_java.ps1
# Performed by: R. Lisovenko
# Started: 27.10.2026
#
# Description:
# Configure Java JDK 17 for Apache Spark on Windows.
# ------------------------------------------------------------

# Set the Java installation directory.
$env:JAVA_HOME = "C:\dev_soft\Java\jdk-17"

# Add Java binaries to PATH if they are not already present.
$javaBin = Join-Path $env:JAVA_HOME "bin"

if (($env:Path -split ";") -notcontains $javaBin) {
    $env:Path = "$javaBin;$env:Path"
}

# Verify Java configuration.
Write-Host "JAVA_HOME: $env:JAVA_HOME"

java -version
javac -version
```

**Note:** Java environment variables are already configured permanently in Windows. This script can be used to verify or restore the configuration.

### 8.2 configure_pyspark.ps1

**Location:** `scripts/ps/configure_pyspark.ps1`

**Purpose:** Configure the Python interpreter and network settings for local PySpark execution.

```powershell
# ------------------------------------------------------------
# Course: Lakehouse Data Pipelines with Spark and dbt
# Script: configure_pyspark.ps1
# Performed by: R. Lisovenko
# Started: 27.10.2026
#
# Description:
# Configure Python and network settings for local PySpark.
# ------------------------------------------------------------

# Resolve the project root relative to this script.
$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path

# Locate the Python executable in the virtual environment.
$pythonExe = Join-Path $projectRoot ".venv\Scripts\python.exe"

# Verify that the Python executable exists.
if (-not (Test-Path $pythonExe)) {
    throw "Python executable not found: $pythonExe"
}

# Configure Python for Spark worker processes.
$env:PYSPARK_PYTHON = $pythonExe

# Use the same Python interpreter for the Spark driver.
$env:PYSPARK_DRIVER_PYTHON = $pythonExe

# Bind Spark to the local loopback interface.
$env:SPARK_LOCAL_IP = "127.0.0.1"

# Verify PySpark configuration.
Write-Host "PYSPARK_PYTHON: $env:PYSPARK_PYTHON"
Write-Host "PYSPARK_DRIVER_PYTHON: $env:PYSPARK_DRIVER_PYTHON"
Write-Host "SPARK_LOCAL_IP: $env:SPARK_LOCAL_IP"
```

**Important:** `$PSScriptRoot` resolves paths relative to the saved `.ps1` file, regardless of the current working directory.

### 8.3 Execute Configuration Scripts

From the project root:

```powershell
# Configure Java.
. .\scripts\ps\configure_java.ps1

# Configure PySpark.
. .\scripts\ps\configure_pyspark.ps1
```

The leading dot followed by a space is called **dot-sourcing**.

It allows PowerShell to execute the scripts in the current session.

**Note:** These environment settings apply to the current PowerShell session. They do not permanently modify Windows environment variables.

---

## 9. PySpark Environment Verification

### 9.1 Verification Script

**File:** `scripts/py/spark_setup_check.py`

**Purpose:**

- Initialize a local SparkSession.
- Verify the installed Spark version.
- Create a test DataFrame.
- Display the processed data.
- Stop Spark and release resources.

### 9.2 Run the Verification

From the project root:

```powershell
# Configure the PySpark environment.
. .\scripts\ps\configure_pyspark.ps1

# Execute the verification script.
python .\scripts\py\spark_setup_check.py
```

Alternatively, from `scripts/ps`:

```powershell
python ..\py\spark_setup_check.py
```

### 9.3 Expected Output

```text
Spark version: 4.2.0

+---+----------+
| id|technology|
+---+----------+
|  1|    Python|
|  2|   PySpark|
|  3| Lakehouse|
+---+----------+

PySpark environment check completed successfully.
```

### 9.4 Verification Results

**Date:** 27.10.2026  
**Status:** Successfully tested

| Component | Result | Status |
|---|---|---|
| Python 3.12.10 | Virtual environment | Passed |
| Java JDK 17.0.20.1 | JVM initialization | Passed |
| PySpark 4.2.0 | SparkSession initialization | Passed |
| Spark DataFrame | Creation and processing | Passed |
| DataFrame.show() | Correct output | Passed |
| SparkSession.stop() | Execution completed | Passed |

**Result:** The local PySpark environment was successfully configured and verified.

---

## 10. Spark Resource Optimization

Apache Spark can consume significant system resources even when processing small datasets.

The following settings are recommended for local development.

### 10.1 CPU Configuration

Default configuration:

```python
.master("local[*]")
```

This allows Spark to use all available logical CPU cores.

Recommended configuration:

```python
.master("local[2]")
```

This limits local Spark task execution to two concurrent threads.

### 10.2 Memory and Partition Configuration

Recommended SparkSession configuration for small exercises:

```python
# Initialize Spark with limited resources for local development.
spark = (
    SparkSession.builder
    .appName("Lakehouse-Setup")
    .master("local[2]")
    .config("spark.driver.memory", "1g")
    .config("spark.sql.shuffle.partitions", "2")
    .getOrCreate()
)
```

**Configuration Details:**

| Parameter | Value | Purpose |
|---|---|---|
| `local[2]` | 2 threads | Limit local task concurrency |
| `spark.driver.memory` | 1 GB | Set driver JVM heap size |
| `spark.sql.shuffle.partitions` | 2 | Reduce shuffle partitions for small datasets |

**Note:** The driver memory setting does not limit total memory consumption across all Spark and Python processes.

These settings are recommendations for future exercises; the verified environment test does not depend on them.

---

## 11. Troubleshooting

### 11.1 Java Is Not Recognized

**Error:**

```text
java: The term 'java' is not recognized
```

**Cause:** Java binaries are missing from the current terminal's PATH.

**Solution:**

```powershell
$env:JAVA_HOME = "C:\dev_soft\Java\jdk-17"
$env:Path = "$env:JAVA_HOME\bin;$env:Path"
```

For a permanent solution, configure JAVA_HOME and Path in Windows environment variables.

### 11.2 Java Gateway Exited

**Error:**

```text
PySparkRuntimeError: [JAVA_GATEWAY_EXITED]
```

**Possible Cause:** Spark cannot start the Java process.

**Solution:** Verify Java installation, JAVA_HOME and PATH.

### 11.3 Python Worker Failed to Connect

**Error:**

```text
Python worker failed to connect back
```

**Observed Cause:**

```text
Python was not found; run without arguments
to install from the Microsoft Store
```

Spark could not locate the correct Python interpreter.

**Solution:**

```powershell
# Configure the project Python interpreter.
. .\scripts\ps\configure_pyspark.ps1
```

The configuration ensures that Spark uses the Python executable from `.venv`.

### 11.4 Incorrect Working Directory

**Error:**

```text
No such file or directory: scripts\py\spark_setup_check.py
```

**Cause:** The command was executed from `scripts/ps` rather than the project root.

**Solution:**

From `scripts/ps`:

```powershell
python ..\py\spark_setup_check.py
```

From the project root:

```powershell
python .\scripts\py\spark_setup_check.py
```

### 11.5 Hadoop Windows Utilities and Parquet Write Limitation

**Environment:** Windows, PySpark 4.2.0, Hadoop Client API 3.5.0.

**Observed behavior:** Local SparkSession initialization, DataFrame processing, and CSV/JSON reading succeeded. Writing a Parquet dataset with Spark failed in this Windows environment because Hadoop Windows utilities were unavailable (`winutils.exe` not found and `HADOOP_HOME` unset).

```text
java.io.FileNotFoundException: HADOOP_HOME and hadoop.home.dir are unset
```

**Verified workaround for this reading exercise:** Generate a single Parquet file using Pandas and PyArrow, then read it using PySpark. Run from the project root:

```powershell
# Create the Parquet file without invoking Hadoop's Windows write utilities.
python -c "import pandas as pd; df = pd.read_csv('data/csv/operations_data.csv'); df.to_parquet('data/parquet/operations_data.parquet', engine='pyarrow', index=False); print('Parquet created successfully')"

# Verify that PySpark reads all three input formats.
python .\scripts\py\read_data_formats.py
```

**Important path distinction:** Spark's `DataFrameWriter.parquet(...)` normally creates a *directory* at the target path, containing one or more `part-*.parquet` files. PyArrow's `DataFrame.to_parquet(...)` creates a *single file* at the target path. A directory left by an unsuccessful Spark write at `data/parquet/operations_data.parquet` must not be confused with the PyArrow output file of the same name. Inspect the path before removing or renaming anything.

**Verified result:** PySpark successfully read CSV, JSON, and the PyArrow-generated Parquet file (6 columns and 5 records each).

**Open limitation:** Writing Parquet *with Spark* on this Windows installation remains unresolved. The workaround validates cross-tool Parquet reading, not Spark's Parquet writer. Do not download unverified `winutils.exe` binaries merely to suppress the warning.

### 11.6 Pandas Compatibility Warning

**Warning:**

```text
PySpark does not yet fully support pandas >= 3.0.0
```

The current environment contains Pandas 3.1.0.

Some Pandas-related PySpark features may not work correctly.

**Recommended Action:** If Pandas integration is needed, install a compatible version below 3.0 and update `requirements.txt` accordingly.

---

### 3.3 PySpark and Py4J Integration

PySpark provides a Python API for Apache Spark.

Py4J is automatically installed as a dependency of PySpark
and enables communication between Python and the Java Virtual
Machine (JVM).

**Architecture:**

Python → PySpark → Py4J → JVM → Apache Spark

**Key Takeaways:**

- PySpark allows developers to use Apache Spark through Python.
- Py4J provides communication between Python and Java objects.
- The Spark engine executes distributed data processing tasks.
- Python worker processes may be used for Python-based operations.

**Installed Versions:**

| Package | Version |
|---|---|
| PySpark | 4.2.0 |
| Py4J | 0.10.9.9 |
| Java | 17.0.20.1 |

**Verification:**

    python -m pip show pyspark
    python -m pip show py4j

### 7.1 Python Dependencies

Python dependencies are managed through `requirements.txt`.

**Course example (Edureka):**

```text
py4j==0.10.9.9
pyspark==4.2.0

```
python ..\py\spark_setup_check.py 
```

### 1.3.4 Reading CSV, JSON, and Parquet with PySpark

#### Overview

This lesson introduces reading structured and semi-structured data from different file formats using Apache Spark.

PySpark provides the `spark.read` interface for loading data into Spark DataFrames.

```
python .\scripts\py\read_data_formats.py
```

```
    data/
    ├── csv/
    │   └── operations_data.csv
    ├── json/
    │   └── operations_data.json
    └── parquet/

    output/

    scripts/
    ├── create_parquet_data.py
    └── read_data_formats.py
```

#### Supported File Formats

| Format  | Description                                         | PySpark Method         |
| ------- | --------------------------------------------------- | ---------------------- |
| CSV     | Text-based tabular data                             | `spark.read.csv()`     |
| JSON    | Structured and semi-structured data                 | `spark.read.json()`    |
| Parquet | Column-oriented data format optimized for analytics | `spark.read.parquet()` |

#### Learning Objectives

1. Read CSV, JSON, and Parquet files using PySpark.
2. Understand the differences between file formats.
3. Load data into Spark DataFrames.
4. Inspect DataFrame schemas and contents.
5. Prepare data for further processing and transformations.

#### Basic Syntax

**CSV:**

```python
df_csv = spark.read.csv(
    "data/sample.csv",
    header=True,
    inferSchema=True
)
```

**JSON:**

```python
df_json = spark.read.json("data/sample.json")
```

**Parquet:**

```python
df_parquet = spark.read.parquet("data/sample.parquet")
```

#### Key Concepts

- **DataFrame:** A distributed collection of structured data.
- **Schema:** Defines column names and data types.
- **Schema Inference:** Automatically determines data types from source data.
- **Columnar Storage:** Stores data by columns, improving efficiency for many analytical workloads.

**Practical Exercise:** Completed — 27.10.2026.

**Verified result:** CSV, JSON, and Parquet were read successfully through PySpark; each DataFrame contained 6 columns and 5 records. The Parquet input was generated with Pandas/PyArrow because Spark's Parquet writer was blocked by the Windows Hadoop utilities configuration (see Section 11.5).

**Next Step:** Continue Module 1 with the next PySpark lesson.





---
## 12. Course Project

### Building an Orchestrated Batch Lakehouse Pipeline

The course project integrates PySpark, dbt Core, Apache Airflow, MinIO, and Apache Iceberg into an end-to-end batch data pipeline.

### Planned Workflow

```text
Source Data
    |
    v
PySpark Processing
    |
    v
dbt Transformation
    |
    v
Airflow Orchestration
    |
    v
MinIO / Apache Iceberg
```

### Project Objectives

1. Process source datasets using PySpark.
2. Perform analytical transformations using dbt Core.
3. Orchestrate pipeline execution using Apache Airflow.
4. Explore lakehouse storage using MinIO and Apache Iceberg.
5. Build a reproducible local development environment.

**Status:** Not Started

---

## 13. Progress Tracking

| Date | Module / Activity | Status | Result |
|---|---|---|---|
| 27.10.2026 | Course initialization | Completed | Project structure created |
| 27.10.2026 | Python 3.12 virtual environment | Completed | `.venv` configured |
| 27.10.2026 | Java JDK 17 installation | Completed | Java verified |
| 27.10.2026 | PySpark installation | Completed | PySpark 4.2.0 installed |
| 27.10.2026 | PowerShell configuration scripts | Completed | Java and PySpark configuration prepared |
| 27.10.2026 | SparkSession verification | Completed | Spark initialized successfully |
| 27.10.2026 | DataFrame processing test | Completed | Test DataFrame displayed |
| 27.10.2026 | Read CSV, JSON, and Parquet with PySpark | Completed | 6 columns and 5 records in each format; Parquet created with PyArrow |
| 27.10.2026 | Spark Parquet write on Windows | Open issue | Missing Hadoop Windows utilities; PyArrow workaround documented in Section 11.5 |
| 27.10.2026 | Module 1 — Distributed Processing with PySpark | In Progress | Environment ready |
| — | Module 2 — Transformation Engineering with dbt | Not Started | — |
| — | Module 3 — Orchestration and Lakehouse Foundations | Not Started | — |
| — | Course Project | Not Started | — |
| — | Final Assessment / Certificate | Pending | — |

---

## 14. Current Status

**Last Updated:** 27.10.2026

The local development environment has been successfully configured.

**Completed:**

- Python 3.12.10 installation and virtual environment configuration.
- Eclipse Temurin JDK 17 installation.
- Permanent JAVA_HOME and PATH configuration.
- PySpark 4.2.0 installation.
- PowerShell configuration scripts.
- Successful SparkSession initialization.
- Successful DataFrame processing and verification.
- Successful reading and comparison of CSV, JSON, and Parquet with PySpark (5 records each).
- PyArrow-based Parquet generation documented as a workaround for the unresolved Windows Spark-write issue.

**Next Step:** Continue Module 1 — Distributed Processing with PySpark.

---

**Performed by:** R. Lisovenko  
**Course:** Lakehouse Data Pipelines with Spark and dbt  
**Specialization:** Data Engineering with Open Source Tools