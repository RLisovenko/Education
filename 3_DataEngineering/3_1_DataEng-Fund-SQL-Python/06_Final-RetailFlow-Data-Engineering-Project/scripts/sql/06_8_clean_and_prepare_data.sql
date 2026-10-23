-- RetailFlow Final Project
-- Section 6.8: Clean and Prepare the Data

-- 6.8.1 Remove or Resolve Duplicate Records
SELECT
    order_id,
    item_id,
    quantity,
    price,
    COUNT(*) AS duplicate_count
FROM orders_items_raw
GROUP BY
    order_id,
    item_id,
    quantity,
    price
HAVING COUNT(*) > 1;

-- 6.8.2 Handle Missing Values
SELECT *
FROM orders_items_raw
WHERE order_id IS NULL
   OR customer_id IS NULL
   OR item_id IS NULL
   OR quantity IS NULL
   OR price IS NULL
   OR order_date IS NULL;

UPDATE orders_items_raw
SET error_reason = 'Missing item_id'
WHERE item_id IS NULL;

-- 6.8.3 Standardize Text Values
UPDATE customers
SET customer_name = INITCAP(TRIM(customer_name));

-- 6.8.4 Check / Correct Data Types
SELECT
    column_name,
    data_type
FROM information_schema.columns
WHERE table_name = 'orders_items_raw'
ORDER BY ordinal_position;

SELECT
    order_id::INTEGER,
    item_id::INTEGER,
    quantity::INTEGER,
    price::NUMERIC(10,2)
FROM orders_items_raw;

-- 6.8.5 Validate Numerical Fields
SELECT *
FROM orders_items_raw
WHERE quantity <= 0
   OR price <= 0;

UPDATE orders_items_raw
SET
    quantity = CASE
        WHEN quantity <= 0 THEN NULL
        ELSE quantity
    END,
    price = CASE
        WHEN price <= 0 THEN NULL
        ELSE price
    END;

-- 6.8.6 Standardize Date Representations
SELECT
    order_id,
    order_date
FROM orders
ORDER BY order_date;

SELECT
    TO_DATE('21-10-2026', 'DD-MM-YYYY') AS standardized_date;

-- 6.8.7 Separate Invalid Records
SELECT *
FROM orders_items_raw
WHERE error_reason IS NOT NULL;

CREATE TABLE IF NOT EXISTS orders_items_rejected AS
SELECT *
FROM orders_items_raw
WHERE error_reason IS NOT NULL;
