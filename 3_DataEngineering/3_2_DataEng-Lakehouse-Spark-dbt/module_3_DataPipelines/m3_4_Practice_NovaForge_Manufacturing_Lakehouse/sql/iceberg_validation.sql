-- Execute inside Spark SQL CLI, NOT in PowerShell or PostgreSQL.
SHOW NAMESPACES IN demo;
SHOW TABLES IN demo.manufacturing;
SELECT COUNT(*) FROM demo.manufacturing.manufacturing_production_metrics;
SELECT order_id, facility_id, actual_units, rejected_units, defect_rate
FROM demo.manufacturing.manufacturing_production_metrics
ORDER BY order_id;
SELECT snapshot_id, operation, committed_at
FROM demo.manufacturing.manufacturing_production_metrics.snapshots;
DESCRIBE TABLE EXTENDED demo.manufacturing.manufacturing_production_metrics;
