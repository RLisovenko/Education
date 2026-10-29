select
    record_id,
    upper(trim(source_system)) as source_system,
    initcap(trim(category)) as category,
    case
        when quantity <= 0 then 1
        else quantity
    end as quantity,
    coalesce(amount, 0) as amount,
    upper(trim(status)) as status
from {{ source('raw', 'operations_raw') }}