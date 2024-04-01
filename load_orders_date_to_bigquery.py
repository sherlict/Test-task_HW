import requests
import pyarrow.parquet as pq
import pandas as pd
from datetime import datetime, timedelta
from google.cloud import bigquery

# Function to get data from API
def fetch_orders_data_from_api():
    url = "......."
    
    headers = {
        "Authorization": "......"
    }
    
    yesterday = datetime.now() - timedelta(1)
    date = yesterday.strftime('%Y-%m-%d')

    params = {
        "date": date
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        print(f"API request failed with status code {response.status_code}")
        return None
    
    try:
        data = pq.read_table(io.BytesIO(response.content)).to_pandas()
        
        if data.shape[0] == 0:
            print("Empty data received from API.")
            return None
        
        data = data.rename(columns={
            "iap_item.name": "iap_item_name",
            "iap_item.price": "iap_item_price",
            "discount.code": "discount_code",
            "discount.amount": "discount_amount"
        })
        
        return data
    except Exception as e:
        print(f"Error reading Parquet data: {e}")
        return None

# A function for loading data into BigQuery
def load_data_to_bigquery(data, project_id, dataset_id, table_id):
    client = bigquery.Client(project=project_id)
    dataset_ref = client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)
    
    try:
        job = client.load_table_from_dataframe(data, table_ref)
        job.result()
        print(f"Data successfully loaded into {project_id}.{dataset_id}.{table_id}")
    except Exception as e:
        print(f"Error loading data to BigQuery: {e}")

# The main code
if __name__ == "__main__":
    data = fetch_orders_data_from_api()
    
    if data is not None:
        project_id = "test-task-holy-water"
        dataset_id = "Test_DWH"
        table_id = "orders_date"
        
        load_data_to_bigquery(data, project_id, dataset_id, table_id)
    else:
        print("No data received.")
