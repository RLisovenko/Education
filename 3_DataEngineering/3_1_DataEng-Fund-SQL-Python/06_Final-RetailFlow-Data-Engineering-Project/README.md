# 06_Final-RetailFlow-Data-Engineering-Project

1. Run scripts\ps\setup_unbl_scr.cmd if PowerShell scripts are blocked.
2. In PowerShell, run .\scripts\ps\start_cur_venv.ps1 and select 1.
3. Install packages: python -m pip install -r requirements.txt
4. Check the environment: .\scripts\ps\check_PATH.cmd

Folders: data, notebooks, output, docs, scripts/ps, scripts/sql, scripts/py.

# RetailFlow Data Engineering Project

Final practical project for the course **Data Engineering Foundations with SQL and Python**.

The project demonstrates an end-to-end structured data engineering workflow using CSV, JSON, Parquet, Python, PostgreSQL, SQL, Git, and data-quality engineering practices.

### 6.1. PostgreSQL Database Inspection

- Connect to PostgreSQL:

```powershell
psql -U postgres
```

- Connect to the `retail_db` database:

```text
\c retail_db
```

- Show the current database:

```sql
SELECT current_database();
```
### 6.2. Explore and Analyze the Source Data
- List all tables in the current database schema:

```text
\dt
```

Current tables:

```text
customers
orders
sales
sales_cleaned
sales_orders
sales_quality
shipments_clean
shipments_raw
```

- View the structure of a specific table:

```text
\d customers
```

- View table data:

```sql
SELECT *
FROM customers;
```

- List all tables with schema information:

```text
\dt+
```

- Exit PostgreSQL:

```text
\q
```
```tecxt
customers
├─ customer_id   integer          PRIMARY KEY, NOT NULL
├─ customer_name varchar(100)
└─ city          varchar(50)
```

```plain text
customers.customer_id
        ↑
        │ FOREIGN KEY
        │
orders.customer_id
```

```plain text
orders
├─ order_id      integer          PRIMARY KEY, NOT NULL
├─ customer_id   integer          FOREIGN KEY
├─ product       varchar(100)
├─ quantity      integer
├─ unit_price    numeric(10,2)
└─ order_date    date
```
```plain text
orders.customer_id
        │
        └──> customers.customer_id
```

```plain text
customers (1)
    │
    └────< orders (many)
```


### 6.3. Create Two Tables in the Database: Products and Order Items Tables
#### Create Table

```sql
CREATE TABLE items (
    id INTEGER PRIMARY KEY,
    item_name VARCHAR(100) not null,
    info VARCHAR(200)
);
```

```plain text
orders.order_id
      ↑
      │ FK
orders_items.order_id

items.id
      ↑
      │ FK
orders_items.item_id

```

```sql
CREATE TABLE orders_items (
    id INTEGER PRIMARY KEY,
    order_id INTEGER not null,
    item_id INTEGER not null,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (item_id) REFERENCES items(id)
);
```

```sql
ALTER TABLE orders_items
ADD COLUMN quantity INTEGER,
ADD COLUMN unit_price NUMERIC(10,2);
```

```sql
ALTER TABLE orders_items
RENAME COLUM

```text
orders_items
├─ id
├─ order_id
├─ item_id
├─ quantity
└─ price
```

```text
\d orders_items
```

- `NOT NULL` — requires the column to contain a value and prevents `NULL` from being stored.

- `order_id NOT NULL` — every order item must belong to an existing order.
- `item_id NOT NULL` — every order item must reference a product.
- `item_name NOT NULL` — every product must have a name.


#### Backward Compatibility with Previous Exercises

The existing `orders` table is preserved to maintain compatibility with previous course exercises.

The legacy columns:

- `product`
- `quantity`
- `unit_price`

are not removed because earlier SQL, JOIN, aggregation, and reporting exercises depend on them.

For the final project, a more normalized relational model is added using the new `items` and `order_items` tables.

The relationship is created through:

`order_items.order_id` → `orders.order_id`

and:

`order_items.item_id` → `items.item_id`

This approach allows the existing database and previous exercises to continue working while extending the model for the final Data Engineering project.

```palin text
orders
├─ order_id PK
├─ customer_id FK
├─ product        ← legacy, !! -> in items als item_name
├─ quantity       ← legacy, !!!
├─ unit_price     ← legacy, !!!!
└─ order_date

