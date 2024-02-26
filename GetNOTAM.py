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
def getNotam(effectiveStartDate, effectiveEndDate, longitude, latitude, pageNum, radius):
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

#buildNotam: does multiple API call of a location given in inputs and combines all Jsons of each page into a single Json file
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

   
def removeDupes():
    input_file_path = 'raw_notams.json'
    output_file_path = 'deduplicated_file.json'

    # Load the data from the original JSON file
    with open(input_file_path, 'r') as file:
        data = json.load(file)

    print("Loaded data:", data)  # Debugging

    # Initialize a set to keep track of seen NOTAM IDs and a list for unique NOTAMs
    seen_notam_ids = set()
    unique_notams = []

    # Iterate through each item in the 'items' key of each page in data
    for page in data:  # If your JSON has multiple pages at the top level
        for item in page.get('items', []):  # Use dict.get() to handle missing keys
            core_notam_data = item.get('properties', {}).get('coreNOTAMData', {})
            notam_id = core_notam_data.get('notam', {}).get('id')
            if notam_id and notam_id not in seen_notam_ids:
                unique_notams.append(item)
                seen_notam_ids.add(notam_id)

    # Write the clean list back to a new JSON file
    with open(output_file_path, 'w') as file:
        json.dump(unique_notams, file, indent=4)

    print(f"Deduplicated file saved as '{output_file_path}'.")