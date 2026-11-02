-- One row per source maintenance_record; raw input standardized in PySpark.
SELECT * FROM {{ source('manufacturing_raw', 'maintenance_records') }}