items
├─ item_id PK
├─ item_name
└─ info

order_items
├─ order_item_id PK
├─ order_id FK ──────> orders.order_id
├─ item_id FK ───────> items.item_id
├─ quantity
└─ unit_price
```
####Create links order_items an orders via key order_id 

```plain text
orders.order_id
      ↑
      │ FOREIGN KEY
      │
order_items.order_id

```
#### Final Project Test Customer and Order

- A new customer `LiR` with `customer_id = 7` is created for the final project.
- A new order `109` is linked to this customer.
- The legacy `product`, `quantity`, and `unit_price` columns in `orders` are preserved for backward compatibility but are not used for the new normalized order.
- Product information for order `109` will be stored through `orders_items` and `items`.

### 6.4. Build a File-to-Database Workflow
#### 4.1. Populate Items and Order Items

- The existing `orders` table is preserved for backward compatibility.
- Products are stored separately in the new `items` table.
- `orders_items` links each existing order to the corresponding item.
- `ON CONFLICT DO NOTHING` allows the inserts to be safely re-run without creating duplicate primary keys.

```sql
INSERT INTO items (id, item_name, info)
VALUES
(1, 'Laptop', 'Electronics'),
(2, 'Mouse', 'Accessories'),
(3, 'Keyboard', 'Accessories'),
(4, 'Monitor', 'Electronics'),
(5, 'Webcam', 'Accessories')
ON CONFLICT (id) DO NOTHING;
```

Verify:

```sql
SELECT *
FROM items
ORDER BY id;
```


Populate the relationship table:

```sql
INSERT INTO orders_items (id, order_id, item_id)
VALUES
(1, 101, 1),
(2, 102, 2),
(3, 103, 3),
(4, 104, 4),
(5, 105, 5),
(6, 106, 3),
(7, 107, 1),
(8, 108, 2)
ON CONFLICT (id) DO NOTHING;
```

Verify:

```sql
SELECT *
FROM orders_items
ORDER BY id;
```

- 1. Add a new customer for the final project 3_1_6

```sql
INSERT INTO customers (
    customer_id,
    customer_name,
    city
)
VALUES (
    7,
    'LiR-final project 6',
    NULL
);
```

```sql
SELECT *
FROM customers
WHERE customer_id = 7;
```
- 2. Create a new order for customer LiR
- Legacy product/quantity/unit_price columns are intentionally left NULL.
- New order products will be stored through orders_items.

```sql
INSERT INTO orders (
    order_id,
    customer_id,
    order_date
)
VALUES (
    109,
    7,
    '2026-10-21'
);
```
```sql
SELECT *
FROM orders
WHERE order_id = 109;
```

```text
customers
   7 LiR
     │
     ▼
orders
   109
     │
     ▼
orders_items
   │       │
   ▼       ▼
 items   quantity/...
```

```sql
INSERT INTO orders_items (
    id,
    order_id,
    item_id
)
VALUES
(1, 109, 1),
(2, 109, 2),
(3, 109, 3),
(4, 109, 4);
```
```plain text
Order 109
├─ Item 1
├─ Item 2
├─ Item 3
└─ Item 4
```

```sql
SELECT *
FROM orders_items
WHERE order_id = 109
ORDER BY id;
```

```sql
SELECT
    oi.order_id,
    i.id AS item_id,
    i.item_name
FROM orders_items oi
JOIN items i
    ON oi.item_id = i.id
