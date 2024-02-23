import requests
import credentials  # Assuming this module contains your API credentials
import json
import os

# Base URL for the NOTAM API
url = 'https://external-api.faa.gov/notamapi/v1/notams'

# Predefined NOTAM Request Information for University of Oklahoma Westheimer Airport (OUN)
responseFormat = "geoJson"
effectiveStartDate = "2024-02-15T00:00:00Z"
effectiveEndDate = "2024-02-16T23:59:59Z"
locationLongitude = "-97.4425"  # OUN Longitude
locationLatitude = "35.2456"  # OUN Latitude
locationRadius = "1"  # Assuming the unit is nautical miles
sortBy = "notamType"
sortOrder = "Asc"

# Construct the URL with the required parameters
url = (f"{url}?responseFormat={responseFormat}&effectiveStartDate={effectiveStartDate}"
       f"&effectiveEndDate={effectiveEndDate}&locationLongitude={locationLongitude}"
       f"&locationLatitude={locationLatitude}&locationRadius={locationRadius}"
       f"&sortBy={sortBy}&sortOrder={sortOrder}")

headers = {'client_id': credentials.clientID, 'client_secret': credentials.clientSecret}

# Sending the GET request
req = requests.get(url, headers=headers)
parsed_req = json.loads(req.text)

print(f"{req.status_code}\n\n")
print(f"{req.headers}\n\n")
print(f"{req.text}\n\n")

# File handling
directory = "TestData"
if not os.path.exists(directory):
    os.makedirs(directory)

with open(os.path.join(directory, "norman.json"), 'w') as json_file:
    json.dump(parsed_req, json_file)


