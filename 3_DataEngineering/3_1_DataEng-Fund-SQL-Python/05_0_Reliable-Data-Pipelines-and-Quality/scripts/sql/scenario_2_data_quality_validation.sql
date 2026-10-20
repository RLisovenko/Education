/*
File: scenario_2_data_quality_validation.sql
Performed by: R. Lisovenko

Scenario 2:
Validating Data Quality in PostgreSQL

Description:
Loads a sales dataset containing intentional data-quality
problems and performs structured validation checks.
*/


-- ============================================================
-- 1. Create validation table
-- ============================================================

CREATE TABLE sales_quality (
    order_id INTEGER,
    customer_name VARCHAR(100),
    product VARCHAR(100),
    quantity INTEGER,
    unit_price NUMERIC(10,2),
    order_date DATE
);


-- ============================================================
-- 2. Load quality-check dataset
-- ============================================================

\copy sales_quality FROM 'data/raw/sales_orders_quality.csv' DELIMITER ',' CSV HEADER;


-- ============================================================
-- 3. Verify loaded records
-- ============================================================

SELECT COUNT(*) AS total_rows
FROM sales_quality;


SELECT *
FROM sales_quality
ORDER BY order_id;


-- ============================================================
-- 4. Check populated order IDs
-- ============================================================

SELECT
    COUNT(*) AS total_rows,
    COUNT(order_id) AS populated_order_ids
FROM sales_quality;


-- ============================================================
-- 5. Check missing customer names
-- ============================================================

SELECT *
FROM sales_quality
WHERE customer_name IS NULL
   OR customer_name = '';


-- ============================================================
-- 6. Check missing products
-- ============================================================

SELECT *
FROM sales_quality
WHERE product IS NULL
   OR product = '';


-- ============================================================
-- 7. Check duplicate order IDs
-- ============================================================

SELECT
    order_id,
    COUNT(*) AS duplicate_count
FROM sales_quality
GROUP BY order_id
HAVING COUNT(*) > 1;


-- ============================================================
-- 8. Check invalid quantities
-- ============================================================

SELECT *
FROM sales_quality
WHERE quantity <= 0;


-- ============================================================
-- 9. Check invalid prices
-- ============================================================

SELECT *
FROM sales_quality
WHERE unit_price <= 0;


-- ============================================================
-- 10. Completeness check
-- ============================================================

SELECT
    COUNT(*) AS total_records,
    COUNT(NULLIF(customer_name, '')) AS valid_customer_names,
    COUNT(NULLIF(product, '')) AS valid_products
FROM sales_quality;


-- ============================================================
-- 11. Count duplicate groups
-- ============================================================

SELECT
    COUNT(*) AS duplicate_records
FROM (
    SELECT order_id
    FROM sales_quality
    GROUP BY order_id
    HAVING COUNT(*) > 1
) duplicates;


-- ============================================================
-- 12. Data-quality summary
-- ============================================================

SELECT
    SUM(
        CASE
            WHEN customer_name IS NULL OR customer_name = ''
            THEN 1 ELSE 0
        END
    ) AS missing_customer_names,

    SUM(
        CASE
            WHEN product IS NULL OR product = ''
            THEN 1 ELSE 0
        END
    ) AS missing_products,

    SUM(
        CASE
            WHEN quantity <= 0
            THEN 1 ELSE 0
        END
    ) AS invalid_quantity,

    SUM(
        CASE
            WHEN unit_price <= 0
            THEN 1 ELSE 0
        END
    ) AS invalid_price

FROM sales_quality;