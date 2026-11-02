-- One row per source production_line; raw input standardized in PySpark.
SELECT * FROM {{ source('manufacturing_raw', 'production_lines') }}
