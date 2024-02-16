import json
from shapely.geometry import Point, Polygon, mapping
import fiona
from fiona.crs import from_epsg

# Function to convert NOTAM coordinate string to a (longitude, latitude) tuple
def convert_notam_coord_to_lon_lat(coord_str):
    lat_deg = int(coord_str[0:2])
    lat_min = int(coord_str[2:4])
    lat_sec = int(coord_str[4:6])
    lat = lat_deg + (lat_min / 60) + (lat_sec / 3600)

    lon_deg = int(coord_str[7:10])
    lon_min = int(coord_str[10:12])
    lon_sec = int(coord_str[12:14])
    lon = -(lon_deg + (lon_min / 60) + (lon_sec / 3600))  # Negative for Western Hemisphere

    return (lon, lat)

# Read the input JSON file with NOTAMs
with open('TestData/norman.json', 'r') as file:
    notams_data = json.load(file)

# Create a list to hold our transformed features
features = []

# Process each NOTAM
for item in notams_data['items']:
    geometry = item['geometry']
    properties = item['properties']
    
    if geometry['type'] == 'GeometryCollection':
        for geom in geometry['geometries']:
            # Create the appropriate Shapely geometry
            if geom['type'] == 'Point':
                coordinates = convert_notam_coord_to_lon_lat(properties['coreNOTAMData']['notam']['coordinates'])
                shape = Point(coordinates)
            elif geom['type'] == 'Polygon':
                coordinates = [(lon, lat) for lon, lat in geom['coordinates'][0]]
                shape = Polygon(coordinates)
            else:
                continue  # Skip geometries that are not Point or Polygon
            
            # Append a new feature dictionary to the features list
            features.append({
                'type': 'Feature',
                'properties': properties,
                'geometry': mapping(shape)
            })
    else:
        continue  # Skip items that do not have a GeometryCollection type

# Define the output GeoJSON structure
geojson = {
    'type': 'FeatureCollection',
    'features': features
}

# Write the output GeoJSON file
with open('transformed_notams.geojson', 'w') as outfile:
    json.dump(geojson, outfile)

print('GeoJSON file created: transformed_notams.geojson')
