import streamlit as st
from pymongo import MongoClient
import boto3
import os

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
    st.write(f"🔍 Searching for seismic data at station: **{station}** ...")
    
    results = list(collection.find({"station": station}).sort("start_time", -1))  # Convert cursor to list

    if results:
        st.success(f"✅ Found {len(results)} records for station: {station}")

        # Loop through and display all metadata
        for i, result in enumerate(results):
            st.write("---")  # Divider for clarity
            st.subheader(f"📁 Record {i + 1}")
            st.write(f"📍 **Network:** {result.get('network', 'N/A')}")
            st.write(f"📡 **Channel:** {result.get('channel', 'N/A')}")
            st.write(f"📅 **Start Time:** {result.get('start_time', 'N/A')}")
            st.write(f"📅 **End Time:** {result.get('end_time', 'N/A')}")

            # Get S3 file link
            s3_url = result.get("s3_url", "#")
            if s3_url != "#":
                st.markdown(f"📥 **Download Data:** [Click Here]({s3_url})", unsafe_allow_html=True)
            else:
                st.warning("No S3 URL available for this record.")
    else:
        st.error("❌ No seismic data found for this station.")