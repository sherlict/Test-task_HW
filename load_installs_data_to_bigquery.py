import requests
import json
from google.cloud import bigquery
from datetime import datetime, timedelta

URL = "https://......"
HEADERS = {
    "Authorization": "......."
}

def fetch_data_from_api(date):
    params = {"date": date}
    
    response = requests.get(URL, headers=HEADERS, params=params)
    
    if response.status_code == 200:
        data = response.json()
        
        # Convert the "records" string to a list of dictionaries
        data['records'] = json.loads(data['records'].replace("\\", ""))
        
        return data
    else:
        print(f"Failed to fetch data: {response.status_code}")
        print(f"Response content: {response.text}")
        return None

def load_data_to_bigquery(data, project_id, dataset_id, table_id):
    client = bigquery.Client(project=project_id)
    table_ref = client.dataset(dataset_id).table(table_id)
    table = client.get_table(table_ref)

    # We check whether the table has a defined scheme
    if not table.schema:
        print(f"Table {project_id}.{dataset_id}.{table_id} does not have a schema defined.")
        return

    errors = client.insert_rows_json(table, data)

    if errors == []:
        print(f"Data successfully loaded into {project_id}:{dataset_id}.{table_id}")
    else:
        print(f"Encountered errors while inserting rows: {errors}")

if __name__ == "__main__":
    
    # Get the current date
    current_date = datetime.now()
    previous_date = current_date - timedelta(days=1)
    
    # Format the date to the desired format (YYYY-MM-DD)
    date_to_fetch = previous_date.strftime('%Y-%m-%d')
    
    data = fetch_data_from_api(date_to_fetch)
    
    if data:
        print("Fetched data successfully:")
        print(json.dumps(data, indent=4))

        project_id = "test-task-holy-water"
        dataset_id = "Test_DWH"
        table_id = "installs_data"
        
        load_data_to_bigquery(data['records'], project_id, dataset_id, table_id)
