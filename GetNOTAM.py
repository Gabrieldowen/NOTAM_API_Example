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
  # Convert start and end dates to the desired format if provided
  if effectiveStartDate:
    effectiveStartDate = datetime.strptime(effectiveStartDate, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%dT%H:%M:%SZ")
        
  if effectiveEndDate:
    effectiveEndDate = datetime.strptime(effectiveEndDate, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%dT%H:%M:%SZ") 
  
  url = 'https://external-api.faa.gov/notamapi/v1/notams'
  url = (f"{url}?responseFormat=geoJson&effectiveStartDate={effectiveStartDate}"
       f"&effectiveEndDate={effectiveEndDate}&locationLongitude={longitude}"
       f"&locationLatitude={latitude}&locationRadius={radius}"
       f"&pageNum={pageNum}&pageSize=1000"
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
def buildNotam(effectiveStartDate, effectiveEndDate, long, lat, radius):
    combined_responses = []  # To store the full responses from all pages
    initial_response = getNotam(effectiveStartDate, effectiveEndDate, long, lat, 1, radius)  # pageNum=1 for the initial call
    total_pages = initial_response.get('totalPages', 1)
    combined_responses.append(initial_response)  # Add the initial response to the combined list

    # If there are more pages, loop through them and add their responses to the combined list
    if total_pages > 1:
        for page_num in range(2, total_pages + 1):  # Start from 2 since we already have page 1
            page_response = getNotam(effectiveStartDate, effectiveEndDate, long, lat, page_num, radius)
            combined_responses.append(page_response)  # Add the current page's response

    return combined_responses
