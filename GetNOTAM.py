from tkinter.tix import INTEGER
import requests
import credentials
import json
import urllib.parse
import os
import ZuluConverter
import AirportsLatLongConverter



# Base URL for the NOTAM API


def merge_two_dicts(x, y):
    z = x.copy()   # start with keys and values of x
    z.update(y)    # modifies z with keys and values of y
    return z

def startNotam():
# User inputs
    effectiveStartDate = input("Enter effective start date (YYYY-MM-DD HH:MM:SS): ")
    effectiveEndDate = input("Enter effective end date (YYYY-MM-DD HH:MM:SS): ")
    location = input("Enter airport: ")
    finalLocation = input("Enter ending airport: ")

    airLocation = AirportsLatLongConverter.get_lat_and_lon(location)
    finalAirLocation = AirportsLatLongConverter.get_lat_and_lon(finalLocation)


    effectiveStartDate = ZuluConverter.convert_cst_to_zulu(effectiveStartDate)
    effectiveEndDate = ZuluConverter.convert_cst_to_zulu(effectiveEndDate)
    headers = {'client_id': credentials.clientID, 'client_secret': credentials.clientSecret}
    
    return effectiveStartDate, effectiveEndDate, airLocation[1], airLocation[0], finalAirLocation[1], finalAirLocation[0]
    
    

def getNotam(effectiveStartDate, effectiveEndDate, long, lat, pageNum):
    url = 'https://external-api.faa.gov/notamapi/v1/notams'
    url = (f"{url}?responseFormat=geoJson&effectiveStartDate={effectiveStartDate}"
       f"&effectiveEndDate={effectiveEndDate}&locationLongitude={long}"
       f"&locationLatitude={lat}&locationRadius=25"
       f"&pageNum={pageNum}&pageSize=50"
       f"&sortBy=notamType&sortOrder=Asc")

    headers = {'client_id': credentials.clientID, 'client_secret': credentials.clientSecret}

    # Sending the GET request
    req = requests.get(url, headers=headers)
    
    parsed_req = req.json()
    

    return parsed_req
    
def buildNotam(effectiveStartDate, effectiveEndDate, long, lat,combined_core_notam_data):
    initial_response = getNotam(effectiveStartDate, effectiveEndDate, long, lat, pageNum=1)
    total_pages = initial_response.get('totalPages', 1)

    # Loop through all pages
    for page_num in range(1, total_pages + 1):
        page_response = getNotam(effectiveStartDate, effectiveEndDate, long, lat, pageNum=page_num)
        page_items = page_response.get('items', [])

        # Extract 'coreNOTAMData' from each item

        for item in page_items:
            if 'coreNOTAMData' in item['properties']:
                core_notam_data = item['properties']['coreNOTAMData']['notam']
                if core_notam_data not in combined_core_notam_data:
                    combined_core_notam_data.append(core_notam_data)
    return combined_core_notam_data

def runNotam():
    effectiveStartDate, effectiveEndDate, long, lat, fLong, fLat = startNotam()
    
    combined_core_notam_data = []
    # Initial call to get the total number of pages
    
    combined_core_notam_data = buildNotam(effectiveStartDate, effectiveEndDate, long, lat, combined_core_notam_data)
    print(len(combined_core_notam_data))
    wlong = float(long)
    wlat = float(lat)
    
    while wlong >= fLong or wlat <= fLat:
        combined_core_notam_data = buildNotam(effectiveStartDate, effectiveEndDate, str(wlong), str(wlat), combined_core_notam_data)
        if wlong >= fLong:
            wlong = wlong - 0.16667
        if wlat <= fLat:
            wlat = wlat + 0.16667
        print(wlat)
        print(wlong)
        print(len(combined_core_notam_data))
   
    
    
    # File handling
    directory = "TestData"
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(os.path.join(directory, "TestNOTAM.json"), 'w') as json_file:
        json.dump(combined_core_notam_data, json_file)

   
runNotam()
