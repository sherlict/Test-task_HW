with 
events as(
select
          user_id, 
          alpha_2, 
          transaction_id,
          user_params.marketing_id as marketing_id,
          format_date('%Y-%m', date(timestamp_micros(event_time * 1000))) as event_month 
    from `test-task-holy-water.Test_DWH.events`,
    unnest([user_params]) as user_params
),
orders as(
select distinct
           format_date('%Y-%m', date(timestamp (event_time))) as event_month,
           transaction_id,
           round(iap_item_price - discount_amount - fee - tax, 2) as revenu
    from `test-task-holy-water.Test_DWH.orders_date` 
    where type is null 
          and transaction_id not in(
                                    select origin_transaction_id 
                                    from `test-task-holy-water.Test_DWH.orders_date`
                                    where origin_transaction_id is not null)
),
costs as(
select 
        format_date('%Y-%m', date(timestamp (load_date))) as load_month,
        location,
        channel, 
        medium, 
        campaign, 
        keyword,
        ad_content,
        ad_group,
        landing_page,
        round(sum(cost), 2) as total_cost
    from `test-task-holy-water.Test_DWH.costs` 
    group by 1,2,3,4,5,6,7,8,9
),
installs as(
select 
        format_date('%Y-%m', date(timestamp (install_time))) as install_month,
        marketing_id,
        alpha_2,
        channel,
        medium,
        campaign,
        keyword,
        ad_content,
        ad_group,
        landing_page
    from `test-task-holy-water.Test_DWH.installs_data`
)
select 
      e.event_month,
      e.alpha_2 as location, 
      i.channel,
      i.medium,
      i.campaign,
      i.keyword,
      i.ad_content,
      i.ad_group,
      i.landing_page,
      sum(od.revenu) as total_revenu,
      sum(c.total_cost) as total_cost,
      round(sum(od.revenu) / sum(c.total_cost), 2) as ROAS
from events e
join orders od on e.transaction_id = od.transaction_id 
               and e.event_month = od.event_month
join installs i on e.marketing_id = i.marketing_id
join costs c on c.load_month = e.event_month
            and c.channel = i.channel
            and c.medium = i.medium
            and c.campaign = i.campaign
            and c.keyword = i.keyword
            and c.ad_content = i.ad_content
            and c.ad_group = i.ad_group
            and c.landing_page = i.landing_page
            -- uncomment if you want to have all values in rows (not None or Undefined)
                --and i.keyword <> 'None' and c.keyword <> 'None'
                --and i.ad_content <> 'None' and c.ad_content <> 'None'
                --and i.ad_group <> 'None' and c.ad_group <> 'None'
                --and i.landing_page <> 'Undefined' and c.landing_page <> 'Undefined'
group by 1,2,3,4,5,6,7,8,9
order by 1,2,3,4,5,6,7,8,9
limit 100
