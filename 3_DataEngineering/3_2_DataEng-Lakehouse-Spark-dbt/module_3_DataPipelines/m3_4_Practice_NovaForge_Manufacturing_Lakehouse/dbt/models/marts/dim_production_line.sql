-- Grain: one production line.
SELECT line_id, facility_id, line_name
FROM {{ ref('stg_production_lines') }}
