import streamlit as st
from pymongo import MongoClient
import boto3
import os

# MongoDB Connection
mongo_uri = st.secrets["mongodb"]["MONGO_URI"]
client = MongoClient(mongo_uri)
db = client["seismic_db"]
collection = db["metadata_collection"]

# AWS S3 Connection
S3_BUCKET = "myseismicbucket"
s3 = boto3.client("s3")

# Streamlit UI
st.title("Seismic Data Query & Download")

# Search bar
station = st.text_input("Enter Station Code (e.g., DSB)")

if st.button("Search"):
    results = collection.find({"station": station}).sort("start_time", -1)  # Sort by start_time in descending order
    results_list = list(results) 

    if results_list:
        st.success(f"Seismic data found for station: {station}")
        
        # Loop through and display all results
        for result in results:
            st.write("---")  # Divider for clarity
            st.write(f"📍 **Network:** {result['network']}")
            st.write(f"📡 **Channel:** {result['channel']}")
            st.write(f"📅 **Start Time:** {result['start_time']}")
            st.write(f"📅 **End Time:** {result['end_time']}")
            
            # Get S3 file link
            s3_url = result["s3_url"]
            st.markdown(f"📥 **Download Data:** [Click Here]({s3_url})", unsafe_allow_html=True)
    else:
        st.error("No seismic data found for this station.")
