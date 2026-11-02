-- One row per source machine; raw input standardized in PySpark.
SELECT * FROM {{ source('manufacturing_raw', 'machines') }}