WHERE oi.order_id = 109
ORDER BY oi.id;
```

#### 4.4 Prepaire Step: Build the File-to-Database Workflow

    order_316_customer_7.csv
            ↓
    \copy
            ↓
    order_items_raw
            ↓
    validation / cleaning
            ↓
    orders + items + orders_items

    ```sql
    INSERT INTO orders (
        order_id,
        customer_id,
        order_date
    )
    VALUES (
        316,
        7,
        '2026-10-21'
    );
    ```sql

    ```sql
    ALTER TABLE orders_items
    ADD COLUMN quantity INTEGER,
    ADD COLUMN unit_price NUMERIC(10,2);
    ```

    - Populates the `orders_items` table with item records for order `316`.
    - The dataset intentionally includes an invalid quantity, an invalid negative price, and a duplicate item to test data-quality checks.

    ```sql
    INSERT INTO orders_items (
        id,
        order_id,
        item_id,
        quantity,
        price
    )
    VALUES
    (5, 316, 1, 1, 75000.00),
    (6, 316, 2, 2, 800.00),
    (7, 316, 3, 0, 1600.00),       -- invalid quantity
    (8, 316, 4, 1, -18000.00),    -- invalid price
    (9, 316, 2, 2, 800.00);       -- duplicate item in the order

    ```
##### 4.4.1 Input File: `\raw\in_order_316_customer_7.csv`

        - Raw input file for order `316` and customer `7`.
        - The file contains intentionally incorrect and incomplete records for testing the data validation workflow.
        - Included data quality issues:
        - `quantity = 0`
        - negative `price`
        - missing `item_id`
        - duplicate order item
        - The file is stored in the `data/raw/` directory and must be validated before loading into the final PostgreSQL tables.
        
        ```powershell
        Get-Content data\raw\in_order_316_customer_7.csv
        ```
        ```text
            order_id,customer_id,item_id,quantity,price,order_date
            316,7,1,1,75000.00,2026-10-21
            316,7,2,2,800.00,2026-10-21
            316,7,3,0,1600.00,2026-10-21
            316,7,4,1,-18000.00,2026-10-21
            316,7,,1,2500.00,2026-10-21
            316,7,2,2,800.00,2026-10-21
        ```
##### 4.4.2 Validate records before loading them into the database

```
psql -U postgres -d retail_db
```

```sql
CREATE TABLE orders_items_raw (
    id INTEGER PRIMARY KEY,
    order_id INTEGER not null,
    item_id INTEGER not null,
    quantity INTEGER,
    price NUMERIC(10,2),
    order_date DATE    
);
```
```sql
    ALTER TABLE orders_items_raw
    ALTER COLUMN order_id DROP NOT NULL,
    ALTER COLUMN item_id DROP NOT NULL;
``` 
```sql
DROP TABLE IF EXISTS orders_items_raw;
```
```sql
CREATE TABLE orders_items_raw (
    order_id INTEGER,
    customer_id INTEGER,
    item_id INTEGER,
    quantity INTEGER,
    price NUMERIC(10,2),
    order_date DATE
);  
```

##### 4.4.3 Load valid records into the appropriate PostgreSQL tables. 
    -  Cllear Buffer
    ``` 
        \r
    ```

```text
\copy orders_items_raw (
    order_id,
    customer_id,
    item_id,
    quantity,
    price,
    order_date
)
FROM 'data/raw/in_order_316_customer_7.csv'
DELIMITER ','
CSV HEADER;
```
\copy orders_items_raw (order_id, customer_id, item_id, quantity, price, order_date) FROM 'in_order_316_customer_7.csv' DELIMITER ',' CSV HEADER;

```
\copy orders_items_raw (order_id, customer_id, item_id, quantity, price, order_date) FROM '../data/raw/in_order_316_customer_7.csv' DELIMITER ',' CSV HEADER;
```
- Identify the current working directory before loading the CSV file.

```text
\! cd
```
#### 4.5 Handle Invalid or Incomplete Records Appropriately

Invalid or incomplete records are identified in the `orders_items_raw` table before they are loaded into the final `orders_items` table.

The following conditions are treated as invalid:

- missing `order_id`
- missing `customer_id`
- missing `item_id`
- `quantity <= 0`
- `price <= 0`
- missing `order_date`

```sql
SELECT *
FROM orders_items_raw
WHERE order_id IS NULL
   OR customer_id IS NULL
   OR item_id IS NULL
   OR quantity IS NULL
   OR quantity <= 0
   OR price IS NULL
   OR price <= 0
   OR order_date IS NULL;
```
These records are not loaded into the final table until they are corrected or explicitly rejected.
```sql
ALTER TABLE orders_items_raw
ADD COLUMN error_reason VARCHAR(100);
```

```sql
    UPDATE orders_items_raw
    SET item_id = Null, error_reason = 'Missing item_id'
    WHERE item_id IS NULL; 

