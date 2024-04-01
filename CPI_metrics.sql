with 
costs as(select 
                format_date('%y-%m',date(timestamp (load_date))) as load_date,
                location,
                channel, 
                medium, 
                campaign, 
                keyword,
                ad_content,
                ad_group,
                landing_page,
                round(sum(cost), 2) as cost
        from `test-task-holy-water.Test_DWH.costs` 
        group by 1,2,3,4,5,6,7,8,9
),
installs as(select
                  format_date('%y-%m',date(timestamp (install_time))) as install_date,   
                  alpha_2,
                  channel,
                  medium,
                  campaign,
                  keyword,
                  ad_content,
                  ad_group,
                  landing_page,
                  count(distinct marketing_id) as count_installations
           from `test-task-holy-water.Test_DWH.installs_data`
           group by 1,2,3,4,5,6,7,8,9
)
select i.install_date,
       c.location,
       i.channel,
       i.medium,
       i.campaign,
       i.keyword,
       i.ad_content,
       i.ad_group,
       i.landing_page,
       round(sum(c.cost) / count(i.count_installations), 2) as CPI
from installs i
join costs c on i.install_date = c.load_date
                and i.alpha_2 = c.location
                and i.channel = c.channel
                and i.medium = c.medium
                and i.campaign = c.campaign
                and i.keyword = c.keyword     
                and i.ad_content = c.ad_content  
                and i.ad_group = c.ad_group 
                and i.landing_page = c.landing_page 
                -- uncomment if you want to have all values in rows (not None or Undefined)
                --and i.keyword <> 'None' and c.keyword <> 'None'
                --and i.ad_content <> 'None' and c.ad_content <> 'None'
                --and i.ad_group <> 'None' and c.ad_group <> 'None'
                --and i.landing_page <> 'Undefined' and c.landing_page <> 'Undefined'
group by 1,2,3,4,5,6,7,8,9   
order by 1,2,3,4,5,6,7,8,9
