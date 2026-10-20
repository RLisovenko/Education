/*
File: scenario_4_structured_workflow.sql
Performed by: R. Lisovenko
Date: 20-10-2026

Scenario 4:
Building a Structured Data Processing Workflow

Description:
Loads raw shipment data, validates data quality,
creates a separate cleaning layer, fixes detected issues,
removes duplicates, validates the final dataset,
calculates summary statistics, and exports processed data.
*/


-- ============================================================
-- 1. Create raw shipment table
-- ============================================================

CREATE TABLE shipments_raw (
    shipment_id VARCHAR(20),
    origin_hub VARCHAR(100),
    destination_hub VARCHAR(100),
    package_weight NUMERIC(10,2),
    delivery_status VARCHAR(50),
    shipment_date DATE
);


-- ============================================================
-- 2. Load source CSV into raw table
-- ============================================================

\copy shipments_raw FROM 'data/raw/daily_shipments.csv' DELIMITER ',' CSV HEADER;


-- ============================================================
-- 3. Check number of loaded records
-- ============================================================

SELECT COUNT(*) AS loaded_shipments
FROM shipments_raw;


-- ============================================================
-- 4. Initial data-quality validation
-- ============================================================

SELECT
    COUNT(*) AS total_records,
    SUM(CASE
        WHEN destination_hub IS NULL OR destination_hub = ''
        THEN 1 ELSE 0
    END) AS missing_destinations,

    SUM(CASE
        WHEN delivery_status IS NULL OR delivery_status = ''
        THEN 1 ELSE 0
    END) AS missing_statuses,

    SUM(CASE
        WHEN package_weight <= 0
        THEN 1 ELSE 0
    END) AS invalid_weights

FROM shipments_raw;


-- ============================================================
-- 5. Check duplicate shipment IDs
-- ============================================================

SELECT
    shipment_id,
    COUNT(*) AS duplicate_count
FROM shipments_raw
GROUP BY shipment_id
HAVING COUNT(*) > 1;


-- ============================================================
-- 6. Create separate working / clean table
-- Raw data remains unchanged.
-- ============================================================

CREATE TABLE shipments_clean AS
SELECT *
FROM shipments_raw;


-- ============================================================
-- 7. Verify number of rows in working table
-- ============================================================

SELECT COUNT(*) AS working_rows
FROM shipments_clean;


-- ============================================================
-- 8. Replace missing destination hubs
-- ============================================================

UPDATE shipments_clean
SET destination_hub = 'Unknown Hub'
WHERE destination_hub IS NULL
   OR destination_hub = '';


-- ============================================================
-- 9. Replace missing delivery statuses
-- ============================================================

UPDATE shipments_clean
SET delivery_status = 'Unknown'
WHERE delivery_status IS NULL
   OR delivery_status = '';


-- ============================================================
-- 10. Correct negative package weights
-- ABS() converts negative values to positive values.
-- ============================================================

UPDATE shipments_clean
SET package_weight = ABS(package_weight)
WHERE package_weight < 0;


-- ============================================================
-- 11. Correct zero package weights
-- ============================================================

UPDATE shipments_clean
SET package_weight = 1
WHERE package_weight = 0;


-- ============================================================
-- 12. Standardize origin hub names
-- TRIM() removes spaces at the beginning/end.
-- INITCAP() converts names to title case.
-- ============================================================

UPDATE shipments_clean
SET origin_hub = INITCAP(TRIM(origin_hub));


-- ============================================================
-- 13. Standardize destination hub names
-- ============================================================

UPDATE shipments_clean
SET destination_hub = INITCAP(TRIM(destination_hub));


-- ============================================================
-- 14. Remove duplicate shipments
-- Keep one physical row for each shipment_id.
-- ============================================================

DELETE FROM shipments_clean
WHERE ctid NOT IN (
    SELECT MIN(ctid)
    FROM shipments_clean
    GROUP BY shipment_id
);


-- ============================================================
-- 15. Verify duplicate removal
-- ============================================================

SELECT
    shipment_id,
    COUNT(*) AS duplicate_count
FROM shipments_clean
GROUP BY shipment_id
HAVING COUNT(*) > 1;


-- ============================================================
-- 16. Final data-quality validation
-- ============================================================

SELECT
    COUNT(*) AS final_records,

    SUM(CASE
        WHEN destination_hub IS NULL OR destination_hub = ''
        THEN 1 ELSE 0
    END) AS missing_destinations,

    SUM(CASE
        WHEN delivery_status IS NULL OR delivery_status = ''
        THEN 1 ELSE 0
    END) AS missing_statuses,

    SUM(CASE
        WHEN package_weight <= 0
        THEN 1 ELSE 0
    END) AS invalid_weights

FROM shipments_clean;


-- ============================================================
-- 17. Shipment count by delivery status
-- ============================================================

SELECT
    delivery_status,
    COUNT(*) AS shipment_count
FROM shipments_clean
GROUP BY delivery_status
ORDER BY shipment_count DESC;


-- ============================================================
-- 18. Shipment summary by destination hub
-- ============================================================

SELECT
    destination_hub,
    COUNT(*) AS shipment_count,
    SUM(package_weight) AS total_weight
FROM shipments_clean
GROUP BY destination_hub
ORDER BY shipment_count DESC, destination_hub;


-- ============================================================
-- 19. Overall shipment statistics
-- ============================================================

SELECT
    COUNT(*) AS total_shipments,
    SUM(package_weight) AS total_package_weight,
    AVG(package_weight) AS average_package_weight
FROM shipments_clean;


-- ============================================================
-- 20. View final cleaned dataset
-- ============================================================

SELECT *
FROM shipments_clean
ORDER BY shipment_id;


-- ============================================================
-- 21. Export processed data to CSV
-- ============================================================

\copy (
    SELECT *
    FROM shipments_clean
    ORDER BY shipment_id
) TO 'data/processed/processed_shipments.csv' DELIMITER ',' CSV HEADER;