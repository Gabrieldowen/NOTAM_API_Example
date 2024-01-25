import json

# File path where the JSON data is saved
file_path = "TestData/TestNOTAM.json"

# Reading JSON data from the file
with open(file_path, 'r') as json_file:
    loaded_data = json.load(json_file)

# Accessing the loaded JSON data
for item in loaded_data['items']:
    print(item['type'])
