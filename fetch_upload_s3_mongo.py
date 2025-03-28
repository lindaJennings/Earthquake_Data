import requests
import os
import boto3
import json
from pymongo import MongoClient

def fetch_seismic_data():
# URL with correct parameters
    URL = "https://service.iris.edu/fdsnws/dataselect/1/query"

    params = {
        "net": "EI",
        "sta": "DSB",
        "cha": "BHZ",
        "start": "2024-03-01T00:00:00",
        "end": "2024-03-02T00:00:00"
    }

# Send the GET request
    response = requests.get(URL, params=params)

# Save the file if successful
    if response.status_code == 200:
        with open("seismic_data.mseed", "wb") as f:
         f.write(response.content)
        print("✅ Data downloaded successfully as seismic_data.mseed")
    else:
     print(f"❌ Error {response.status_code}: {response.text}")

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

def upload_metadata_to_mongo(metadata, mongo_uri, db_name, collection_name):
    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]
    try:
        collection.insert_one(metadata)
        print("✅ Metadata uploaded to MongoDB")
    except Exception as e:
        print(f"❌ Error uploading to MongoDB: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    seismic_file = fetch_seismic_data()
    if seismic_file:
        s3_url = upload_to_s3(seismic_file, "myseismicbucket")
        if s3_url:
            metadata = {
                "station": "DSB",
                "network": "EI",
                "channel": "BHZ",
                "start_time": "2024-03-01T00:00:00",
                "end_time": "2024-03-02T00:00:00",
                "s3_url": s3_url
            }
            upload_metadata_to_mongo(metadata, os.getenv('MONGO_URI'), "seismic_db", "metadata_collection")