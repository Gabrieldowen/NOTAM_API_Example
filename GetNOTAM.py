from tkinter.tix import INTEGER
import requests
import credentials
import json
import urllib.parse
import os
import ZuluConverter
import AirportsLatLongConverter
from datetime import datetime
import concurrent.futures
import threading

# Create a lock for the critical section
lock = threading.Lock()
    
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
    initial_response = getNotam(effectiveStartDate, effectiveEndDate, long, lat, pageNum=1, radius=radius)
    total_pages = initial_response.get('totalPages', 1)

    # Loop through all pages for an API Call
    combined_core_notam_data = []

    with concurrent.futures.ProcessPoolExecutor() as executor:
        # Submit API calls for all pages concurrently
        futures = [executor.submit(getNotam, effectiveStartDate, effectiveEndDate, long, lat, pageNum=page_num, radius=radius) 
                   for page_num in range(1, total_pages + 1)]

        # Wait for all API calls to complete and get results
        with lock:  # Acquire lock for the critical section
            combined_core_notam_data.extend([future.result() for future in futures])

    return combined_core_notam_data
