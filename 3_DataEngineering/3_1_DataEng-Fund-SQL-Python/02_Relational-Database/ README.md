# Data Engineering Course

Practical exercises and notes for the Coursera course **Data Engineering Foundations with SQL and Python**, including data formats, PostgreSQL, SQL, relational databases, and reporting-oriented data workflows.

## Executor

- Performed by: R. Lisovenko
- Created: 12-10-2026

## Project Structure

- `data/` — source datasets
- `docs/` — documentation and notes
- `notebooks/` — Jupyter notebooks
- `output/` — processed results
- `scripts/ps/` — PowerShell scripts
- `scripts/py/` — Python scripts
- `scripts/sql/` — SQL scripts

```text
02_Relational-Database/
├─ data/
├─ docs/
├─ notebooks/
├─ output/
├─ scripts/
│  ├─ ps/
│  ├─ py/
│  └─ sql/
│     └─ retail_db_setup.sql
├─ .gitignore
├─ requirements.txt
├─ README.md
└─ Scenario
```

## Workspace

- Python Version: 3.14.6
- Pandas Version: 3.0.6
- Git Version: 2.55.0.windows.5
- PostgreSQL: 17.11

## PostgreSQL Commands

### Connect to PostgreSQL

```powershell
psql -U postgres
```

### Create Database

```sql
CREATE DATABASE retail_db;
```

### List Databases

```text
\l
```

### Connect to `retail_db`

```text
\c retail_db
```

After connecting, the `psql` prompt changes to:

```text
retail_db=#
```

### Create the `sales` Table

```sql
CREATE TABLE sales (
    order_id INTEGER PRIMARY KEY,
    customer_name VARCHAR(100),
    product VARCHAR(100),
    quantity INTEGER,
    unit_price NUMERIC(10,2),
    order_date DATE
);
```

### View Tables

```text
\dt
```

### View Table Structure and Column Types

```text
\d sales
```

### Insert Sample Data

```sql
INSERT INTO sales
(order_id, customer_name, product, quantity, unit_price, order_date)
VALUES
(1001, 'Alice Johnson', 'Laptop', 1, 75000.00, '2026-08-01'),
(1002, 'Rahul Sharma', 'Mouse', 2, 800.00, '2026-08-02'),
(1003, 'Priya Nair', 'Keyboard', 1, 1500.00, '2026-08-02');
```

### View All Records

```sql
SELECT * FROM sales;
```

### Example Filtered Query

```sql
SELECT *
FROM sales
WHERE unit_price > 1000;
```

## PostgreSQL SQL Script

The PostgreSQL setup commands are also stored in:

```text
02_Relational-Database/
└─ scripts/
   └─ sql/
      └─ retail_db_setup.sql
```

### Run SQL Script in PostgreSQL

From the `02_Relational-Database` project directory:

```powershell
psql -U postgres -f scripts\sql\retail_db_setup.sql
```

The script creates the database and table, inserts sample records, and runs basic inspection queries.

## PostgreSQL Authentication Configuration

PostgreSQL client authentication is configured in:

```text
C:\Program Files\PostgreSQL\17\data\pg_hba.conf
```

Standard local authentication:

```text
host    all    all    127.0.0.1/32    scram-sha-256
host    all    all    ::1/128         scram-sha-256
```

For temporary local password recovery, authentication can be changed to:

```text
host    all    all    127.0.0.1/32    trust
host    all    all    ::1/128         trust
```

Restart PostgreSQL from Administrator PowerShell:

```powershell
Restart-Service postgresql-x64-17
```

Connect locally:

```powershell
psql -h 127.0.0.1 -U postgres
```

Set a new password:

```sql
ALTER USER postgres WITH PASSWORD 'NEW_PASSWORD';
```

Exit `psql`:

```text
\q
```

After changing the password, restore secure authentication:

```text
host    all    all    127.0.0.1/32    scram-sha-256
host    all    all    ::1/128         scram-sha-256
```

Restart PostgreSQL again:

```powershell
Restart-Service postgresql-x64-17
```

## Related Other Completed Courses and Learning

### Data Engineering

- Performed by: R. Lisovenko
- Created: 02-10-2026

Educational materials, exercises, and practical tasks in Data Engineering, including SQL, PostgreSQL, data pipelines, data quality, ETL, batch processing, streaming concepts, file formats, and relational databases.

### Data Science

- 🔗 [Data Science](https://github.com/RLisovenko/Python/tree/Python/edu/DataScience)
- 🔗 [Data Science AI Development](https://github.com/RLisovenko/Python/tree/Python/edu/DataScience-AI-Dev)

Educational materials, exercises, and practical tasks in data analysis, pandas, Jupyter notebooks, statistics, AI development, and Data Science workflows.

### Python

- 🔗 [Python Repository](https://github.com/RLisovenko/Python)

Educational materials and practical exercises in Python programming, automation, data processing, scripting, and backend-related development.

### SQL

- 🔗 [SQL, Data Science & Python](https://github.com/RLisovenko/Databases/tree/db/edu-SQL-DataScience-Python)
- 🔗 [Databases Repository](https://github.com/RLisovenko/Databases)

Educational materials and practical exercises in SQL, relational databases, data modeling, querying, joins, aggregations, and analytical SQL.

### DevOps

Educational materials and practical exercises in Git, GitHub, CI/CD, containers, automation, infrastructure, and DevOps workflows.

### Certificates

- 🔗 [Certificates](https://github.com/RLisovenko/Education/tree/main/Certificates)
- 📄 [Databases, SQL, Data Science & Python](https://github.com/RLisovenko/Education/blob/main/Certificates/Databases_SQL_DataScience_Python.pdf)
- 📄 [DevOps Introduction](https://github.com/RLisovenko/Education/blob/main/Certificates/DevOps_Introduction.pdf)
- 📄 [Python Data Science AI Development](https://github.com/RLisovenko/Education/blob/main/Certificates/PythonDataScience_AI_Development.pdf)
- 📄 [Python Data Science](https://github.com/RLisovenko/Education/blob/main/Certificates/Python_Data_Science.pdf)

Certificates and records of completed courses, specializations, and professional learning programs.