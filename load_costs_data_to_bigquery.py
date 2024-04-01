import requests
from google.cloud import bigquery
from datetime import datetime, timedelta
import io
import csv

# Function to get data from API
def fetch_data_from_api(date, dimensions=None):
    url = "https://......."
    
    headers = {
        "Authorization": "................"
    }
    
    # Date conversion to "YYYY-MM-DD" string format
    date_str = date.strftime('%Y-%m-%d')

    params = {
        "date": date_str
    }
    
    if dimensions:
        params["dimensions"] = dimensions
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = io.StringIO(response.text)
        reader = csv.DictReader(data, delimiter='\t')
        
        # Adding a load_date field to each record
        new_data = []
        for row in reader:
            row['load_date'] = date.strftime('%Y-%m-%d %H:%M:%S')
            new_data.append(row)
        
        return new_data

# A function for loading data into BigQuery
def load_data_to_bigquery(data, dataset_id, table_id, project_id):
    client = bigquery.Client(project=project_id)
    dataset_ref = client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)
    
    table = client.get_table(table_ref)
    
    errors = client.insert_rows_json(table, data)
    
# The main code
if __name__ == "__main__":
    yesterday = datetime.now() - timedelta(1)  # Отримання дати попереднього дня
    dimensions = "location,channel,medium,campaign,keyword,ad_content,ad_group,landing_page"  # Встановіть потрібні розрізи   
    data = fetch_data_from_api(yesterday, dimensions)  # Передача дати без перетворення в рядок
    
    if data:
        project_id = "test-task-holy-water"
        dataset_id = "Test_DWH"
        table_id = "costs"
        
        load_data_to_bigquery(data, dataset_id, table_id, project_id)
