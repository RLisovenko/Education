-- RetailFlow Final Project
-- Section 6.10: Troubleshoot and Validate the Complete Workflow

-- 6.10.1 Missing input files
-- In psql, while current directory is data/raw:
-- \! powershell -Command "Test-Path '.\in_order_316_customer_7.csv'"

-- 6.10.2 Unexpected schema changes
SELECT
    column_name,
    data_type,
    ordinal_position
FROM information_schema.columns
WHERE table_name = 'orders_items_raw'
ORDER BY ordinal_position;

-- 6.10.3 Invalid data types
SELECT
    column_name,
    data_type
FROM information_schema.columns
WHERE table_name = 'orders_items_raw'
ORDER BY ordinal_position;

-- 6.10.4 Duplicate records
SELECT
    order_id,
    item_id,
    COUNT(*) AS duplicate_count
FROM orders_items
GROUP BY order_id, item_id
HAVING COUNT(*) > 1;

-- 6.10.5 Database connection failures
-- Connection test:
-- psql -U postgres -d retail_db

-- 6.10.6 SQL query errors
SELECT *
FROM orders_items
WHERE order_id = 316
ORDER BY item_id;

-- In interactive psql, clear an incomplete query buffer with:
-- \r

-- 6.10.7 Incorrect joins
SELECT
    o.order_id,
    oi.item_id,
    i.item_name,
    COUNT(*) AS join_count
FROM orders o
JOIN orders_items oi
    ON o.order_id = oi.order_id
JOIN items i
    ON oi.item_id = i.id
GROUP BY
    o.order_id,
    oi.item_id,
    i.item_name
ORDER BY
    o.order_id,
    oi.item_id;

-- 6.10.8 Failed or incomplete data loads
SELECT COUNT(*) AS raw_rows
FROM orders_items_raw;

SELECT
    order_id,
    COUNT(*) AS final_rows
FROM orders_items
GROUP BY order_id
ORDER BY order_id;

-- 6.10.9 Execute and validate the complete workflow
SELECT
    order_id,
    COUNT(*) AS final_rows
FROM orders_items
GROUP BY order_id
ORDER BY order_id;

SELECT
    order_id,
    SUM(quantity) AS total_quantity,
    SUM(quantity * price) AS total_sales
FROM orders_items
GROUP BY order_id
ORDER BY order_id;

SELECT *
FROM orders_items
WHERE order_id IS NULL
   OR item_id IS NULL
   OR quantity IS NULL
   OR price IS NULL;

SELECT *
FROM orders_items
WHERE quantity <= 0
   OR price <= 0;

SELECT
    order_id,
    item_id,
    COUNT(*) AS duplicate_count
FROM orders_items
GROUP BY order_id, item_id
HAVING COUNT(*) > 1;

SELECT
    oi.order_id,
    oi.item_id
FROM orders_items oi
LEFT JOIN orders o
    ON oi.order_id = o.order_id
WHERE o.order_id IS NULL;

SELECT
    oi.order_id,
    oi.item_id
FROM orders_items oi
LEFT JOIN items i
    ON oi.item_id = i.id
WHERE i.id IS NULL;

-- Expected business metrics:
-- 109 -> total_quantity 6, total_sales 114100.00
-- 316 -> total_quantity 3, total_sales 91000.00
