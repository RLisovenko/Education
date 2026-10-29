select
    record_id,
    source_system,
    category,
    quantity,
    amount,
    total_value,
    case
        when status = 'ACTIVE' then 't'
        else 'f'
    end as is_active
from {{ ref('int_operations_enriched') }}