from obspy import UTCDateTime
from obspy.clients.fdsn import Client

# Define parameters
client = Client("http://www.insn.ie/fdsnws/")  # Irish National Seismic Network FDSN URL
start_time = UTCDateTime().date  # Today's date
end_time = UTCDateTime()  # Now

# Fetch seismic data
st = client.get_waveforms(network="IE", station="DUB", location="", channel="BH?", starttime=start_time, endtime=end_time)

# Save MiniSEED file
filename = f"seismic_data_{start_time}.mseed"
st.write(filename, format="MSEED")

print(f"Seismic data saved: {filename}")
