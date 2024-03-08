from tkinter.tix import INTEGER
import requests
import credentials
import json
import urllib.parse
import os
import ZuluConverter
import AirportsLatLongConverter
from datetime import datetime

  
    
#getNotam: takes the lat, long, start and end time and the page number then runs an API call to the FAA for a json of the api
#@returns parsed_req: the json of the request
def getNotam(effectiveStartDate, effectiveEndDate, longitude, latitude, pageNum, radius):
  # Convert datetime strings to the desired format
  effectiveStartDate = datetime.strptime(effectiveStartDate, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%dT%H:%M:%SZ")
  effectiveEndDate = datetime.strptime(effectiveEndDate, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%dT%H:%M:%SZ")  
  
  url = 'https://external-api.faa.gov/notamapi/v1/notams'
  url = (f"{url}?responseFormat=geoJson&effectiveStartDate={effectiveStartDate}"
       f"&effectiveEndDate={effectiveEndDate}&locationLongitude={longitude}"
       f"&locationLatitude={latitude}&locationRadius={radius}"
       f"&pageNum={pageNum}&pageSize=50"
       f"&sortBy=notamType&sortOrder=Asc")

  headers = {'client_id': credentials.clientID, 'client_secret': credentials.clientSecret}

  req = requests.get(url, headers=headers)
    
  parsed_req = req.json()
    
  return parsed_req

#buildNotam: does multiple API calls of a location given in inputs and combines all Jsons of each page into a single Json file
#@returns: combinded_core_notam_data, the combinded Json of all pages for one location
#         effectiveEndDate: User inputed end flight time
#         long: lat for a location
#         lat: long for a location
#         combined_core_notam_data: a Json being built by runNotam of all Jsons for a path
def buildNotam(effectiveStartDate, effectiveEndDate, long, lat, combined_core_notam_data):
    #gets the first page of the API call for a single location
    initial_response = getNotam(effectiveStartDate, effectiveEndDate, long, lat, pageNum=1)
    #Gets the total number of pages for all the notams in a single location
    total_pages = initial_response.get('totalPages', 1)

    # Loop through all pages for an API Call
    for page_num in range(1, total_pages + 1):
        page_response = getNotam(effectiveStartDate, effectiveEndDate, long, lat, pageNum=page_num)
        page_items = page_response.get('items', [])
        #Removes duplicates from the parsed Json 
        for item in page_items:
            if 'coreNOTAMData' in item['properties']:
                core_notam_data = item['properties']['coreNOTAMData']['notam']
                #Adds to parsed if the Notam doesn't already exist
                if core_notam_data not in combined_core_notam_data:
                    combined_core_notam_data.append(core_notam_data)

    return combined_core_notam_data
