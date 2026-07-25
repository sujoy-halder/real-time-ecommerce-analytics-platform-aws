{{ config(unique_key='payment_fact_id', incremental_strategy='merge') }}

with payments as (
    select * from {{ ref('stg_payments') }}
)

select
    {{ dbt_utils.generate_surrogate_key(['payment_date', 'customer_id']) }} as payment_fact_id,
    payment_date,
    customer_id,
    payment_events,
    authorized_payment_amount,
    _updated_at
from payments

{% if is_incremental() %}
where _updated_at > (select coalesce(max(_updated_at), '1900-01-01') from {{ this }})
{% endif %}