```
- Invalid quantity values (`quantity <= 0`) are replaced with `NULL` during data cleaning.
```sql
    UPDATE orders_items_raw
    SET quantity = Null, error_reason = 'Missing quantity'
    WHERE quantity <=0; 

```

- Invalid price values (`price <= 0`) are replaced with `NULL` during data cleaning.
```sql
    UPDATE orders_items_raw
    SET price = NULL,
        error_reason = 'Invalid price: ' || price::text
    WHERE price <= 0;

```
#### 4.6 Design the workflow so that repeated execution does not unnecessarily duplicate existing records.
    ```sql
        select count(*) as dubl_count
        from orders_items_raw;

    ```
    ```sql
        select order_id, item_id, count(*) as dubl_count
        from orders_items_raw
        group by order_id,item_id
        having count(*)>1;

    ```
    - Duplicate records are detected using the combination of `order_id` and `item_id`.

    ```sql
        UPDATE orders_items_raw
        SET error_reason =
            'Duplicate item_id: ' || item_id::text ||
            ', quantity: ' || quantity::text
        WHERE (order_id, item_id) IN (
            SELECT
                order_id,
                item_id
            FROM orders_items_raw
            GROUP BY order_id, item_id
            HAVING COUNT(*) > 1
        );
    ```
#### Raw Data Validation Result
```text
        The `orders_items_raw` table contains the following records after validation:

        ```text
        order_id | customer_id | item_id | quantity | price     | order_date | error_reason
        ---------+-------------+---------+----------+-----------+------------+--------------------------------------
        316      | 7           | 1       | 1        | 75000.00  | 2026-10-21 |
        316      | 7           |         | 1        | 2500.00   | 2026-10-21 | Missing item_id
        316      | 7           | 3       |          | 1600.00   | 2026-10-21 | Missing quantity
        316      | 7           | 4       | 1        |           | 2026-10-21 | Invalid price: -18000.00
        316      | 7           | 2       | 2        | 800.00    | 2026-10-21 | Duplicate item_id: 2, quantity: 2
        316      | 7           | 2       | 2        | 800.00    | 2026-10-21 | Duplicate item_id: 2, quantity: 2
```
    - The first matching record is preserved, while additional duplicate rows are marked with an error reason.
    - PostgreSQL `ctid` is used only as a temporary technical identifier to distinguish otherwise identical raw records.

    ```sql
        UPDATE orders_items_raw r
        SET error_reason = 'Duplicate item: ' || r.item_id::text
        WHERE r.ctid NOT IN (
            SELECT MIN(ctid)
            FROM orders_items_raw
            GROUP BY order_id, item_id
        );
    ```
    ```text
        316 | 2 | ...   ← первая остаётся
        316 | 2 | ...   ← вторая получает Duplicate item
    ```

#### 4.7 Explain how idempotency and safe reprocessing are supported.
#### Idempotency and Safe Reprocessing

- Raw source data is first loaded into the `orders_items_raw` staging table.
- Records are validated before they are inserted into the final `orders_items` table.
- Invalid and duplicate records are marked using `error_reason` and are not loaded into the final table.
- Before inserting a valid record, the workflow checks whether the same `order_id` and `item_id` already exist in `orders_items`.
- This prevents duplicate records when the same input file is processed more than once.
- The raw staging data can be safely cleared and reloaded from the original CSV file if processing needs to be repeated.

    ```sql
        INSERT INTO orders_items (
            order_id,
            item_id,
            quantity,
            price
        )
        SELECT
            r.order_id,
            r.item_id,
            r.quantity,
            r.price
        FROM orders_items_raw r
        WHERE r.error_reason IS NULL

        AND NOT EXISTS (
            SELECT 1
            FROM orders_items oi
            WHERE oi.order_id = r.order_id
                AND oi.item_id = r.item_id
        );
    ```
- Only valid records are loaded into the final table.
- Idempotency ensures that reprocessing the same input file does not create duplicate records or change already processed valid data.

- The combination of `order_id` and `item_id` is defined as unique in the final `orders_items` table.
    ```sql
        ALTER TABLE orders_items
        ADD CONSTRAINT uq_order_item
        UNIQUE (order_id, item_id);
    ```
