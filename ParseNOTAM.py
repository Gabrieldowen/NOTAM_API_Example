import json
import Models

def ParseNOTAM(json_data = None):

    if json_data is None:
        print("*********************\n USING TEST DATA \n*********************")
        # File path where the test JSON data is saved
        file_path = "static/TestData/TestNOTAM.json"

        # Reading JSON data from the file
        with open(file_path, 'r') as json_file:
            json_data = json.load(json_file)


    # create a class for each NOTAM
    NOTAMs = []
    for item in json_data['items']:
        NOTAMs.append(models.Notam(item['properties']['coreNOTAMData']['notam']))
        
    return NOTAMs

ParseNOTAM()