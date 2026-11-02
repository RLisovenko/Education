-- One row per source quality_inspection; raw input standardized in PySpark.
SELECT * FROM {{ source('manufacturing_raw', 'quality_inspections') }}
