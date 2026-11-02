-- A generic singular test: should return zero rows.
SELECT order_id
FROM {{ ref('fact_production') }}
WHERE actual_units < 0 OR rejected_units < 0
   OR defect_rate < 0 OR defect_rate > 1
   OR downtime_minutes < 0 OR runtime_minutes < 0
