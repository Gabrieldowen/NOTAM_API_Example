import geopandas as gpd
import matplotlib.pyplot as plt
# Load the GeoJSON files
us_map = gpd.read_file('us.geojson')
notams = gpd.read_file('transformed_notams.geojson')

# Plotting
fig, ax = plt.subplots(figsize=(10, 10))  # Adjust the figure size as needed

# Plot the US map
us_map.plot(ax=ax, color='lightgray')

# Plot NOTAMs over the US map
notams.plot(ax=ax, color='red', markersize=5)  # You can change the color and size
plt.title('US Map with NOTAMs')
plt.show()
