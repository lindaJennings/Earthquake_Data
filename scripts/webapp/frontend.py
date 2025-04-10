from datetime import datetime
import streamlit as st
from pymongo import MongoClient
import boto3
import os

mongo_uri = st.secrets["mongodb"]["MONGO_URI"]
client = MongoClient(mongo_uri)
db = client["seismic_db"]
collection = db["metadata_collection"]

S3_BUCKET = "myseismicbucket"
s3 = boto3.client("s3")

st.title("Seismic Data Query & Download")

station = st.text_input("Enter Station Code (e.g., DSB)")

start_time = st.date_input("Start date"); end_time = st.date_input("End date")

if st.button("Search"):
    start_iso = datetime.combine(start_time, datetime.min.time()).isoformat()
    end_iso = datetime.combine(end_time, datetime.max.time()).isoformat()

    st.write(f"🔍 Searching for station **{station}** between **{start_iso}** and **{end_iso}** ...")

    query = {
        "station": station,
        "start_time": {"$gte": start_iso},
        "end_time": {"$lte": end_iso}
    }

    results = list(collection.find(query).sort("start_time", -1))
   
    if results:
        st.success(f"✅ Found {len(results)} records for station: {station}")
    for i, result in enumerate(results):
            st.write("---")  
            st.subheader(f"📁 Record {i + 1}")
            st.write(f"📍 **Network:** {result.get('network', 'N/A')}")
            st.write(f"📡 **Channel:** {result.get('channel', 'N/A')}")
            st.write(f"📅 **Start Time:** {result.get('start_time', 'N/A')}")
            st.write(f"📅 **End Time:** {result.get('end_time', 'N/A')}")

            s3_url = result.get("s3_url", "#")
            if s3_url != "#":
                st.markdown(f"📥 **Download Data:** [Click Here]({s3_url})", unsafe_allow_html=True)
            else:
                st.warning("⚠️No S3 URL available for this record.")
    else:
        st.error("❌ No seismic data found for this station.")