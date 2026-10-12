# Data Engineering Course

Practical exercises and notes for the Coursera course **Data Engineering Foundations with SQL and Python**, including data formats, PostgreSQL, SQL, relational databases, and reporting-oriented data workflows.

# SQL Queries and Aggregations

Practical SQL exercises for analyzing sales data stored in PostgreSQL.

## Executor

- Performed by: R. Lisovenko
- Created: 12-10-2026

## Scenario

A retail team stores customer orders in PostgreSQL and needs quick answers about sales performance.

Using SQL, the `sales` table can be explored to:

- identify high-value products
- calculate order statistics
- find unique products
- summarize sales by product
- generate useful business insights from transactional data

## Database

This lab continues working with the existing PostgreSQL database:


```text
Database: retail_db
Table: sales

## Project Structure

- `data/` — source datasets
- `docs/` — documentation and notes
- `notebooks/` — Jupyter notebooks
- `output/` — processed results
- `scripts/ps/` — PowerShell scripts
- `scripts/py/` — Python scripts
- `scripts/sql/` — SQL scripts

```text
03_SQL-Queries-and-Aggregations/
├─ data/
├─ docs/
├─ notebooks/
├─ output/
├─ scripts/
│  ├─ ps/
│  ├─ py/
│  └─ sql/
│     └─ sales_analysis.sql
├─ .gitignore
├─ README.md
├─ requirements.txt
└─ Scenario
```

The sales table contains:
```
    order_id
    customer_name
    product
    quantity
    unit_price
    order_date
```

```
INSERT INTO sales
(order_id, customer_name, product, quantity, unit_price, order_date)
VALUES
-- (1001, 'Alice Johnson', 'Laptop', 1, 75000.00, '2026-08-01'),
-- (1002, 'Rahul Sharma', 'Mouse', 2, 800.00, '2026-08-02'),
-- (1003, 'Priya Nair', 'Keyboard', 1, 1500.00, '2026-08-02'),
(1004, 'John Thomas', 'Monitor', 2, 18000.00, '2026-08-03'),
(1005, 'Sneha Patel', 'Webcam', 3, 2500.00, '2026-08-04'),
(1006, 'Arjun Mehta', 'Laptop', 1, 72000.00, '2026-08-05'),
(1007, 'Neha Kapoor', 'Mouse', 4, 850.00, '2026-08-05'),
(1008, 'Karan Singh', 'Keyboard', 2, 1600.00, '2026-08-06');

```
```
SELECT * FROM sales ORDER BY order_id;
```

```
select order_id, customer_name, product from sales
```

## Workspace

- Python Version: 3.14.6
- Pandas Version: 3.0.6
- Git Version: 2.55.0.windows.5
- PostgreSQL: 17.11

## SQL Topics
    This lab focuses on:
    - SELECT
    - WHERE
    - DISTINCT
    - COUNT
    - SUM
    - AVG
    - MIN
    - MAX
    - GROUP BY
    - ORDER BY

Connect to PostgreSQL
``` 
    psql -U postgres 
```

Connect to the existing database:
```
    \c retail_db
```

View Existing Data
```
    SELECT * FROM sales;
```

SQL queries for this lab are stored in:
```
scripts/sql/sales_analysis.sql
```

Run the script from the project directory:
```
psql -U postgres -d retail_db -f scripts\sql\sales_analysis.sql
```

### SQl command

    SELECT / ORDER BY
    WHERE
    TOP 3 + LIMIT
    DISTINCT
    COUNT / SUM / AVG / MIN / MAX
    GROUP BY
    SUM(quantity * unit_price)
    ORDER BY aggregated value

```
select * From sales WHERE unit_price > 5000;  
```

```
select order_id,customer_name, product, unit_price 
From sales 
Order by  unit_price DESC;  --ASC
```

```
SELECT order_id, customer_name, product, unit_price
FROM sales
ORDER BY unit_price DESC
LIMIT 3;
```
```
SELECT DISTINCT product
FROM sales;
```

```
SELECT
    COUNT(*) AS total_orders,
    SUM(quantity) AS total_quantity,
    AVG(unit_price) AS average_unit_price,
    MIN(unit_price) AS minimum_unit_price,
    MAX(unit_price) AS maximum_unit_price
FROM sales;
```

```
/*
    1. `quantity * unit_price` — calculates the value of each order line.  
    2. `SUM(...)` — calculates the total sales value for each product.  
    3. `GROUP BY product` — groups rows that contain the same product.  
    4. `ORDER BY total_sales_value DESC` — sorts products from the highest to the lowest total sales value.
*/
SELECT
    product,
    SUM(quantity * unit_price) AS total_sales_value
FROM sales
GROUP BY product
ORDER BY total_sales_value DESC;
```

## Goal
    The goal of this lab is to use SQL to transform stored transactional sales data into useful summaries, statistics, and business insights.

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