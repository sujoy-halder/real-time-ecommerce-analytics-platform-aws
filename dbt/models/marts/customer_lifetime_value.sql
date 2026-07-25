{{ config(materialized='table') }}

select
    customer_id,
    sum(gross_revenue) as lifetime_value,
    sum(orders) as lifetime_orders,
    max(last_order_at) as last_order_at
from {{ ref('fact_orders') }}
group by 1
