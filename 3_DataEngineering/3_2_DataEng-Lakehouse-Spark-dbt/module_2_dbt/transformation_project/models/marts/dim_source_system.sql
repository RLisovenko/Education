select distinct
    source_system,
    case
        when source_system = 'CRM' then 'Customer Operations'
        when source_system = 'ERP' then 'Supply Operations'
        when source_system = 'API' then 'Platform Engineering'
        else 'Unknown'
    end as owner_team
from {{ ref('int_operations_enriched') }}

