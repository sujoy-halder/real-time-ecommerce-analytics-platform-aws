with source as (
    select * from {{ source('lakehouse_gold', 'gold_customer_orders_daily') }}
)

select
    event_date as order_date,
    customer_id,
    orders,
    gross_revenue,
    last_order_at,
    _updated_at
from source

