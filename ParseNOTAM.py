import json
import models

def ParseNOTAM():
    # File path where the JSON data is saved
    file_path = "static/TestData/TestNOTAM.json"

    # Reading JSON data from the file
    with open(file_path, 'r') as json_file:
        loaded_data = json.load(json_file)

    # create a class for each NOTAM
    NOTAMs = []
    for item in loaded_data['items']:
        NOTAMs.append(models.Notam(item['properties']['coreNOTAMData']['notam']))
        
    return NOTAMs

ParseNOTAM()