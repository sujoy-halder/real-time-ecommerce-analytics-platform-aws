with source as (
    select * from {{ source('lakehouse_gold', 'gold_customer_payments_daily') }}
)

select
    event_date as payment_date,
    customer_id,
    payment_events,
    authorized_payment_amount,
    _updated_at
from source

