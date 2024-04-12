import matplotlib.pyplot as plt
import geopandas as gpd

# load US map
gdf = gpd.read_file('us.geojson')

def plot_path_on_us_map(coordList):
    # Load the US map from the GeoJSON file
    us_map = gpd.read_file('us.geojson')
    
    # Extract latitude and longitude from coordList
    latitudes, longitudes = zip(*coordList)
    
    # Create a GeoDataFrame for the path points
    path_gdf = gpd.GeoDataFrame(geometry=gpd.points_from_xy(longitudes, latitudes))
    
    # Initialize the plot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot the US map
    us_map.plot(ax=ax, color='lightgray', edgecolor='black')
    
    # Plot the path
    path_gdf.plot(ax=ax, marker='o', color='blue', linestyle='-', markersize=5, linewidth=2)
    
    # Optional: Annotate the start and end points
    plt.text(longitudes[0], latitudes[0], ' Start', color='green', fontsize=12)
    plt.text(longitudes[-1], latitudes[-1], ' End', color='red', fontsize=12)
    
    # Set titles and labels
    plt.title('Path Visualization on US Map')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    
    # Show the plot
    plt.show()
