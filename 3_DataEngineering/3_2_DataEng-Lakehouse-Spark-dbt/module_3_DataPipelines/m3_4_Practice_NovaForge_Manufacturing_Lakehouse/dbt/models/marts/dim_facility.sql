-- Grain: one manufacturing facility.
SELECT facility_id, facility_name, region
FROM {{ ref('stg_facilities') }}
