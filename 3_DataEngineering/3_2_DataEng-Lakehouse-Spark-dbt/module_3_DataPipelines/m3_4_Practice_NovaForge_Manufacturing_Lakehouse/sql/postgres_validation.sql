-- Run inside PostgreSQL: psql -U novaforge -d manufacturing -f /path/to/file
SELECT 'orders' AS dataset, COUNT(*) FROM raw.production_orders
UNION ALL SELECT 'operations', COUNT(*) FROM raw.machine_operations
UNION ALL SELECT 'inspections', COUNT(*) FROM raw.quality_inspections;
SELECT facility_id, production_date, production_orders, total_units_produced,
       total_rejected_units, weighted_defect_rate
FROM marts.mart_production_daily
ORDER BY facility_id, production_date;
SELECT order_id, defect_rate, runtime_minutes, downtime_minutes
FROM marts.fact_production
ORDER BY order_id;
