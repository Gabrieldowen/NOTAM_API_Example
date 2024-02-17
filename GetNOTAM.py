from tkinter.tix import INTEGER
import requests
import credentials
import json
import urllib.parse
import os
import ZuluConverter
import AirportsLatLongConverter


#startNotam: Takes all user input from the user
#@returns effectiveStartDate: User inputed start flight time
#         effectiveEndDate: User inputed end flight time
#         airLocation[1]: lat for start location
#         airLocation[0]: long for start location
#         finalAirLocation[1]: lat for end location
#         finalAirLocation[0]: long for end location
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
    
    return effectiveStartDate, effectiveEndDate, airLocation[1], airLocation[0], finalAirLocation[1], finalAirLocation[0]
    
    
#getNotam: takes the lat, long, start and end time and the page number then runs an API call to the FAA for a json of the api
#@returns parsed_req: the json of the request
def getNotam(effectiveStartDate, effectiveEndDate, longitude, latitude, pageNum):
    url = 'https://external-api.faa.gov/notamapi/v1/notams'
    url = (f"{url}?responseFormat=geoJson&effectiveStartDate={effectiveStartDate}"
       f"&effectiveEndDate={effectiveEndDate}&locationLongitude={longitude}"
       f"&locationLatitude={latitude}&locationRadius=25"
       f"&pageNum={pageNum}&pageSize=50"
       f"&sortBy=notamType&sortOrder=Asc")

    headers = {'client_id': credentials.clientID, 'client_secret': credentials.clientSecret}

    req = requests.get(url, headers=headers)
    
    parsed_req = req.json()
    

    return parsed_req

#buildNotam: does multiple API call of a location given in inputs and combines all Jsons of each page into a single Json file
#@returns: combinded_core_notam_data, the combinded Json of all pages for one location
#         effectiveEndDate: User inputed end flight time
#         long: lat for a location
#         lat: long for a location
#         combined_core_notam_data: a Json being built by runNotam of all Jsons for a path
def buildNotam(effectiveStartDate, effectiveEndDate, long, lat, combined_core_notam_data):
    initial_response = getNotam(effectiveStartDate, effectiveEndDate, long, lat, pageNum=1)
    total_pages = initial_response.get('totalPages', 1)

    # Loop through all pages
    for page_num in range(1, total_pages + 1):
        page_response = getNotam(effectiveStartDate, effectiveEndDate, long, lat, pageNum=page_num)
        page_items = page_response.get('items', [])

        for item in page_items:
            if 'coreNOTAMData' in item['properties']:
                core_notam_data = item['properties']['coreNOTAMData']['notam']
                if core_notam_data not in combined_core_notam_data:
                    combined_core_notam_data.append(core_notam_data)
    return combined_core_notam_data

#runNotam: takes user input and does multiple buildNotam calls along a path in order 
def runNotam():
    effectiveStartDate, effectiveEndDate, long, lat, fLong, fLat = startNotam()
    
    combined_core_notam_data = []
    
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

   
