import time
import pandas as pd
import os
from datetime import datetime
from dotenv import load_dotenv
from azure.storage.filedatalake import DataLakeServiceClient

# CONFIGURATION
STORAGE_ACCOUNT_NAME = "dota2lakehouse"  # Storage Account Name
STORAGE_ACCOUNT_KEY = os.getenv("AZURE_STORAGE_ACCOUNT_KEY")  # Load from .env file for security
CONTAINER_NAME = "data"
DIRECTORY_NAME = "bronze"                  # The folder where streamed files will land
LOCAL_SOURCE_FILE = "main_metadata.csv"

# CONNECTION SETUP
def get_service_client():
    account_url = f"https://dota2lakehouse.dfs.core.windows.net"
    try:
        service_client = DataLakeServiceClient(account_url=account_url, credential=STORAGE_ACCOUNT_KEY)
        return service_client
    except Exception as e:
        print(f"Connection Failed: {e}")
        return None

# STREAMING LOGIC
def stream_data():
    print(f"--- Starting Streaming Simulation using {LOCAL_SOURCE_FILE} ---")
    
    # Check if file exists locally
    if not os.path.exists(LOCAL_SOURCE_FILE):
        print(f"Error: Could not find {LOCAL_SOURCE_FILE} in the current folder.")
        return

    # Load the data
    print("Loading dataset...")
    df = pd.read_csv(LOCAL_SOURCE_FILE)
    print(f"Loaded {len(df)} rows. Starting stream...")

    # Connect to Azure
    service_client = get_service_client()
    if not service_client: return
    
    file_system_client = service_client.get_file_system_client(file_system=CONTAINER_NAME)
    directory_client = file_system_client.get_directory_client(DIRECTORY_NAME)

    # Simulation Settings
    BATCH_SIZE = 5      # Number of matches to send at once
    SLEEP_TIME = 3      # Seconds to wait between uploads (Simulate delay)

    # Loop through the dataframe in chunks
    for i in range(0, 50, BATCH_SIZE):  # LIMIT: Only running for 50 rows to save credits
        
        # 1. Get a "Mini-Batch" of data
        chunk = df.iloc[i:i+BATCH_SIZE]
        
        # 2. Convert to JSON (common format for streaming)
        json_data = chunk.to_json(orient='records')
        
        # 3. Generate a unique filename with Timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"raw_matches_{timestamp}.json"
        
        # 4. Upload to Azure
        try:
            print(f"Uploading {file_name}...", end=" ")
            file_client = directory_client.get_file_client(file_name)
            file_client.create_file()
            file_client.append_data(data=json_data, offset=0, length=len(json_data))
            file_client.flush_data(len(json_data))
            print("Done.")
        except Exception as e:
            print(f"Upload Error: {e}")

        # 5. Wait (Simulate real-time gap)
        time.sleep(SLEEP_TIME)

    print("\n--- Simulation Complete ---")

if __name__ == "__main__":
    stream_data()