# Data Engineering Course

Practical exercises and notes for the Coursera course **Data Engineering Foundations with SQL and reporting system**.

## Executor
    - LiR
    - Created: 12-10-2026

## Project Structure

- `data/` — source datasets
- `docs/` — documentation and notes
- `notebooks/` — Jupyter notebooks
- `output/` — processed results
- `scripts/ps/` — PowerShell scripts
- `scripts/py/` — Python scripts
- `scripts/sql/` — SQL scripts
DataEng/
├─ data/
├─ docs/
├─ notebooks/
├─ output/
├─ scripts/
│  ├─ ps/
│  ├─ py/
│  └─ sql/
├─ requirements.txt
└─ README.md

## WorkSpace
    - Python Version : 3.14.6
    - Pandas Version : 3.0.6
    - Git Version    : git version 2.55.0.windows.5
    - PostgreSQL     : psql (PostgreSQL) 17.11

## PostgreSQL Commands

### Connect to PostgreSQL

- powershell 
```
  psql -U postgres
  CREATE DATABASE retail_db;
  \l
```
##### — switch retail_db

```
\с retail_db                
```

02_Relational-Database/
└─ scripts/
   └─ sql/
      └─ retail_db_setup.sql
##### Run SQL-sript in PostgreSQL
   - psql -U postgres -f scripts\sql\retail_db_setup.sql

- view tabl and Type columns
```
    \dt
    \d sales
```
```
CREATE TABLE sales (
    order_id INTEGER PRIMARY KEY,
    customer_name VARCHAR(100),
    product VARCHAR(100),
    quantity INTEGER,
    unit_price NUMERIC(10,2),
    order_date DATE
);
```
```
SELECT * FROM sales;
```

```
INSERT INTO sales
(order_id, customer_name, product, quantity, unit_price, order_date)
VALUES
(1001, 'Alice Johnson', 'Laptop', 1, 75000.00, '2026-08-01'),
(1002, 'Rahul Sharma', 'Mouse', 2, 800.00, '2026-08-02'),
(1003, 'Priya Nair', 'Keyboard', 1, 1500.00, '2026-08-02');
```


## Related Other Completed Courses and Learning

### DataEngineering
 - Performed by: R. Lisovenko
 - Created: 02-10-2026

 Educational materials, exercises, and practical tasks in data engineering, including SQL, PostgreSQL, data pipelines, data quality, ETL, batch processing, and streaming concepts.

### DataScience

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

