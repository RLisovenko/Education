-- Grain: facility and calendar day; trusted reporting-ready metrics.
SELECT
    facility_id, production_date,
    COUNT(*)::integer AS production_orders,
    SUM(actual_units)::bigint AS total_units_produced,
    SUM(rejected_units)::bigint AS total_rejected_units,
    SUM(runtime_minutes)::bigint AS total_runtime_minutes,
    SUM(downtime_minutes)::bigint AS total_downtime_minutes,
    CASE WHEN SUM(actual_units) > 0
         THEN ROUND(SUM(rejected_units)::numeric / SUM(actual_units)::numeric, 4)
         ELSE 0.0 END AS weighted_defect_rate
FROM {{ ref('fact_production') }}
GROUP BY facility_id, production_date
