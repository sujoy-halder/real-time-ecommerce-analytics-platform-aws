{{ config(materialized='table') }}

with events as (
    select * from {{ ref('stg_events') }}
    where product_id is not null
)

select
    product_id,
    min(event_time) as first_viewed_at,
    max(event_time) as last_viewed_at,
    count(*) as product_event_count
from events
group by 1
