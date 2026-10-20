/*
File: scenario_3_cleaning_and_preparation.sql
Performed by: R. Lisovenko

Scenario 3:
Cleaning and Preparing Data for Analysis

Description:
Loads sales data containing known quality problems,
corrects missing and invalid values, standardizes text,
removes duplicates, and performs final quality checks.
*/


-- ============================================================
-- 1. Create cleaned sales table
-- ============================================================

CREATE TABLE sales_cleaned (
    order_id INTEGER,
    customer_name VARCHAR(100),
    product VARCHAR(100),
    quantity INTEGER,
    unit_price NUMERIC(10,2),
    order_date DATE
);


-- ============================================================
-- 2. Load source dataset
-- ============================================================

\copy sales_cleaned FROM 'data/raw/sales_orders_cleaning.csv' DELIMITER ',' CSV HEADER;


-- ============================================================
-- 3. View source records
-- ============================================================

SELECT *
FROM sales_cleaned
ORDER BY order_id;


-- ============================================================
-- 4. Fix missing customer names
-- ============================================================

UPDATE sales_cleaned
SET customer_name = 'Unknown Customer'
WHERE customer_name IS NULL
   OR customer_name = '';


-- ============================================================
-- 5. Verify missing customer-name correction
-- ============================================================

SELECT *
FROM sales_cleaned
WHERE customer_name = 'Unknown Customer';


-- ============================================================
-- 6. Fix missing products
-- ============================================================

UPDATE sales_cleaned
SET product = 'Unknown Product'
WHERE product IS NULL
   OR product = '';


-- ============================================================
-- 7. Fix invalid quantities
-- ============================================================

UPDATE sales_cleaned
SET quantity = 1
WHERE quantity <= 0;


-- ============================================================
-- 8. Verify quantities
-- ============================================================

SELECT *
FROM sales_cleaned
WHERE quantity <= 0;


-- ============================================================
-- 9. Fix negative prices
-- ============================================================

UPDATE sales_cleaned
SET unit_price = ABS(unit_price)
WHERE unit_price < 0;


-- ============================================================
-- 10. Verify prices
-- ============================================================

SELECT *
FROM sales_cleaned
WHERE unit_price < 0;


-- ============================================================
-- 11. Standardize customer names
-- TRIM() removes leading/trailing spaces.
-- INITCAP() converts names to title case.
-- ============================================================

UPDATE sales_cleaned
SET customer_name = INITCAP(TRIM(customer_name));


-- ============================================================
-- 12. Remove duplicate records
-- ============================================================

DELETE FROM sales_cleaned
WHERE ctid NOT IN (
    SELECT MIN(ctid)
    FROM sales_cleaned
    GROUP BY order_id
);


-- ============================================================
-- 13. Verify duplicate removal
-- ============================================================

SELECT
    order_id,
    COUNT(*) AS duplicate_count
FROM sales_cleaned
GROUP BY order_id
HAVING COUNT(*) > 1;


-- ============================================================
-- 14. View final cleaned dataset
-- ============================================================

SELECT *
FROM sales_cleaned
ORDER BY order_id;


-- ============================================================
-- 15. Final completeness check
-- ============================================================

SELECT
    COUNT(*) AS total_records,
    COUNT(NULLIF(customer_name, '')) AS valid_customer_names,
    COUNT(NULLIF(product, '')) AS valid_products
FROM sales_cleaned;


-- ============================================================
-- 16. Final data-quality summary
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
    ) AS invalid_quantities,

    SUM(
        CASE
            WHEN unit_price < 0
            THEN 1 ELSE 0
        END
    ) AS invalid_prices

FROM sales_cleaned;