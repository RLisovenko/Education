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

#### 6.5.1. Filtering and Sorting Records

Filtering and sorting are used to retrieve specific records from the database and organize the results in a meaningful order.

WHERE filters records according to specified conditions.

ORDER BY sorts the returned records.

ASC sorts values in ascending order.

DESC sorts values in descending order.

Example: display all order items for order 316 and sort them by price from highest to lowest.
```sql
SELECT
    order_id,
    item_id,
    quantity,
    price
FROM orders_items
WHERE order_id = 316
ORDER BY price DESC;
```
Example: display all orders for customer 7, sorted by order date.
```sql
SELECT *
FROM orders
WHERE customer_id = 7
ORDER BY order_date ASC;
```
These queries demonstrate how filtering and sorting can be used to explore specific customer and order data stored in PostgreSQL.

#### 6.5.2. Calculating Totals, Averages, and Counts
##### 6.5.2.1. Two additional valid records
- Two additional valid records were added to the input CSV file to make the final SQL analysis more illustrative.
- `TRUNCATE TABLE orders_items_raw;` removes all previously loaded raw records before reloading the updated CSV file.
- This keeps the staging table synchronized with the current source file and avoids unnecessary duplicates in the raw layer.
- Even if duplicate records remain in the raw table, the final `orders_items` table is protected by the unique constraint on `(order_id, item_id)` and `ON CONFLICT DO NOTHING`.

```sql
TRUNCATE TABLE orders_items_raw;
```
- Reload the updated CSV file into the `orders_items_raw` staging table.

```sql
\copy orders_items_raw (order_id, customer_id, item_id, quantity, price, order_date) FROM 'in_order_316_customer_7.csv' DELIMITER ',' CSV HEADER;
```

- The updated file now contains **8 records**, including two additional valid records for further SQL analysis.

- After reloading and validating the updated raw data, only valid records are transferred to the final `orders_items` table.
- Existing `(order_id, item_id)` combinations are skipped automatically, so only new valid order items are added.

- The `UPDATE` statement cleans and validates all records in the `orders_items_raw` staging table in one step.
- Invalid quantities (`quantity <= 0`) are replaced with `NULL`.
- Invalid prices (`price <= 0`) are replaced with `NULL`.
- Missing `item_id` values are marked with `Missing item_id`.
- Invalid quantities are marked with `Missing quantity`.
- Invalid prices are marked with the original invalid value.
- Fully duplicated records are detected using all relevant columns and marked as duplicates.
- Valid records remain with `error_reason = NULL` and can later be loaded into the final `orders_items` table.
```sql
UPDATE orders_items_raw r
SET
    quantity = CASE
        WHEN r.quantity <= 0 THEN NULL
        ELSE r.quantity
    END,

    price = CASE
        WHEN r.price <= 0 THEN NULL
        ELSE r.price
    END,

    error_reason = CASE
        WHEN r.item_id IS NULL
            THEN 'Missing item_id'

        WHEN r.quantity <= 0
            THEN 'Missing quantity'

        WHEN r.price <= 0
            THEN 'Invalid price: ' || r.price::text

        WHEN (
            r.order_id,
            r.customer_id,
            r.item_id,
            r.quantity,
            r.price,
            r.order_date
        ) IN (
            SELECT
                order_id,
                customer_id,
                item_id,
                quantity,
                price,
                order_date
            FROM orders_items_raw
            GROUP BY
                order_id,
                customer_id,
                item_id,
                quantity,
                price,
                order_date
            HAVING COUNT(*) > 1
        )
            THEN 'Duplicate item_id: ' || r.item_id::text ||
                 ', quantity: ' || r.quantity::text

        ELSE NULL
    END;
```

- Only validated records with `error_reason IS NULL` are inserted into the final `orders_items` table.
- Existing `(order_id, item_id)` combinations are skipped automatically to prevent duplicates.

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

- `error_reason IS NULL` allows only validated records to be loaded.
- `ON CONFLICT (order_id, item_id) DO NOTHING` prevents existing order items from being inserted again.

