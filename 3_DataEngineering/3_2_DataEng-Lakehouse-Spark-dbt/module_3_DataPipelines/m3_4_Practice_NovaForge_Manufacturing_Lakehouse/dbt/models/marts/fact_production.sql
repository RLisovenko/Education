-- Grain: one production order. Central fact used for Iceberg publication.
SELECT
    order_id, facility_id, line_id, product_id,
    production_date, production_status, planned_units,
    actual_units, rejected_units, defect_rate,
    runtime_minutes, downtime_minutes,
    production_duration_minutes, operation_count
FROM {{ ref('int_production_enriched') }}
