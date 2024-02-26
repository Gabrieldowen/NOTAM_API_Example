import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from shapely.geometry import Polygon
from MinimalCirclesPath import getSearchArea

us_map = gpd.read_file('us.geojson')

# Define start and destination coordinates, and other parameters if different from defaults
startLat, startLong = 32.7767, -96.7970
destLat, destLong = 39.7392, -104.9903
pathWidth = 50  # Path width in nautical miles

# Get the corners of the search area
corners = getSearchArea(startLat, startLong, destLat, destLong, pathWidth=pathWidth)



polygon_coords = [(lon, lat) for lat, lon in corners]
area_polygon = Polygon(polygon_coords)

def plot_notams_on_us_map(notams_file, us_map_gdf, polygon):
    notams_gdf = gpd.read_file(notams_file)

    if notams_gdf.empty:
        print("No NOTAMs found in the provided GeoJSON file.")
        return

    fig, ax = plt.subplots(figsize=(15, 10))
    ax.set_aspect('equal')

    us_map_gdf.plot(ax=ax, color='lightgray')

    overlaps_polygon = notams_gdf[notams_gdf.geometry.intersects(polygon)]
    outside_polygon = notams_gdf[~notams_gdf.geometry.intersects(polygon)]

    if not overlaps_polygon.empty:
        overlaps_polygon.plot(ax=ax, color='green', markersize=50, alpha=0.5, label='Overlap Area')
    if not outside_polygon.empty:
        outside_polygon.plot(ax=ax, color='red', markersize=50, alpha=0.5, label='Outside Area')

    # Plot the defined area polygon
    gpd.GeoSeries([polygon]).plot(ax=ax, edgecolor='blue', facecolor='none', linewidth=2)

    # Create custom legend
    legend_elements = [
        Patch(facecolor='green', edgecolor='green', label='Overlap Area'),
        Patch(facecolor='red', edgecolor='red', label='Outside Area'),
        Patch(facecolor='none', edgecolor='blue', label='Defined Area')
    ]
    plt.legend(handles=legend_elements, loc='lower left')
    plt.title('NOTAMs on US Map Relative to Defined Area')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')

    # Set the x and y axis limits to the bounds of the contiguous US
    ax.set_xlim([-125, -66])
    ax.set_ylim([24, 50])

    plt.show()

# comment out the one you want to use / plot
plot_notams_on_us_map('transformed_notams.geojson', us_map, area_polygon)
# plot_notams_on_us_map('path.geojson', us_map, area_polygon)