-- Grain: one unique calendar date observed in production orders.
SELECT DISTINCT
    (EXTRACT(YEAR FROM production_date)::integer * 10000
     + EXTRACT(MONTH FROM production_date)::integer * 100
     + EXTRACT(DAY FROM production_date)::integer) AS date_key,
    production_date AS calendar_date,
    EXTRACT(YEAR FROM production_date)::integer AS calendar_year,
    EXTRACT(MONTH FROM production_date)::integer AS calendar_month,
    EXTRACT(DAY FROM production_date)::integer AS day_of_month
FROM {{ ref('stg_production_orders') }}
