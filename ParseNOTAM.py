import json
import Models

def ParseNOTAM(apiOutput = None):

    if apiOutput is None:
        print("*********************\n USING TEST DATA \n*********************")
        # File path where the test JSON data is saved
        file_path = "static/TestData/TestNOTAM.json"

        # Reading test JSON data from the file
        with open(file_path, 'r') as json_file:
            apiOutput = json.load(json_file)

    """
    apiOutput is an array of output from the API. In each of the outputs the "items" are that API call's NOTAMs
    each notam is json structure as follows:
    {
      "pageSize": 10,
      "pageNum": 3,
      "totalCount": 124,
      "totalPages": 13,
      "items": [
        {
          "type": "Point",
          "geometry": {
            "type": "Point",
            "coordinates": [
              0
            ]
          },
          "properties": {
            "coreNOTAMData": {
              "notamEvent": {
                "scenario": "6000"
              },
              "notam": {
                "id": "NOTAM_1_66366992",
                "series": "A",
                "number": "A9833/22",
                "type": "N",
                "issued": "2022-12-07T02:34:00.000Z",
                etc...
            }
          }
        }
      ]
    }
    """
    NOTAMs = []
    for notam in apiOutput:
        # create a class for each NOTAM
        for item in notam['items']:
            NOTAMs.append(Models.Notam(item['properties']['coreNOTAMData']['notam']))
            
    return NOTAMs


