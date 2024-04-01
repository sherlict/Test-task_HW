with 
events as(select 
                date(timestamp_micros(event_time * 1000)) as event_time,
                count(distinct user_id) as total_active_user
          from `test-task-holy-water.Test_DWH.events` 
          group by 1
),
orders as(select distinct
                   date(timestamp (event_time)) as event_time,
                   transaction_id,
                   iap_item_price,
                   discount_amount,
                   fee,
                   tax
          from `test-task-holy-water.Test_DWH.orders_date` 
          where type is null and transaction_id not in(
                                                 select origin_transaction_id 
                                                 from `test-task-holy-water.Test_DWH.orders_date`
                                                 where origin_transaction_id is not null)
          order by transaction_id
),
cte as(select 
            date(timestamp (event_time)) as event_time,
            round(sum(iap_item_price - discount_amount - fee - tax), 2) as revenu
          from orders
          group by 1
)
select 
        format_date('%Y-%m', e.event_time) as month,
        revenu,
        total_active_user,
        round(revenu / total_active_user,2) as ARPU         
from events e
join cte using(event_time)
order by month
