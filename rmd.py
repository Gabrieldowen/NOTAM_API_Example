import json

# Replace 'your_file.json' with the path to your JSON file
input_file_path = 'raw_notams.json'
output_file_path = 'deduplicated_file.json'

# Load the data from the original JSON file
with open(input_file_path, 'r') as file:
    data = json.load(file)

# Assuming 'data' is a list of dictionaries each containing a 'items' key with the actual NOTAMs
# Initialize a set to keep track of seen NOTAM IDs and a list for unique NOTAMs
seen_notam_ids = set()
unique_notams = []

# Iterate through each item in the 'items' key of each page in data
for page in data:  # If your JSON has multiple pages at the top level
    for item in page['items']:
        notam_id = item['properties']['coreNOTAMData']['notam']['id']
        if notam_id not in seen_notam_ids:
            unique_notams.append(item)
            seen_notam_ids.add(notam_id)

# Write the deduplicated list back to a new JSON file
with open(output_file_path, 'w') as file:
    json.dump(unique_notams, file, indent=4)

print(f"Deduplicated file saved as '{output_file_path}'.")
