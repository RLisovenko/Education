-- One row per source production_order; raw input standardized in PySpark.
SELECT * FROM {{ source('manufacturing_raw', 'production_orders') }}
