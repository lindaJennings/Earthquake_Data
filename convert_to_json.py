import obspy
import json

# Load the MiniSEED file
mseed_file = "seismic_data.mseed"
try:
    st = obspy.read(mseed_file)
except Exception as e:
    print(f"❌ Error reading MiniSEED file: {e}")
    exit(1)

# Convert traces to a JSON format
data_list = []
for trace in st:
    trace_data = {
        "station": trace.stats.station,
        "network": trace.stats.network,
        "channel": trace.stats.channel,
        "starttime": str(trace.stats.starttime),
        "endtime": str(trace.stats.endtime),
        "sampling_rate": trace.stats.sampling_rate,
        "data_points": trace.data.tolist(),  # Convert NumPy array to list
    }
    data_list.append(trace_data)

# Save to JSON file
json_file = "seismic_data.json"
with open(json_file, "w") as f:
    json.dump(data_list, f, indent=2)

print(f"✅ MiniSEED data successfully converted and saved as '{json_file}'.")