- This prevents the same item from being inserted twice for the same order at the database level.
    ON CONFLICT (order_id, item_id) DO NOTHING;
- Because the database enforces this rule, a separate `NOT EXISTS` check is not required before every insert.
    ```sql
            AND NOT EXISTS (
            SELECT 1
            FROM orders_items oi
            WHERE oi.order_id = r.order_id
                AND oi.item_id = r.item_id
    ```
#### Configure Automatic ID Generation and Prevent Duplicate Order Items

The final `orders_items` table uses an automatically generated `id`.

Because the table already contains existing records, the `id` column is converted to an identity column so PostgreSQL can generate new identifiers automatically during future inserts.

```sql
ALTER TABLE orders_items
ALTER COLUMN id
ADD GENERATED BY DEFAULT AS IDENTITY;
```
```sql
SELECT setval(
    pg_get_serial_sequence('orders_items', 'id'),
    (SELECT MAX(id) FROM orders_items),
    true
);
```

Valid records can then be loaded from the raw staging table without manually specifying `id`.

```sql
INSERT INTO orders_items (
    order_id,
    item_id,
    quantity,
    price
)
SELECT
    r.order_id,
    r.item_id,
    r.quantity,
    r.price
FROM orders_items_raw r
WHERE r.error_reason IS NULL
ON CONFLICT (order_id, item_id) DO NOTHING;
```

- `GENERATED BY DEFAULT AS IDENTITY` automatically creates new `id` values.
- `UNIQUE (order_id, item_id)` prevents duplicate items within the same order.
- `error_reason IS NULL` ensures that only valid records are loaded.
- `ON CONFLICT DO NOTHING` safely skips records that already exist.
- This supports idempotent reprocessing because the same input can be processed again without creating duplicate final records.



### 6.5. Explore the Data with SQL

Use SQL to analyse the loaded retail data stored in PostgreSQL.

#### 5.1 Filtering and Sorting Records

Use `WHERE`, `ORDER BY`, and other filtering conditions to retrieve specific records and organize query results.

#### 5.2 Calculating Totals, Averages, and Counts

Use aggregate functions such as `SUM()`, `AVG()`, and `COUNT()` to calculate summary values from the retail data.

#### 5.3 Grouping Data for Business Analysis

Use `GROUP BY` to summarize data by customers, orders, items, or other business dimensions.

#### 5.4 Joining Related Tables

Use SQL `JOIN` operations to combine information from related tables:

- `customers`
- `orders`
- `orders_items`
- `items`

This allows customer, order, product, quantity, and price information to be analysed together.

#### 5.5 Calculating Sales Metrics

Calculate useful business metrics such as:

- total order value
- total quantity sold
- average item price
- sales by customer
- sales by item

The basic sales calculation is:

`quantity × price`

#### 5.6 Common Table Expressions (CTEs)

Use `WITH` and Common Table Expressions (CTEs) to divide complex SQL queries into clear and reusable logical steps.

CTEs make analytical queries easier to read, understand, and maintain.

#### 5.7 Window Functions

Use SQL window functions with `OVER()` to perform analytical calculations without grouping individual rows into a single result.

Window functions can be used for:

- ranking records
- numbering rows
- comparing values
- calculating running totals
- analysing values within groups




        
## ---------------Executor

- Performed by: R. Lisovenko
- Created: 21-10-2026

## Business Context

RetailFlow Commerce is a growing retail company that receives business data from multiple systems, including:

- customer records
- product catalogs
- store transactions
- online orders
- sales reports

The company receives much of this information as CSV, JSON, and Parquet files.

As data volumes grow, the existing manual workflow becomes difficult to manage and may introduce missing values, duplicates, invalid records, schema inconsistencies, and repeated processing problems.

The goal of this project is to build a structured, reliable, and reproducible data engineering workflow.

## Project Goals

The project includes:

- structured project organization
- CSV, JSON, and Parquet inspection
- schema validation
- data contract documentation
- PostgreSQL relational modeling
- file-to-database loading
- SQL exploration and reporting
- JOIN operations
- aggregations and business metrics
- CTEs
- window functions
- defensive SQL
- data-quality validation
- data cleaning
- duplicate handling
- idempotent processing
- incremental loading
- safe reprocessing
- pipeline troubleshooting
- final validation

