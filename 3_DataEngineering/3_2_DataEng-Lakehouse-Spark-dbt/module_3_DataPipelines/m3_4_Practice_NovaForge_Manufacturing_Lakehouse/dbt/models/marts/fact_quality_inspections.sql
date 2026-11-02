-- Grain: one inspection event.
SELECT
    q.inspection_id, q.order_id, o.facility_id, o.line_id,
    q.inspected_units, q.rejected_units,
    CASE WHEN q.inspected_units > 0
         THEN ROUND(q.rejected_units::numeric / q.inspected_units::numeric, 4)
         ELSE 0.0 END AS defect_rate,
    q.inspection_at
FROM {{ ref('stg_quality_inspections') }} q
INNER JOIN {{ ref('stg_production_orders') }} o ON q.order_id = o.order_id
