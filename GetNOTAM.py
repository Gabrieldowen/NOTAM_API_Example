import requests
import credentials
import json
import urllib.parse
import os

# Base URL for the NOTAM API
url = 'https://external-api.faa.gov/notamapi/v1/notams'

# User inputs
responseFormat = input("Enter response format (e.g., geoJson): ")
effectiveStartDate = input("Enter effective start date (YYYY-MM-DDTHH:MM:SS): ")
effectiveEndDate = input("Enter effective end date (YYYY-MM-DDTHH:MM:SS): ")
locationLongitude = input("Enter longitude: ")
locationLatitude = input("Enter latitude: ")
locationRadius = input("Enter radius (assumed unit, e.g., nautical miles): ")
sortBy = input("Enter sort by parameter (e.g., notamType): ")
sortOrder = input("Enter sort order (Asc or Desc): ")

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

with open(os.path.join(directory, "TestNOTAM.json"), 'w') as json_file:
    json.dump(parsed_req, json_file)
