-- Grain: one product.
SELECT product_id, product_name, product_family
FROM {{ ref('stg_products') }}
