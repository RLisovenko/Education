# Data Engineering Course

Practical exercises and notes for the Coursera course **Data Engineering Foundations with SQL and Python**, including data formats, PostgreSQL, SQL, relational databases, and reporting-oriented data workflows.

# Reliable-Data-Pipelines-and-Quality

-
```text
Data Quality
    ↓
Clear Workflow
    ↓
Validation
    ↓
Error Handling
    ↓
Reliable Data
```

## Executor

- Performed by: R. Lisovenko
- Created: 19-10-2026

## Scenario

GlobalMart receives a CSV file every morning from its online sales system.

Before analysts can use the data, the engineering team must:

1. Receive the source file.
2. Create the destination table.
3. Load the file into PostgreSQL.
4. Verify that every record has been imported.
5. Confirm that there are no duplicate order IDs.

## Database

## PostgreSQL Connection

- Activate the Python virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
```

- Connect to PostgreSQL:

```powershell
psql -U postgres
```

- Enter the PostgreSQL password when prompted.

- Connect to the project database:

```text
\c retail_db
```

- After a successful connection, the prompt should look like:

```text
retail_db=#
```

- Check the current database:

```sql
SELECT current_database();
```

- List available tables:

```text
\dt
```

- Exit PostgreSQL:

```text
\q
```
## Create Destination Table

- Creates the `sales_orders` table for loading data from the source CSV file.

```sql
CREATE TABLE sales_orders (
    order_id INTEGER,
    customer_name VARCHAR(100),
    product VARCHAR(100),
    quantity INTEGER,
    unit_price NUMERIC(10,2),
    order_date DATE
);
```

- Verify that the table was created:

```text
\dt
```

- View the table structure:

```text
\d sales_orders
```

- Loads data from the local CSV file into the PostgreSQL `sales_orders` table.
- `CSV HEADER` skips the first row containing column names.

```text
\copy sales_orders FROM 'data/raw/sales_orders.csv' DELIMITER ',' CSV HEADER;
```
```sql
SELECT COUNT(*)
FROM sales_orders;
```
```sql
SELECT *
FROM sales_orders
ORDER BY order_id;
```

- Verifies that all rows were loaded and checks that every record has a populated `order_id`.
- `COUNT(*)` counts all rows, while `COUNT(order_id)` counts only non-NULL `order_id` values.

```sql
SELECT
    COUNT(*) AS total_rows,
    COUNT(order_id) AS populated_order_ids
FROM sales_orders;
```
- Checks the `sales_orders` table for duplicate `order_id` values.
- `GROUP BY order_id` groups identical order IDs, and `HAVING COUNT(*) > 1` returns only duplicates.

```sql
SELECT
    order_id,
    COUNT(*) AS duplicate_count
FROM sales_orders
GROUP BY order_id
HAVING COUNT(*) > 1;
```

Expected result:

```text
(0 rows)
```

- `0 rows` means no duplicate `order_id` values were found.

- Calculates the total sales value of all imported orders.
- `quantity * unit_price` calculates the value of each order, and `SUM(...)` adds all order values together.

```sql
SELECT
    SUM(quantity * unit_price) AS total_sales_value
FROM sales_orders;
```

Expected result:

```text
total_sales_value
-----------------
222500.00
```



## Project Structure

- `data/` — source datasets
- `docs/` — documentation and notes
- `notebooks/` — Jupyter notebooks
- `output/` — processed results
- `scripts/ps/` — PowerShell scripts
- `scripts/py/` — Python scripts
- `scripts/sql/` — SQL scripts

```text
05_Reliable-Data-Pipelines-and-Quality/
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