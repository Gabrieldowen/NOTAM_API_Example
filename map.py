import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon
import json

# Assuming `notams_data` is the JSON data you provided
notams_data = {
    # ... your NOTAM data ...
}

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

# Extract geometries from NOTAMs
notam_geometries = []
for item in notams_data['items']:
    geom_collection = item['geometry']['geometries']
    for geom in geom_collection:
        if geom['type'] == 'Point':
            coords = convert_notam_coord_to_lon_lat(item['properties']['coreNOTAMData']['notam']['coordinates'])
            notam_geometries.append(Point(coords))
        elif geom['type'] == 'Polygon':
            coords = [(lon, lat) for lon, lat in geom['coordinates'][0]]
            notam_geometries.append(Polygon(coords))

# Create a GeoDataFrame from the NOTAM geometries
notam_gdf = gpd.GeoDataFrame(geometry=notam_geometries)

# Load the US shapefile
us_map = gpd.read_file('/path/to/ne_10m_admin_0_countries_usa.shp')

# Filter the GeoDataFrame to only include the United States
us = us_map[us_map['ADMIN'] == 'United States of America']

# Plot the US map
fig, ax = plt.subplots(figsize=(15, 20))
us.plot(ax=ax, color='lightgrey')

# Overlay the NOTAM geometries on the map
notam_gdf.plot(ax=ax, color='red', markersize=5)

# Set plot limits if necessary
# ax.set_xlim([-130, -65])
# ax.set_ylim([24, 50])

plt.show()
