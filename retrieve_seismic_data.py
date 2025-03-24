from obspy import UTCDateTime
from obspy.clients.fdsn import Client

# Use IRIS or GFZ as the FDSN provider instead of INSN
client = Client("IRIS")  # Alternative: Client("GFZ")

# Define the time range
start_time = UTCDateTime("2024-03-01T00:00:00")
end_time = UTCDateTime("2024-03-02T00:00:00")

# Define parameters for INSN stations (network="EI" for Irish Seismic Network)
network = "EI"       # Irish Seismic Network (INSN) code
station = "DUB"      # Example: Dublin station (change as needed)
location = ""        # Usually empty
channel = "BH?"      # Broadband high-gain channels (e.g., BHE, BHN, BHZ)

try:
    # Fetch the waveform data
    st = client.get_waveforms(network=network, station=station, location=location,
                              channel=channel, starttime=start_time, endtime=end_time)
    
    # Save as MiniSEED file
    filename = f"seismic_data_{start_time.date}.mseed"
    st.write(filename, format="MSEED")

    print(f"Seismic data successfully saved: {filename}")

except Exception as e:
    print(f"Error retrieving seismic data: {e}")
