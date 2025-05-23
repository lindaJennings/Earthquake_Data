import requests
import os
import boto3
import json
from pymongo import MongoClient
from datetime import datetime

BUCKET_NAME = "myseismicbucket"
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "seismic_db"
COLLECTION_NAME = "metadata_collection"

def fetch_seismic_data():
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"seismic_data_{timestamp}.mseed"

    URL = "https://service.iris.edu/fdsnws/dataselect/1/query"
    params = {
        "net": "EI",
        "sta": "DSB",
        "cha": "*",
        "start": "2024-03-06T00:00:00",
        "end": "2024-03-07T00:00:00"
    }

    response = requests.get(URL, params=params)
    
    if response.status_code == 200:
        with open(filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)
        print("✅ Data downloaded successfully as", filename)
        return filename 
    else:
        print(f"❌ Error {response.status_code}: {response.text}")
        return None

def upload_to_s3(file_name, bucket_name, object_name=None):
    s3 = boto3.client("s3")
    if object_name is None:
        object_name = file_name
    
    try:
        s3.upload_file(file_name, bucket_name, object_name)
        print(f"✅ {file_name} uploaded to S3 bucket {bucket_name}")
        return f"s3://{bucket_name}/{object_name}"
    except Exception as e:
        print(f"❌ Error uploading to S3: {e}")
        return None

def upload_metadata_to_mongo(metadata):
    try:
        client = MongoClient(MONGO_URI, tls=True, tlsAllowInvalidCertificates=True)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
        collection.insert_one(metadata)
        print(f"✅ Metadata {metadata['station']} uploaded to MongoDB")
    except Exception as e:
        print(f"❌ Error uploading to MongoDB: {e}")
    finally:
        client.close()

def process_and_store_seismic_data():
    seismic_file = fetch_seismic_data()
    if seismic_file:
        s3_url = upload_to_s3(seismic_file, BUCKET_NAME)
        if s3_url:
            stations = ["DSB"]  
            
            for station in stations:
                metadata = {
                    "station": station,
                    "network": "EI",
                    "channel": "*",
                    "start_time": "2024-03-06T00:00:00",
                    "end_time": "2024-03-07T00:00:00",
                    "s3_url": s3_url
                }
                upload_metadata_to_mongo(metadata)

if __name__ == "__main__":
    process_and_store_seismic_data()