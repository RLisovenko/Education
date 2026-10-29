select
    record_id,
    source_system,
    category,
    quantity,
    amount,
    status,
    quantity * amount as total_value
from {{ ref('stg_operations') }}