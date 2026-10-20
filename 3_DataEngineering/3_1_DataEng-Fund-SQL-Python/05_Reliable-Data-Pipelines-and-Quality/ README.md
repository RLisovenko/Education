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
# Scenario 2: Validating Data Quality in PostgreSQL
- Creates the `sales_quality` table for loading and validating a new batch of sales transactions.
- The table stores order details that will be checked for missing values, duplicates, and invalid numeric data.

```sql
CREATE TABLE sales_quality (
    order_id INTEGER,
    customer_name VARCHAR(100),
    product VARCHAR(100),
    quantity INTEGER,
    unit_price NUMERIC(10,2),
    order_date DATE
);
```

- Displays the structure of the `sales_quality` table, including column names and data types.

```text
\d sales_quality
```

- Loads the CSV file into the `sales_quality` table for data-quality validation.
- `CSV HEADER` skips the first row with column names.

```
\copy sales_quality FROM 'data/raw/sales_orders_quality.csv' DELIMITER ',' CSV HEADER;
```

Expected result:

```text
COPY 8
```

- `COPY 8` means that 8 records were successfully loaded into PostgreSQL.

## Validate Loaded Records

- Counts all rows loaded into the `sales_quality` table.

```sql
SELECT COUNT(*) AS total_rows
FROM sales_quality;
```

Expected result:

```text
total_rows
----------
8
```

- Displays all loaded records for manual verification.

```sql
SELECT *
FROM sales_quality
ORDER BY order_id;
```


- Checks how many records have a populated `order_id`.

```sql
SELECT
    COUNT(*) AS total_rows,
    COUNT(order_id) AS populated_order_ids
FROM sales_quality;
```

Expected result:

```text
total_rows | populated_order_ids
-----------+--------------------
8          | 8
```

- Checks for missing or empty customer names in the `sales_quality` table.
- `IS NULL` finds missing values, while `= ''` finds empty text values.

```sql
SELECT *
FROM sales_quality
WHERE customer_name IS NULL
   OR customer_name = '';
```

Expected result:

```text
order_id | customer_name | product | quantity | unit_price | order_date
---------+---------------+---------+----------+------------+------------
3004     |               | Monitor | 2        | 18000.00   | 2026-08-03
```

- Checks for missing or empty product values in the `sales_quality` table.
- `IS NULL` finds missing values, while `= ''` finds empty text values.

```sql
SELECT *
FROM sales_quality
WHERE product IS NULL
   OR product = '';
```

Expected result:

```text
order_id | customer_name | product | quantity | unit_price | order_date
---------+---------------+---------+----------+------------+------------
3007     | Neha Kapoor   |         | 4        | 850.00     | 2026-08-05
```

- Checks for duplicate `order_id` values in the `sales_quality` table.
- `GROUP BY order_id` groups identical IDs, while `HAVING COUNT(*) > 1` returns only duplicated orders.

```sql
SELECT
    order_id,
    COUNT(*) AS duplicate_count
FROM sales_quality
GROUP BY order_id
HAVING COUNT(*) > 1;
```

Expected result:

```text
order_id | duplicate_count
---------+----------------
3002     | 2
```

- Checks for invalid `quantity` values in the `sales_quality` table.
- `quantity <= 0` finds records where the quantity is zero or negative.

```sql
SELECT *
FROM sales_quality
WHERE quantity <= 0;
```

Expected result:

```text
order_id | customer_name | product | quantity | unit_price | order_date
---------+---------------+---------+----------+------------+------------
3005     | Sneha Patel   | Webcam  | 0        | 2500.00    | 2026-08-04
```

- Checks for invalid `unit_price` values in the `sales_quality` table.
- `unit_price <= 0` finds records where the price is zero or negative.

```sql
SELECT *
FROM sales_quality
WHERE unit_price <= 0;
```

Expected result:

```text
order_id | customer_name | product | quantity | unit_price | order_date
---------+---------------+---------+----------+------------+------------
3006     | Arjun Mehta   | Laptop  | 1        | -72000.00  | 2026-08-05
```