```sql
UPDATE orders_items oi
SET
    quantity = r.quantity,
    price = r.price
FROM orders_items_raw r
WHERE oi.order_id = r.order_id
  AND oi.item_id = r.item_id
  AND oi.order_id = 316
  AND r.quantity > 0
  AND r.price > 0;
```

##### 6.5.2.2. Aggregate functions are used to calculate summary values from the loaded retail data.

- `SUM()` calculates totals.
- `AVG()` calculates average values.
- `COUNT()` counts records.

- Calculate the total quantity and total sales value for order `316`:

```sql
SELECT
    order_id,
    SUM(quantity) AS total_quantity,
    SUM(quantity * price) AS total_sales
FROM orders_items
WHERE order_id = 316
GROUP BY order_id;
```
```text
Result:

order_id | total_quantity | total_sales
---------+----------------+------------
316      | 3              | 91000.00

The order contains a total of 3 items.

The total sales value is 91,000.00.
```
Calculate the average item price for order `316`:

```sql
SELECT
    order_id,
    AVG(price) AS average_price
FROM orders_items
WHERE order_id = 316
GROUP BY order_id;
```
```text
Result:

order_id | average_price
---------+--------------------
316      | 30333.333333333333

The average item price for order 316 is approximately 30,333.33.
```
Count the number of items in order `316`:

```sql
SELECT
    order_id,
    COUNT(*) AS item_count
FROM orders_items
WHERE order_id = 316
GROUP BY order_id;
```

#### 6.5.3. Grouping Data for Business Analysis

`GROUP BY` is used to organize records into groups and calculate summary values for each group.

The following query groups order items by `item_id` and calculates the total quantity and sales value for each item in order `316`.

```sql
SELECT
    item_id,
    SUM(quantity) AS total_quantity,
    SUM(quantity * price) AS total_sales
FROM orders_items
WHERE order_id = 316
GROUP BY item_id
ORDER BY item_id;
```

Expected result:

```text
item_id | total_quantity | total_sales
--------+----------------+------------
1       | 1              | 75000.00
3       | 1              | 7000.00
4       | 1              | 9000.00
```

- `GROUP BY item_id` creates a separate group for each item.
- `SUM(quantity)` calculates the quantity sold for each item.
- `SUM(quantity * price)` calculates the sales value generated by each item.
- This type of grouping can be used for product-level business analysis.

#### 6.5.4. Joining Customer, Order, Product, and Transaction Information

`JOIN` is used to combine related information stored in separate relational tables.

The following query combines:

- customer information from `customers`
- order information from `orders`
- order item information from `orders_items`
- product information from `items`

```sql
SELECT
    c.customer_id,
    c.customer_name,
    o.order_id,
    o.order_date,
    i.item_name,
    oi.quantity,
    oi.price,
    oi.quantity * oi.price AS line_total
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
JOIN orders_items oi
    ON o.order_id = oi.order_id
JOIN items i
    ON oi.item_id = i.id
WHERE o.order_id = 316
ORDER BY oi.item_id;
```

Expected result:

```text
customer_id | customer_name | order_id | order_date  | item_name | quantity | price    | line_total
------------+---------------+----------+-------------+-----------+----------+----------+-----------
7           | LiR           | 316      | 2026-10-21  | ...       | 1        | 75000.00 | 75000.00
7           | LiR           | 316      | 2026-10-21  | ...       | 1        | 7000.00  | 7000.00
7           | LiR           | 316      | 2026-10-21  | ...       | 1        | 9000.00  | 9000.00
```

- The joins connect the relational model through primary and foreign keys.
- Customer, order, product, quantity, and price information can be analysed together.
- `quantity * price` calculates the value of each individual order line.

The relational tables are connected using existing primary and foreign keys.

The query combines customer, order, order item, and product information into one result.

```sql
SELECT
    c.customer_name,
    o.order_id,
    i.item_name,
    oi.quantity,
    oi.price
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
JOIN orders_items oi
    ON o.order_id = oi.order_id
JOIN items i
    ON oi.item_id = i.id
WHERE o.order_id = 316;
```

