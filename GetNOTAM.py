from tkinter.tix import INTEGER
import requests
import credentials
import json
import urllib.parse
import os
import ZuluConverter
import AirportsLatLongConverter



# Base URL for the NOTAM API


def startNotam():
# User inputs
    effectiveStartDate = input("Enter effective start date (YYYY-MM-DD HH:MM:SS): ")
    effectiveEndDate = input("Enter effective end date (YYYY-MM-DD HH:MM:SS): ")
    location = input("Enter airport: ")

    airLocation = AirportsLatLongConverter.get_lat_and_lon(location)


    effectiveStartDate = ZuluConverter.convert_cst_to_zulu(effectiveStartDate)
    effectiveEndDate = ZuluConverter.convert_cst_to_zulu(effectiveEndDate)
    headers = {'client_id': credentials.clientID, 'client_secret': credentials.clientSecret}
    
    return effectiveStartDate, effectiveEndDate, airLocation[1], airLocation[0]
    
    

def getNotam(effectiveStartDate, effectiveEndDate, long, lat):
    url = 'https://external-api.faa.gov/notamapi/v1/notams'
    url = (f"{url}?responseFormat=geoJson&effectiveStartDate={effectiveStartDate}"
       f"&effectiveEndDate={effectiveEndDate}&locationLongitude={long}"
       f"&locationLatitude={lat}&locationRadius=25"
       f"&sortBy=notamType&sortOrder=Asc")

    headers = {'client_id': credentials.clientID, 'client_secret': credentials.clientSecret}

    # Sending the GET request
    req = requests.get(url, headers=headers)
    
    parsed_req = req.json()

    return req, parsed_req

def runNotam():
    effectiveStartDate, effectiveEndDate, long, lat = startNotam()
    
    req, parsed_req = getNotam(effectiveStartDate, effectiveEndDate, long, lat)
    res = req.json()
    wlong = float(long)+10
    wlat = float(lat)+10
    areq, sreq  = getNotam(effectiveStartDate, effectiveEndDate, str(wlong), str(wlat))
    print(res)
    print(sreq)
    merged_dict = {}

    # Combine keys and values from both dictionaries
    combined_items = {**res, **sreq}
    
    print(combined_items)

    

    # File handling
    directory = "TestData"
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(os.path.join(directory, "TestNOTAM.json"), 'w') as json_file:
        json.dump(parsed_req, json_file)
runNotam()
