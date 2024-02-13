import requests
import credentials
import json
import urllib.parse
import os
import ZuluConverter
import AirportsLatLongConverter

# Base URL for the NOTAM API
url = 'https://external-api.faa.gov/notamapi/v1/notams'

# User inputs
effectiveStartDate = input("Enter effective start date (YYYY-MM-DD HH:MM:SS): ")
effectiveEndDate = input("Enter effective end date (YYYY-MM-DD HH:MM:SS): ")
location = input("Enter airport: ")

airLocation = AirportsLatLongConverter.get_lat_and_lon(location)


effectiveStartDate = ZuluConverter.convert_cst_to_zulu(effectiveStartDate)
effectiveEndDate = ZuluConverter.convert_cst_to_zulu(effectiveEndDate)

# Construct the URL with the required parameters
url = (f"{url}?responseFormat=geoJson&effectiveStartDate={effectiveStartDate}"
       f"&effectiveEndDate={effectiveEndDate}&locationLongitude={airLocation[1]}"
       f"&locationLatitude={airLocation[0]}&locationRadius=50"
       f"&sortBy=notamType&sortOrder=Asc")

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