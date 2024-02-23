import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon
import numpy as np

# Define the vertices of the polygon (replace these with your actual points)
vertices = [(lat1, lon1), (lat2, lon2), (lat3, lon3), (lat4, lon4)]

# Create the polygon from vertices
polygon = Polygon(vertices)

# Example NOTAM points (replace these with your actual NOTAMs or points)
notam_points = [(latA, lonA), (latB, lonB), ...]

# Setup the plot
fig, ax = plt.subplots()

# Plot the polygon
x,y = polygon.exterior.xy
ax.fill(x, y, alpha=0.4, fc='green', ec='black')

# Check each NOTAM point and plot
for point in notam_points:
    p = Point(point)
    # Color the NOTAM point based on whether it's inside the polygon
    if polygon.contains(p):
        ax.plot(point[1], point[0], marker='o', color='green', markersize=5)
    else:
        ax.plot(point[1], point[0], marker='o', color='red', markersize=5)

# Assuming your map plotting goes here, with basemap, contextily, or another mapping tool

plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('NOTAMs Visualization')
plt.show()