- `customers.customer_id` is linked to `orders.customer_id`.
- `orders.order_id` is linked to `orders_items.order_id`.
- `orders_items.item_id` is linked to `items.id`.
- No additional customer identifier is required because `customer_id` already acts as the primary key in the `customers` table.
- The result shows who placed the order, which products were included, their quantities, and their prices.

#### 6.5.5. Calculating Useful Sales Metrics

Sales metrics help summarize the financial value of customer orders.

The following query calculates the total value of order `316` and the total number of items included in the order.

```sql
SELECT
    o.order_id,
    c.customer_name,
    SUM(oi.quantity) AS total_quantity,
    SUM(oi.quantity * oi.price) AS total_order_value
FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id
JOIN orders_items oi
    ON o.order_id = oi.order_id
WHERE o.order_id = 316
GROUP BY
    o.order_id,
    c.customer_name;
```

Expected result:

```text
order_id | customer_name | total_quantity | total_order_value
---------+---------------+----------------+------------------
316      | LiR           | 3              | 91000.00
```

- `SUM(oi.quantity)` calculates the total number of items in the order.
- `SUM(oi.quantity * oi.price)` calculates the total financial value of the order.
- The query combines customer and order information to produce a useful business metric.

#### 6.5.6. Using Common Table Expressions (CTEs)

A Common Table Expression (CTE) is a temporary named result set created with `WITH`.

CTEs make complex SQL queries easier to read and organize.

The following query first calculates the value of each order item and then calculates the total value of order `316`.

```sql
WITH order_details AS (
    SELECT
        oi.order_id,
        oi.item_id,
        oi.quantity,
        oi.price,
        oi.quantity * oi.price AS line_total
    FROM orders_items oi
    WHERE oi.order_id = 316
)
SELECT
    order_id,
    SUM(quantity) AS total_quantity,
    SUM(line_total) AS total_order_value
FROM order_details
GROUP BY order_id;
```

Expected result:

```text
order_id | total_quantity | total_order_value
---------+----------------+------------------
316      | 3              | 91000.00
```

- The CTE `order_details` calculates `line_total` for each item.
- The main query uses the CTE result to calculate totals.
- This approach separates the calculation into clear logical steps and makes the query easier to maintain.

#### 6.5.7. Using Window Functions

Window functions perform analytical calculations across a set of rows without collapsing them into a single grouped result.

The following query ranks the items in order `316` by price from highest to lowest.

```sql
SELECT
    order_id,
    item_id,
    quantity,
    price,
    ROW_NUMBER() OVER (
        PARTITION BY order_id
        ORDER BY price DESC
    ) AS price_rank
FROM orders_items
WHERE order_id = 316;
```

Expected result:

```text
order_id | item_id | quantity | price    | price_rank
---------+---------+----------+----------+-----------
316      | 1       | 1        | 75000.00 | 1
316      | 4       | 1        | 9000.00  | 2
316      | 3       | 1        | 7000.00  | 3
```

- `ROW_NUMBER()` assigns a sequential number to each row.
- `PARTITION BY order_id` performs the calculation separately for each order.
- `ORDER BY price DESC` ranks the most expensive item first.
- Unlike `GROUP BY`, the window function keeps all individual rows visible.

Functions and clauses used:

- ROW_NUMBER() — assigns a sequential number to each row.

- OVER() — defines the window over which the window function operates.

- PARTITION BY order_id — divides the records into separate groups for each order.

- ORDER BY price DESC — sorts items from the highest price to the lowest price inside each order.

- AS price_rank — gives the calculated row number the alias price_rank.

Unlike GROUP BY, a window function does not combine multiple records into one row. Each original order item remains visible while the analytical value is added as an additional column.

### 6.6. Apply Defensive SQL Practices

Defensive SQL is used to make queries more reliable when the database contains incomplete, invalid, or unexpected data.

#### 6.6.1. Identify NULL Values

Before calculations or joins are performed, columns should be checked for missing values.

```sql
SELECT *
FROM orders_items
WHERE order_id IS NULL
   OR item_id IS NULL
   OR quantity IS NULL
   OR price IS NULL;
```

- `IS NULL` identifies records with missing values.
- Detecting missing values before calculations helps prevent incorrect analytical results.
- In the final `orders_items` table, important business fields should normally contain valid values.


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
