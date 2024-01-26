import requests
import credentials
import json 

# To add parameters to seach we need to append to the url like example below
# https://external-api.faa.gov/notamapi/v1/notams?icaoLocation=KLAX&domesticLocation=JFK&notamType=N&classification=INTL&effectiveStartDate=YYYY-MM-DDTHH%3AMM&effectiveEndDate=YYYY-MM-DDTHH%3AMM&featureType=RWY&locationLongitude=65&locationLatitude=30&locationRadius=10&lastUpdatedDate=10&sortBy=domesticLocation&sortOrder=Asc 

url = 'https://external-api.faa.gov/notamapi/v1/notams'
headers = {'client_id': credentials.clientID,'client_secret': credentials.clientSecret}

req = requests.get(url, headers=headers)

parsed_req = json.loads(req.text)

print(f"{req.status_code}\n\n")
print(f"{req.headers}\n\n")
print(f"{req.text}\n\n")

with open("TestData/TestNOTAM.json", 'w') as json_file:
    json.dump(parsed_req, json_file)
