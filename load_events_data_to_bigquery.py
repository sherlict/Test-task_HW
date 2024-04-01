import json
import requests
from google.cloud import bigquery
from datetime import datetime, timedelta

# Function to get data from API
def fetch_events_data_from_api(date, next_page=None):
    url = "https://......"
    
    headers = {
        "Authorization": "......."
    }
    
    params = {
        "date": date
    }
    
    if next_page:
        params["next_page"] = next_page
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        print(f"API request failed with status code {response.status_code}")
        return None, None
    
    try:
        json_data = json.loads(response.text)
        data = json_data.get("data", [])
        next_page = json_data.get("next_page")
        return data, next_page
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None, None

# A function for loading data into BigQuery
def load_data_to_bigquery(data, project_id, dataset_id, table_id):
    client = bigquery.Client(project=project_id)
    dataset_ref = client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)
    
    try:
        job = client.load_table_from_json(data, table_ref)
        job.result()
        print(f"Data successfully loaded into {project_id}.{dataset_id}.{table_id}")
    except Exception as e:
        print(f"Error loading data to BigQuery: {e}")

# The main code
if __name__ == "__main__":
    # Get the current date
    current_date = datetime.now()

    # Get the previous day's date
    previous_date = current_date - timedelta(days=1)

    # Convert date to string in "YYYY-MM-DD" format
    date = previous_date.strftime('%Y-%m-%d')
    
    next_page = None
    
    all_data = []
    
    while True:
        data, next_page = fetch_events_data_from_api(date, next_page)
        
        if data:
            all_data.extend(data)
        
        if not next_page:
            break

    project_id = "test-task-holy-water"
    dataset_id = "Test_DWH"
    table_id = "events_data"
        
    load_data_to_bigquery(all_data, project_id, dataset_id, table_id)
