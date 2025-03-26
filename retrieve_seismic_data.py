import requests

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
