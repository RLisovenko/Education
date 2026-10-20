/*
File: sales_analysis.sql
Performed by: R. Lisovenko
Date: 12-10-2026

Description:
Analyzes sales data stored in PostgreSQL.
The script demonstrates basic SQL queries, filtering,
aggregation, unique values, and sales summaries by product.

high-value products       → WHERE
order statistics          → COUNT / SUM / AVG / MIN / MAX
unique products           → DISTINCT
summarise by product      → GROUP BY
sales performance         → quantity * unit_price


*/


-- ============================================================
-- 1. View all sales records
-- ============================================================

SELECT *
FROM sales
ORDER BY order_id;


-- ============================================================
-- 2. Identify high-value products
-- ============================================================

SELECT
    order_id,
    customer_name,
    product,
    quantity,
    unit_price
FROM sales
WHERE unit_price > 1000
ORDER BY unit_price DESC;


-- ============================================================
-- 3. Calculate value of each order
-- ============================================================


SELECT
    order_id,
    customer_name,
    product,
    unit_price
FROM sales
ORDER BY unit_price DESC
LIMIT 3;


-- ============================================================
-- 4. Calculate order statistics
-- ============================================================

SELECT
    COUNT(*) AS total_orders,
    SUM(quantity) AS total_quantity,
    AVG(unit_price) AS average_unit_price,
    MIN(unit_price) AS minimum_unit_price,
    MAX(unit_price) AS maximum_unit_price
FROM sales;


-- ============================================================
-- 5. Find unique products
-- ============================================================

SELECT DISTINCT product
FROM sales
ORDER BY product;


-- ============================================================
-- 6. Count unique products
-- ============================================================

SELECT
    COUNT(DISTINCT product) AS unique_products
FROM sales;


-- ============================================================
-- 7. Summarize quantity sold by product
-- ============================================================

SELECT
    product,
    SUM(quantity) AS total_quantity
FROM sales
GROUP BY product
ORDER BY total_quantity DESC;


-- ============================================================
-- 8. Summarize sales value by product
-- ============================================================

SELECT
    product,
    SUM(quantity) AS total_quantity,
    SUM(quantity * unit_price) AS total_sales
FROM sales
GROUP BY product
ORDER BY total_sales DESC;


-- ============================================================
-- 9. Average price by product
-- ============================================================

SELECT
    product,
    AVG(unit_price) AS average_price
FROM sales
GROUP BY product
ORDER BY average_price DESC;


-- ============================================================
-- 10. Overall sales value
-- ============================================================

SELECT
    product,
    SUM(quantity * unit_price) AS total_sales_value
FROM sales
GROUP BY product
ORDER BY total_sales_value DESC;