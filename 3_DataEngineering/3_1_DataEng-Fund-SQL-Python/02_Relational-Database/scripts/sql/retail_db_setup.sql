/*
File: retail_db_setup.sql
Performed by: R. Lisovenko
Date: 12-10-2026

Description:
Creates the retail database and sales table,
inserts sample sales records, and runs basic checks and queries.
*/

-- =========================================================
-- 1. Create database
-- =========================================================

CREATE DATABASE retail_db;


-- =========================================================
-- 2. Connect to database
-- psql command
-- =========================================================

\c retail_db


-- =========================================================
-- 3. Create sales table
-- =========================================================

CREATE TABLE sales (
    order_id INTEGER PRIMARY KEY,
    customer_name VARCHAR(100),
    product VARCHAR(100),
    quantity INTEGER,
    unit_price NUMERIC(10,2),
    order_date DATE
);


-- =========================================================
-- 4. Show tables
-- psql command
-- =========================================================

\dt


-- =========================================================
-- 5. Show sales table structure
-- psql command
-- =========================================================

\d sales


-- =========================================================
-- 6. Insert sample data
-- =========================================================

INSERT INTO sales
(order_id, customer_name, product, quantity, unit_price, order_date)
VALUES
(1001, 'Alice Johnson', 'Laptop', 1, 75000.00, '2026-08-01'),
(1002, 'Rahul Sharma', 'Mouse', 2, 800.00, '2026-08-02'),
(1003, 'Priya Nair', 'Keyboard', 1, 1500.00, '2026-08-02');


-- =========================================================
-- 7. Display all records
-- =========================================================

SELECT * FROM sales;


-- =========================================================
-- 8. Example filtered query
-- =========================================================

SELECT *
FROM sales
WHERE unit_price > 1000;