import os
import json
import pymongo

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI")  
DB_NAME = "Earthquake_Data"
COLLECTION_NAME = "DSB"

client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Load JSON data
with open("seismic_data.json", "r") as f:
    seismic_data = json.load(f)

# Check if data already exists (based on starttime)
existing_entry = collection.find_one({"starttime": seismic_data[0]["starttime"]})

if existing_entry:
    print("Data already uploaded, skipping...")
else:
    collection.insert_many(seismic_data)
    print("New seismic data uploaded to MongoDB!")
