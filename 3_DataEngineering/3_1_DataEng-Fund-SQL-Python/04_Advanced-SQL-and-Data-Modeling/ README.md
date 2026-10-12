# Data Engineering Course 

Practical exercises and notes for the Coursera course **Data Engineering Foundations with SQL and Python**, including data formats, PostgreSQL, SQL, relational databases, and reporting-oriented data workflows.

## 04_Advanced-SQL-and-Data-Modeling
    - NULL
    - Data Types
    - Defensive SQL
    - JOIN
    - CTE
    - Window Functions
    - Data Modeling

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
04_Advanced-SQL-and-Data-Modeling/
├─ data/
├─ docs/
├─ notebooks/
├─ output/
├─ scripts/
│  ├─ ps/
│  ├─ py/
│  └─ sql/
├─ README.md
├─ Scenario
└─ requirements.txt

```
```text
scripts/sql/
├─ nulls_and_types.sql
├─ joins_and_metrics.sql
└─ cte_and_window_functions.sql
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


```

### View Tables

```text
\dt
```

### View Table Structure and Column Types

```text
\d sales
```

```
select * from sales;
```
- Create tbl customers
```
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    customer_name VARCHAR(100),
    city VARCHAR(50)
);
```
- view Column Type customers 
```
\d customers
```

```
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    product VARCHAR(100),
    quantity INTEGER,
    unit_price NUMERIC(10,2),
    order_date DATE,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
```
```
\d orders
```
```
SELECT *
FROM customers
ORDER BY customer_id;
```
- Clear tables
```
TRUNCATE TABLE orders, customers;
```

```
INSERT INTO customers
(customer_id, customer_name, city)
VALUES
(1, 'Alice Johnson', 'Bengaluru'),
(2, 'Rahul Sharma', 'Mumbai'),
(3, 'Priya Nair', 'Chennai'),
(4, 'John Thomas', 'Hyderabad'),
(5, 'Sneha Patel', 'Pune'),
(6, 'Rohan Verma', 'Delhi');
```
```
SELECT *
FROM customers;
```

```
INSERT INTO orders
(order_id, customer_id, product, quantity, unit_price, order_date)
VALUES
(101, 1, 'Laptop', 1, 75000.00, '2026-08-01'),
(102, 2, 'Mouse', 2, 800.00, '2026-08-02'),
(103, 3, 'Keyboard', 1, 1500.00, '2026-08-02'),
(104, 1, 'Monitor', 2, 18000.00, '2026-08-03'),
(105, 5, 'Webcam', 3, 2500.00, '2026-08-04');
```

```
SELECT *
FROM orders;
```

```
SELECT
    c.customer_name,
    c.city,
    o.product,
    o.quantity,
    o.unit_price
FROM customers c
INNER JOIN orders o
ON c.customer_id = o.customer_id;

```

```
SELECT
    c.customer_name,
    c.city,
    o.product,
    o.quantity,
    o.unit_price
FROM customers c
LEFT JOIN orders o
ON c.customer_id = o.customer_id;

```

#-------------------------------------------------------------------
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