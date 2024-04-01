# Test-task_HW
Solution of a test task for the position of Analyst Engineer
1. API access is provided with data:
   URL = “https://.......”
   key {"Authorization": "......"}
2. API methods
- /installs (date: str required)
- /costs (date: str required, dimensions: str optional) - information about marketing costs. Available sections: location, channel, medium, campaign, keyword, ad_content, ad_group, landing_page. Dimensions are passed as a string (str) separated by commas.
- /orders (date: str required) - information about payment for services by users (parquet)
- /events (date: str required, next_page: str optional) - information about user actions in the application, and other information transmitted from the "client". This method returns the next_page parameter, which should be used to get the next portion of data (pagination). When receiving the last portion of data, the next_page parameter is missing
3. It is necessary to calculate the metrics of evaluation of marketing efficiency (CPI, ARPU, ROAS) in dynamics, in sections of traffic sources, etc.


  Solution:
In Google Cloud Platform, tables are created in BigQuery:
- costs
- events
- installs
- orders
In CLOUD SHELL Editor, Python scripts are created for downloading data via API.
- load_costs_data_to_bigquery.py
- load_installs_data_to_bigquery.py
- load_events_data_to_bigquery.py
- load_orders_date_to_bigquery.py
Tasks for downloading 4 scripts are created in crontab:
- 0 minutes
- 02 hours
- every day of the month
- every month
- every day of the week
In BigQuery, SQL queries for calculating metrics are created:
- ROAS
- ARPU
- CPI

  Conclusions:
1. The CPI (Cost Per Install) metric is an indicator that indicates the cost of attracting one new user to a mobile application through advertising campaigns. Calculated by month. It varies from 0.05 to 29.95.
Low CPI (0.05): This indicates that the cost of acquiring a new user is very low. This can be very useful for mobile apps with a limited marketing budget. However, a low cost can also indicate low quality users or low effectiveness of advertising campaigns.
High CPI (29.95): A high CPI indicates a high cost of acquiring a new user. This may be acceptable if the app monetizes well and users are long-term and active. However, high CPI can be a problem for startups or applications with a limited budget.
2. An ARPU (Average Revenue Per User) metric of 0.37 for a mobile app can be considered a normal indicator, but it all depends on the context and comparison with similar apps or industry standards. Calculated by month.
3. ROAS (Return on Advertising Spend) is a metric that measures the return on advertising spend. This is an important indicator for evaluating the effectiveness of advertising campaigns, especially for mobile applications. Calculated by month.
- Comparison with CPI: If your ROAS is higher than CPI (Cost Per Install), this may indicate that the ad campaign appears to be profitable.
- Seasonality and Trends: ROAS may fluctuate based on seasonal fluctuations, promotions and other market factors. It is important to analyze trends and adjust strategies according to these changes.
- Continuous analysis and optimization: It is important to regularly analyze ad campaigns, test different strategies and optimize budgets to achieve the best ROAS.
4. Based on this data, you can make visualizations of changes in metrics over time. The easiest way to do this is in Looker studio. It's from the Google ecosystem, so downloading data is quick and easy. But it is free.
