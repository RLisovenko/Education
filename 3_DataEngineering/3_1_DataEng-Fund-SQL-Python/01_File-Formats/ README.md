# Data Engineering Course

Practical exercises and notes for the Coursera course **Data Engineering Foundations with SQL and Python**.

## Executor
    - LiR
    - Created: 01-10-2026

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
    

## Topics

- Data engineering fundamentals
- CSV, JSON, Parquet
- PostgreSQL and SQL
- Data validation and cleaning
- Data pipelines
- Incremental loading and idempotency
- Git and GitHub.


### CSV, JSON, AND PARQUET FILE INSPECTION

#### CSV FORMAT
    - Shape(rows, columns): (5, 8)
    - Columns:
    - ['order_id', 'customer_name', 'product', 'category', 'quantity', 'unit_price', 'city', 'order_date']

#### Data Types:
    - order_id         int64
    - customer_name      str
    - product            str    
    - category           str
    - quantity         int64
    - unit_price       int64
    - city               str
    - order_date         str
    - dtype: object

### JSON FORMAT

#### Shape(rows, columns): (5, 8)

##### Columns:
    - ['order_id', 'customer_name', 'product', 'category', 'quantity', 'unit_price', 'city', 'order_date']

#### Data Types:
    - order_id         int64
    - customer_name      str
    - product            str
    - category           str
    - quantity         int64
    - unit_price       int64
    - city               str
    - order_date         str
    - dtype: object

#### PARQUET FORMAT
##### Shape(rows, columns): (5, 8)
##### Columns:
    - ['order_id', 'customer_name', 'product', 'category', 'quantity', 'unit_price', 'city', 'order_date']

##### Data Types:
    - order_id                  int64
    - customer_name               str
    - product                     str
    - category                    str
    - quantity                  int64
    - unit_price                int64
    - city                        str
    - order_date       datetime64[us]

#####  dtype: object
| order_id | customer_name | product | category | quantity | unit_price | city | order_date |
|---:|---|---|---|---:|---:|---|---|
| 1001 | Alice Johnson | Laptop | Electronics | 1 | 75000 | Bengaluru | 2026-08-01 |
| 1002 | Rahul Sharma | Mouse | Accessories | 2 | 800 | Mumbai | 2026-08-02 |
| 1003 | Priya Nair | Keyboard | Accessories | 1 | 1500 | Chennai | 2026-08-02 |
| 1004 | John Thomas | Monitor | Electronics | 2 | 18000 | Hyderabad | 2026-08-03 |
| 1005 | Sneha Patel | Webcam | Accessories | 3 | 2500 | Pune | 2026-08-04 |
- 4      1005    Sneha Patel    Webcam  Accessories         3        2500       Pune 2026-08-04


### FOLDER CONTENTS: data

    - data\csv\sales_data.csv
    - data\json\sales_data.json
    - data\parquet\sales_data.parquet
    - data\processed\processed_sales.csv
    - data\raw\sales_data.csv

##### FORMAT COMPARISION SUMMARY


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