- Performs a completeness check for key text fields in the `sales_quality` table.
- `NULLIF(column, '')` converts empty strings to `NULL`.
- `COUNT(...)` counts only non-NULL values, so it shows how many valid customer names and products are present.

```sql
SELECT
    COUNT(*) AS total_records,
    COUNT(NULLIF(customer_name, '')) AS valid_customer_names,
    COUNT(NULLIF(product, '')) AS valid_products
FROM sales_quality;
```
```sql
select * from sales_quality;
```
Expected result:

```text
total_records | valid_customer_names | valid_products
--------------+----------------------+---------------
8             | 7                    | 7
```

- Counts how many duplicated `order_id` groups exist in the `sales_quality` table.
- The inner query finds duplicated order IDs, and the outer `COUNT(*)` counts how many duplicate groups were found.

```sql
SELECT
    COUNT(*) AS duplicate_records
FROM (
    SELECT order_id
    FROM sales_quality
    GROUP BY order_id
    HAVING COUNT(*) > 1
) duplicates;
```

Expected result:

```text
duplicate_records
-----------------
1
```

- Performs a summary data-quality check using conditional aggregation.
- `CASE WHEN` converts each detected issue into `1`, and `SUM(...)` counts the total number of issues for each validation rule.

```sql
SELECT
    SUM(CASE WHEN customer_name IS NULL OR customer_name = '' THEN 1 ELSE 0 END) AS missing_customer_names,
    SUM(CASE WHEN product IS NULL OR product = '' THEN 1 ELSE 0 END) AS missing_products,
    SUM(CASE WHEN quantity <= 0 THEN 1 ELSE 0 END) AS invalid_quantity,
    SUM(CASE WHEN unit_price <= 0 THEN 1 ELSE 0 END) AS invalid_price
FROM sales_quality;
```

## Scenario 3 → Cleaning and Preparing Data for Analysis

## Create Cleaned Sales Table

- Creates the `sales_cleaned` table for storing corrected and standardized sales records.
- This table will contain data after cleaning missing values, duplicates, invalid quantities, negative prices, and inconsistent formatting.

```sql
CREATE TABLE sales_cleaned (
    order_id INTEGER,
    customer_name VARCHAR(100),
    product VARCHAR(100),
    quantity INTEGER,
    unit_price NUMERIC(10,2),
    order_date DATE
);
```

- Verify the table structure:

```text
\d sales_cleaned
```

- Loads the raw cleaning dataset into the `sales_cleaned` table.
- The file intentionally contains missing values, duplicate rows, invalid numeric values, and inconsistent text formatting for cleaning practice.

```text
\copy sales_cleaned FROM 'data/raw/sales_orders_cleaning.csv' DELIMITER ',' CSV HEADER;
```

Expected result:

```text
COPY 8
```

- Displays all imported records for review.

```sql
SELECT *
FROM sales_cleaned
ORDER BY order_id;
```
```text
    4002 → missing customer_name
    4003 → quantity = 0
    4004 → negative unit_price
    4005 → missing product
    4006 → duplicate order
    4001 / 4007 → inconsistent lowercase names
```
- Replaces missing or empty customer names with a standard placeholder value.
- `UPDATE` modifies only records where `customer_name` is `NULL` or an empty string.

```sql
UPDATE sales_cleaned
SET customer_name = 'Unknown Customer'
WHERE customer_name IS NULL
   OR customer_name = '';
```

Expected result:

```text
UPDATE 1
```

- Verifies that missing customer names were successfully replaced with the standard value `Unknown Customer`.

```sql
SELECT *
FROM sales_cleaned
WHERE customer_name = 'Unknown Customer';
```

Expected result:

```text
1 row
```

- Replaces missing or empty product values with the standard placeholder `Unknown Product`.
- The update affects only rows where `product` is `NULL` or an empty string.

```sql
UPDATE sales_cleaned
SET product = 'Unknown Product'
WHERE product IS NULL
   OR product = '';
```

Expected result:

```text
UPDATE 1
```

```sql
SELECT *
FROM sales_cleaned
WHERE product = 'Unknown Product';
```
- Corrects invalid `quantity` values by replacing zero or negative quantities with `1`.
- The follow-up query verifies that no invalid quantity values remain.

