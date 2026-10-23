-- RetailFlow Final Project
-- Section 6.5: Explore the Data with SQL

-- 6.5.1 Filtering and Sorting Records
SELECT
    order_id,
    item_id,
    quantity,
    price
FROM orders_items
WHERE order_id = 316
ORDER BY price DESC;

SELECT *
FROM orders
WHERE customer_id = 7
ORDER BY order_date ASC;

-- 6.5.2 Calculating Totals, Averages, and Counts
SELECT
    order_id,
    SUM(quantity) AS total_quantity,
    SUM(quantity * price) AS total_sales
FROM orders_items
WHERE order_id = 316
GROUP BY order_id;

SELECT
    order_id,
    AVG(price) AS average_price
FROM orders_items
WHERE order_id = 316
GROUP BY order_id;

SELECT
    order_id,
    COUNT(*) AS item_count
FROM orders_items
WHERE order_id = 316
GROUP BY order_id;

-- 6.5.3 Grouping Data for Business Analysis
SELECT
    item_id,
    SUM(quantity) AS total_quantity,
    SUM(quantity * price) AS total_sales
FROM orders_items
WHERE order_id = 316
GROUP BY item_id
ORDER BY item_id;

-- 6.5.4 Joining Customer, Order, Product, and Transaction Information
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

-- 6.5.5 Calculating Useful Sales Metrics
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

-- 6.5.6 Using Common Table Expressions (CTEs)
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

-- 6.5.7 Using Window Functions
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
