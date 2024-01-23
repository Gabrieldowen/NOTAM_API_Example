import requests
import credentials
# 
url = 'https://external-api.faa.gov/notamapi/v1/notams'
headers = {'client_id': credentials.clientID,'client_secret': credentials.clientSecret}

req = requests.get(url, headers=headers)

print(req.status_code)
print(req.headers)
print(req.text)