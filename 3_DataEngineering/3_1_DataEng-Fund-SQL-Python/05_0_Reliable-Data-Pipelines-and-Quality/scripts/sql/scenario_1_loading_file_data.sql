/*
File: scenario_1_loading_file_data.sql
Performed by: R. Lisovenko

Scenario 1:
Loading File Data into PostgreSQL

Description:
Creates the destination table, loads sales data from CSV,
verifies imported records, checks duplicates,
and calculates the total sales value.
*/


-- ============================================================
-- 1. Create destination table
-- ============================================================

CREATE TABLE sales_orders (
    order_id INTEGER,
    customer_name VARCHAR(100),
    product VARCHAR(100),
    quantity INTEGER,
    unit_price NUMERIC(10,2),
    order_date DATE
);


-- ============================================================
-- 2. Load CSV data
-- ============================================================

\copy sales_orders FROM 'data/raw/sales_orders.csv' DELIMITER ',' CSV HEADER;


-- ============================================================
-- 3. Verify number of imported rows
-- ============================================================

SELECT COUNT(*) AS total_rows
FROM sales_orders;


-- ============================================================
-- 4. Verify populated order IDs
-- ============================================================

SELECT
    COUNT(*) AS total_rows,
    COUNT(order_id) AS populated_order_ids
FROM sales_orders;


-- ============================================================
-- 5. View imported records
-- ============================================================

SELECT *
FROM sales_orders
ORDER BY order_id;


-- ============================================================
-- 6. Check duplicate order IDs
-- ============================================================

SELECT
    order_id,
    COUNT(*) AS duplicate_count
FROM sales_orders
GROUP BY order_id
HAVING COUNT(*) > 1;


-- ============================================================
-- 7. Calculate total sales value
-- ============================================================

SELECT
    SUM(quantity * unit_price) AS total_sales_value
FROM sales_orders;