import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon
import json

# Define the coordinates for the Los Angeles area of interest
# The coordinates here are just an example, adjust the latitude and longitude to cover your desired area
LA_bounds = Polygon([
    (-118.7, 33.7),  # Bottom left
    (-117.5, 33.7),  # Bottom right
    (-117.5, 34.3),  # Top right
    (-118.7, 34.3)   # Top left
])

# Define a GeoDataFrame for the area of interest around Los Angeles
LA_area = gpd.GeoDataFrame([1], geometry=[LA_bounds], crs="EPSG:4326")

# Function to read NOTAM data from a JSON file
def read_notam_data_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Load NOTAMs data from JSON file
notams_data = read_notam_data_from_json('LA.json')

# Extract geometries from NOTAMs and check if they are in the LA area
inside_LA = []
outside_LA = []
for item in notams_data['items']:
    if 'geometry' in item and 'geometries' in item['geometry']:
        for geom in item['geometry']['geometries']:
            notam_geom = None
            if geom['type'] == 'Point':
                notam_geom = Point(geom['coordinates'])
            elif geom['type'] == 'Polygon':
                notam_geom = Polygon(geom['coordinates'][0])
            
            if notam_geom is not None:
                if LA_area.geometry.contains(notam_geom).bool():
                    inside_LA.append(notam_geom)
                else:
                    outside_LA.append(notam_geom)

# Create GeoDataFrames for NOTAMs inside and outside the LA area
inside_LA_gdf = gpd.GeoDataFrame(geometry=inside_LA, crs="EPSG:4326")
outside_LA_gdf = gpd.GeoDataFrame(geometry=outside_LA, crs="EPSG:4326")

# Load the US map (assuming you have it as a GeoJSON or Shapefile)
us_map = gpd.read_file('us.geojson')  # Change to your file path

# Plot the US map
fig, ax = plt.subplots(figsize=(15, 20))  # Adjust the figure size as needed
us_map.plot(ax=ax, color='lightgrey')

# Plot NOTAMs inside the LA area in green
inside_LA_gdf.plot(ax=ax, color='green', markersize=5)

# Plot NOTAMs outside the LA area in red
outside_LA_gdf.plot(ax=ax, color='red', markersize=5)

# Plot the LA area
LA_area.plot(ax=ax, edgecolor='black', color='none')

# Set the x and y axis limits to the bounds of the US map
bounds = us_map.total_bounds
ax.set_xlim(bounds[0], bounds[2])
ax.set_ylim(bounds[1], bounds[3])

# Remove axis off
ax.set_axis_off()

# Add a title to the plot
ax.set_title('US Map with Active NOTAMs (Green inside LA area, Red outside)', fontsize=20)

plt.show()
