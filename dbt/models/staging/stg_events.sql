with source as (
    select * from {{ source('lakehouse_gold', 'silver_events') }}
)

select
    event_id,
    event_type,
    event_time,
    event_date,
    customer_id,
    order_id,
    product_id,
    session_id,
    order_amount,
    payment_amount,
    payload,
    _ingested_at
from source

