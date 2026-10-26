-- RetailFlow Final Project
-- Section 6.9: Reliable Reprocessing

-- 6.9.1 Evaluate repeated workflow execution
SELECT
    conname,
    contype,
    pg_get_constraintdef(oid) AS constraint_definition
FROM pg_constraint
WHERE conrelid = 'orders_items'::regclass
ORDER BY conname;

-- 6.9.2 Identify operations that could create duplicate results
SELECT
    order_id,
    item_id,
    COUNT(*) AS duplicate_count
FROM orders_items_raw
GROUP BY order_id, item_id
HAVING COUNT(*) > 1
ORDER BY order_id, item_id;

-- 6.9.3 Apply idempotent processing principles
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
  AND r.order_id IS NOT NULL
  AND r.item_id IS NOT NULL
  AND r.quantity IS NOT NULL
  AND r.quantity > 0
  AND r.price IS NOT NULL
  AND r.price > 0
ON CONFLICT (order_id, item_id) DO NOTHING;

-- 6.9.4 Identify previously processed data
SELECT DISTINCT
    r.order_id,
    r.item_id
FROM orders_items_raw r
JOIN orders_items oi
    ON r.order_id = oi.order_id
   AND r.item_id = oi.item_id
ORDER BY r.order_id, r.item_id;

SELECT
    order_id,
    item_id,
    COUNT(*) AS duplicate_count
FROM orders_items
GROUP BY order_id, item_id
HAVING COUNT(*) > 1;

-- 6.9.5 Incremental loading
SELECT
    r.order_id,
    r.item_id,
    r.quantity,
    r.price
FROM orders_items_raw r
LEFT JOIN orders_items oi
    ON r.order_id = oi.order_id
   AND r.item_id = oi.item_id
WHERE oi.order_id IS NULL
  AND r.error_reason IS NULL
  AND r.order_id IS NOT NULL
  AND r.item_id IS NOT NULL
  AND r.quantity IS NOT NULL
  AND r.quantity > 0
  AND r.price IS NOT NULL
  AND r.price > 0
ORDER BY r.order_id, r.item_id;

-- 6.9.6 Safe reprocessing
-- TRUNCATE TABLE orders_items_raw;
-- From psql while working in data/raw:
-- \copy orders_items_raw (order_id, customer_id, item_id, quantity, price, order_date) FROM 'in_order_316_customer_7.csv' DELIMITER ',' CSV HEADER;

-- 6.9.7 Verify consistent results after reprocessing
SELECT
    order_id,
    COUNT(*) AS item_count
FROM orders_items
GROUP BY order_id
ORDER BY order_id;

SELECT
    order_id,
    item_id,
    COUNT(*) AS duplicate_count
FROM orders_items
GROUP BY order_id, item_id
HAVING COUNT(*) > 1;