## Project Structure

```text
06_Final-RetailFlow-Data-Engineering-Project/
├─ data/
│  ├─ raw/
│  │  ├─ csv/
│  │  ├─ json/
│  │  └─ parquet/
│  ├─ processed/
│  └─ rejected/
│
├─ docs/
│  ├─ data_contract.md
│  ├─ data_quality_checklist.md
│  ├─ idempotency_strategy.md
│  ├─ troubleshooting.md
│  └─ er_diagram.png
│
├─ notebooks/
├─ output/
│
├─ scripts/
│  ├─ ps/
│  ├─ py/
│  │  ├─ inspect_source_data.py
│  │  ├─ validate_data.py
│  │  ├─ clean_data.py
│  │  └─ load_postgresql.py
│  │
│  └─ sql/
│     ├─ 01_create_tables.sql
│     ├─ 02_load_validation.sql
│     ├─ 03_data_quality.sql
│     ├─ 04_cleaning.sql
│     ├─ 05_business_queries.sql
│     ├─ 06_joins_metrics.sql
│     ├─ 07_cte_window_functions.sql
│     └─ 08_final_validation.sql
│
├─ .gitignore
├─ README.md
├─ requirements.txt
└─ Scenario
```

## Data Processing Workflow

```text
Raw Data
   ↓
File Inspection
   ↓
Schema Validation
   ↓
Data Quality Validation
   ↓
Cleaning and Standardization
   ↓
PostgreSQL Load
   ↓
Relational Modeling
   ↓
SQL Analysis
   ↓
Business Metrics
   ↓
Final Validation
   ↓
Trusted Data
```

## Source Data Formats

The project works with:

- CSV
- JSON
- Parquet

Each format is inspected for:

- columns
- data types
- record count
- missing values
- duplicate records
- invalid values
- schema inconsistencies

## PostgreSQL Data Model

The relational model will include business entities such as:

```text
customers
products
orders
order_items
```

The database design will use:

- primary keys
- foreign keys
- appropriate PostgreSQL data types
- relationships between business entities
- controlled NULL handling

## File-to-Database Workflow

The pipeline will:

1. Receive source files.
2. Inspect file structure.
3. Validate the expected schema.
4. Check data quality.
5. Clean or isolate invalid records.
6. Load trusted records into PostgreSQL.
7. Verify row counts.
8. Check duplicates.
9. Validate relational integrity.
10. Confirm final data quality.

## SQL Analysis

SQL exercises include:

- `SELECT`
- `WHERE`
- `ORDER BY`
- `LIMIT`
- `DISTINCT`
- `COUNT`
- `SUM`
- `AVG`
- `MIN`
- `MAX`
- `GROUP BY`
- `HAVING`
- `INNER JOIN`
- `LEFT JOIN`
- CTEs
- window functions
- defensive SQL

## Data Quality

The workflow checks:

- required fields
- missing values
- empty strings
- duplicate IDs
- invalid numeric values
- date validity
- schema compatibility
- relational integrity
- expected row counts
- calculated business metrics

## Data Cleaning

Cleaning operations may include:

- replacing missing values
- removing duplicates
- standardizing text
- correcting numeric values
- validating dates
- separating rejected records
- preserving raw source data

## Idempotency and Safe Reprocessing

The workflow should be safe to run repeatedly.

Key principles:

- avoid duplicate inserts
- identify already processed records
- process only new or changed data when possible
- allow failed steps to be safely re-run
- preserve consistent database results

## Incremental Loading

Incremental processing should load only:

```text
new records
or
changed records
```

instead of reprocessing the complete dataset every time.

## Troubleshooting

Common pipeline problems include:

- missing input files
- schema changes
- invalid data types
- duplicate records
- PostgreSQL connection failures
- SQL errors
- incorrect JOIN conditions
- failed or incomplete loads

Each problem should be identified, investigated, corrected, and documented.

## Expected Result

The completed project should demonstrate how raw structured data can be transformed into:

```text
structured
validated
cleaned
queryable
reliable
analysis-ready data
```

using a reproducible Data Engineering workflow.
