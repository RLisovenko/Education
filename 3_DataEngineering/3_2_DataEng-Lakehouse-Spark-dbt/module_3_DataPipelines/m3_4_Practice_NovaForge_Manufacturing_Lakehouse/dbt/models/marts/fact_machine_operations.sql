-- Grain: one machine operation event.
SELECT
    op.operation_id, op.order_id, op.machine_id, m.line_id,
    o.facility_id, op.operation_at, op.run_minutes,
    op.downtime_minutes, op.energy_consumption_kwh
FROM {{ ref('stg_machine_operations') }} op
INNER JOIN {{ ref('stg_machines') }} m ON op.machine_id = m.machine_id
INNER JOIN {{ ref('stg_production_orders') }} o ON op.order_id = o.order_id
