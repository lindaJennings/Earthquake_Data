from obspy import UTCDateTime
from obspy.clients.fdsn import Client

# Initialize the FDSN client for IRIS
client = Client("IRIS")

# Define the time range for the data retrieval
start_time = UTCDateTime("2024-03-01T00:00:00")
end_time = UTCDateTime("2024-03-02T00:00:00")

# Define the network, station, location, and channel codes
network = "EI"       # INSN network code
station = "DUB"      # Example station code for Dublin
location = ""        # Location code, often an empty string if not specified
channel = "BH?"      # Broadband high-gain channels (e.g., BHE, BHN, BHZ)

# Retrieve the waveform data
st = client.get_waveforms(network=network, station=station, location=location,
                          channel=channel, starttime=start_time, endtime=end_time)

# Save the data to a MiniSEED file
output_filename = f"seismic_data_{start_time.date}.mseed"
st.write(output_filename, format="MSEED")

print(f"Seismic data successfully saved to {output_filename}")
