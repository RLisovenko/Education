-- Grain: one production order. Pre-aggregate 1:N events BEFORE joining to avoid double-counting.
WITH operations AS (
    SELECT order_id,
           COUNT(*)::integer AS operation_count,
           COALESCE(SUM(run_minutes), 0)::integer AS runtime_minutes,
           COALESCE(SUM(downtime_minutes), 0)::integer AS downtime_minutes
    FROM {{ ref('stg_machine_operations') }}
    GROUP BY order_id
), inspections AS (
    SELECT order_id,
           COALESCE(SUM(inspected_units), 0)::integer AS actual_units,
           COALESCE(SUM(rejected_units), 0)::integer AS rejected_units
    FROM {{ ref('stg_quality_inspections') }}
    GROUP BY order_id
)
SELECT
    p.order_id,
    p.facility_id,
    p.line_id,
    p.product_id,
    p.production_date,
    p.production_status,
    p.planned_units,
    COALESCE(q.actual_units, 0)::integer AS actual_units,
    COALESCE(q.rejected_units, 0)::integer AS rejected_units,
    CASE WHEN COALESCE(q.actual_units, 0) = 0 THEN 0.0
         ELSE ROUND(q.rejected_units::numeric / q.actual_units::numeric, 4)
    END AS defect_rate,
    COALESCE(o.runtime_minutes, 0)::integer AS runtime_minutes,
    COALESCE(o.downtime_minutes, 0)::integer AS downtime_minutes,
    (COALESCE(o.runtime_minutes, 0) + COALESCE(o.downtime_minutes, 0))::integer
        AS production_duration_minutes,
    COALESCE(o.operation_count, 0)::integer AS operation_count
FROM {{ ref('stg_production_orders') }} p
LEFT JOIN operations o ON p.order_id = o.order_id
LEFT JOIN inspections q ON p.order_id = q.order_id
