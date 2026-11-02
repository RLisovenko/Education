-- One row per source facilitie; raw input standardized in PySpark.
SELECT * FROM {{ source('manufacturing_raw', 'facilities') }}
