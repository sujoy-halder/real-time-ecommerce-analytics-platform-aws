{{ config(unique_key='order_fact_id', incremental_strategy='merge') }}

with orders as (
    select * from {{ ref('stg_orders') }}
)

select
    {{ dbt_utils.generate_surrogate_key(['order_date', 'customer_id']) }} as order_fact_id,
    order_date,
    customer_id,
    orders,
    gross_revenue,
    last_order_at,
    _updated_at
from orders

{% if is_incremental() %}
where _updated_at > (select coalesce(max(_updated_at), '1900-01-01') from {{ this }})
{% endif %}
