-- One row per source product; raw input standardized in PySpark.
SELECT * FROM {{ source('manufacturing_raw', 'products') }}
