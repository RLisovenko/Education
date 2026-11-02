-- Grain: one machine.
SELECT machine_id, line_id, machine_type
FROM {{ ref('stg_machines') }}
