-- A generic singular test: rejected units cannot exceed inspected units.
SELECT inspection_id
FROM {{ ref('fact_quality_inspections') }}
WHERE rejected_units > inspected_units OR inspected_units < 0
