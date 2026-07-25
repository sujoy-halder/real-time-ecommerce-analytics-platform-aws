{{ config(materialized='table') }}

with events as (
    select * from {{ ref('stg_events') }}
),

customers as (
    select
        customer_id,
        min(event_time) as first_seen_at,
        max(event_time) as last_seen_at,
        count(*) as total_events
    from events
    group by 1
)

select
    customer_id,
    first_seen_at,
    last_seen_at,
    total_events
from customers