```sql
UPDATE sales_cleaned
SET quantity = 1
WHERE quantity <= 0;
```

Expected result:

```text
UPDATE 1
```

```sql
SELECT *
FROM sales_cleaned
WHERE quantity <= 0;
```

Expected result:

```text
0 rows
```

- Corrects negative `unit_price` values by converting them to positive values with `ABS()`.
- The follow-up query verifies that no negative prices remain.

```sql
UPDATE sales_cleaned
SET unit_price = ABS(unit_price)
WHERE unit_price < 0;
```

Expected result:

```text
UPDATE 1
```

```sql
SELECT *
FROM sales_cleaned
WHERE unit_price < 0;
```

Expected result:

```text
0 rows
```

- Cleans customer names by removing leading and trailing spaces with `TRIM()`.
- `INITCAP()` converts each word to title case.

- `TRIM()` — removes leading and trailing spaces from a text value.
- `INITCAP()` — capitalizes the first letter of each word and converts the remaining letters to lowercase.

```sql
UPDATE sales_cleaned
SET customer_name = INITCAP(TRIM(customer_name));
```

- Verify the cleaned customer names:

```sql
SELECT
    order_id,
    customer_name
FROM sales_cleaned
ORDER BY order_id;
```
- Removes duplicate records from `sales_cleaned` while keeping one row for each `order_id`.
- `ctid` is PostgreSQL's internal row identifier.
- `MIN(ctid)` keeps one physical row from each duplicate group, and the other duplicates are deleted.

```sql
DELETE FROM sales_cleaned
WHERE ctid NOT IN (
    SELECT MIN(ctid)
    FROM sales_cleaned
    GROUP BY order_id
);
```

Expected result:

```text
DELETE 1
```

- Verifies that no duplicate `order_id` values remain.

```sql
SELECT
    order_id,
    COUNT(*) AS duplicate_count
FROM sales_cleaned
GROUP BY order_id
HAVING COUNT(*) > 1;
```

Expected result:

```text
0 rows
```

## Final Cleaned Dataset

- Displays the cleaned and standardized dataset after all data-quality corrections.

```sql
SELECT *
FROM sales_cleaned
ORDER BY order_id;
```

- After cleaning, the dataset contains 7 valid records with corrected missing values, numeric values, text formatting, and duplicate removal.

- Performs a final completeness check on the cleaned dataset.
- `COUNT(*)` counts all records.
- `NULLIF(column, '')` treats empty strings as `NULL`, so `COUNT(...)` counts only valid non-empty values.

```sql
SELECT
    COUNT(*) AS total_records,
    COUNT(NULLIF(customer_name, '')) AS valid_customer_names,
    COUNT(NULLIF(product, '')) AS valid_products
FROM sales_cleaned;
```

Expected result:

```text
total_records | valid_customer_names | valid_products
--------------+----------------------+---------------
7             | 7                    | 7
```

- This confirms that all 7 cleaned records now contain valid customer names and product values.

- Performs a final data-quality summary check after cleaning.
- `CASE WHEN` counts any remaining missing customer names, missing products, invalid quantities, or negative prices.
- A result of `0` in every column confirms that the detected quality issues were corrected.

```sql
SELECT
    SUM(CASE WHEN customer_name IS NULL OR customer_name = '' THEN 1 ELSE 0 END) AS missing_customer_names,
    SUM(CASE WHEN product IS NULL OR product = '' THEN 1 ELSE 0 END) AS missing_products,
    SUM(CASE WHEN quantity <= 0 THEN 1 ELSE 0 END) AS invalid_quantities,
    SUM(CASE WHEN unit_price < 0 THEN 1 ELSE 0 END) AS invalid_prices
FROM sales_cleaned;
```

Expected result:

```text
missing_customer_names | missing_products | invalid_quantities | invalid_prices
-----------------------+------------------+--------------------+---------------
0                      | 0                | 0                  | 0
```

- This confirms that the cleaned dataset passes the main quality checks.

## ---------------------------------Project Structure

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