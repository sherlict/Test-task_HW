# Test-task_HW
Solution of a test task for the position of Analyst Engineer
1. API access is provided with data:
   URL = “https://.......”
   key {"Authorization": "......"}
2. API methods
/installs (date: str required)
/costs (date: str required, dimensions: str optional) - information about marketing costs. Available sections: location, channel, medium, campaign, keyword, ad_content, ad_group, landing_page. Dimensions are passed as a string (str) separated by commas.
/orders (date: str required) - information about payment for services by users (parquet)
/events (date: str required, next_page: str optional) - information about user actions in the application, and other information transmitted from the "client". This method returns the next_page parameter, which should be used to get the next portion of data (pagination). When receiving the last portion of data, the next_page parameter is missing
3. It is necessary to calculate the metrics of evaluation of marketing efficiency (CPI, ARPU, ROAS) in dynamics, in sections of traffic sources, etc.
