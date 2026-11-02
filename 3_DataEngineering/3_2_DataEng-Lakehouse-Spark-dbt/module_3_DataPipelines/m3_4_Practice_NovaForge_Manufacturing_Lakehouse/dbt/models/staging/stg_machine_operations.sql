-- One row per source machine_operation; raw input standardized in PySpark.
SELECT * FROM {{ source('manufacturing_raw', 'machine_operations') }}
