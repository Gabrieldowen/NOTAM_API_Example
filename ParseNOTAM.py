import json

# File path where the JSON data is saved
file_path = "static/TestData/TestNOTAM.json"

# Reading JSON data from the file
with open(file_path, 'r') as json_file:
    loaded_data = json.load(json_file)

# print key names of each NOTAM
print(loaded_data['items'][0].keys())

# print components on the first NOTAM
print(f"\n\n type: {loaded_data['items'][0]['type']}")
print(f"\n\n properties: {loaded_data['items'][0]['properties']}")
print(f"\n\n geometry: {loaded_data['items'][0]['geometry']}")

# things we will need
print(f"\n\n notam: {loaded_data['items'][0]['properties']['coreNOTAMData']['notam']}")
print(f"\n\n text: {loaded_data['items'][0]['properties']['coreNOTAMData']['notam']['text']}")

# Accessing the loaded JSON data
#for item in loaded_data['items']:
    #print(item['type'])
