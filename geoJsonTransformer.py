import json
from shapely.geometry import Point, Polygon, mapping
import logging
import re
from pyproj import Transformer, CRS

# Setup basic configuration for logging
logging.basicConfig(filename='transformed_notams.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')

def convert_notam_coord_to_lon_lat(coord_str):
    try:
        # Extract and convert latitude and longitude
        lat_deg, lat_min, lat_sec, lat_hem = int(coord_str[:2]), int(coord_str[2:4]), int(coord_str[4:6]), coord_str[6]
        lon_deg, lon_min, lon_sec, lon_hem = int(coord_str[7:10]), int(coord_str[10:12]), int(coord_str[12:14]), coord_str[14]

        lat = lat_deg + lat_min / 60.0 + lat_sec / 3600.0
        if lat_hem == 'S':
            lat *= -1

        lon = lon_deg + lon_min / 60.0 + lon_sec / 3600.0
        if lon_hem == 'W':
            lon *= -1

        return (lon, lat)
    except ValueError as e:
        logging.error(f"Error converting coordinates: {e}")
        return None

def create_circle(lat, lon, radius_nm):
    # Convert radius from nautical miles to meters
    radius_m = radius_nm * 1852

    # Initialize Transformer instances for geographic to UTM conversion and vice versa
    transformer_to_utm = Transformer.from_crs(CRS.from_epsg(4326), CRS.from_proj4(f"+proj=utm +zone={int((lon + 180) / 6) + 1} +ellps=WGS84"), always_xy=True)
    transformer_to_wgs84 = Transformer.from_crs(CRS.from_proj4(f"+proj=utm +zone={int((lon + 180) / 6) + 1} +ellps=WGS84"), CRS.from_epsg(4326), always_xy=True)

    # Transform WGS84 to UTM
    utm_x, utm_y = transformer_to_utm.transform(lon, lat)

    # Generate a circle polygon around the point in UTM
    circle = Point(utm_x, utm_y).buffer(radius_m, resolution=64)  # Increase resolution for a smoother circle

    # Transform the circle's coordinates back to WGS84
    circle_wgs84_coords = list(transformer_to_wgs84.itransform(circle.exterior.coords))
    
    return Polygon(circle_wgs84_coords)
def process_geometry(geometry, properties):
    features = []

    if geometry.get('type') == 'GeometryCollection' and (not geometry.get('geometries') or geometry['geometries'] == []):
        features += extract_geometry_from_text(properties)
    else:
        if geometry['type'] == 'GeometryCollection':
            for geom in geometry['geometries']:
                features += process_individual_geometry(geom, properties)
        elif geometry['type'] in ['Point', 'Polygon']:
            features += process_individual_geometry(geometry, properties)

    return features

def extract_geometry_from_text(properties):
    features = []
    notam_text = properties.get('coreNOTAMData', {}).get('notam', {}).get('text', '')
    match = re.search(r'(\d+)NM RADIUS OF (\d{6}[NS]\d{7}[EW])', notam_text)
    if match:
        radius_nm = int(match.group(1))
        coord_str = match.group(2)
        lon, lat = convert_notam_coord_to_lon_lat(coord_str)
        if lon is not None and lat is not None:
            circle = create_circle(lat, lon, radius_nm)
            properties_to_include = {
                'id': properties['coreNOTAMData']['notam']['id'],
                'issued': properties['coreNOTAMData']['notam']['issued'],
                'effectiveStart': properties['coreNOTAMData']['notam']['effectiveStart'],
                'effectiveEnd': properties['coreNOTAMData']['notam']['effectiveEnd'],
                'text': properties['coreNOTAMData']['notam']['text'],
                # Include any other properties you want here
            }
            features.append({
                'type': 'Feature',
                'properties': properties_to_include,
                'geometry': mapping(circle)
            })
    return features

def process_individual_geometry(geom, properties):
    properties_to_include = {
        'id': properties['coreNOTAMData']['notam']['id'],
        'issued': properties['coreNOTAMData']['notam']['issued'],
        'effectiveStart': properties['coreNOTAMData']['notam']['effectiveStart'],
        'effectiveEnd': properties['coreNOTAMData']['notam']['effectiveEnd'],
        'text': properties['coreNOTAMData']['notam']['text'],
        # Include any other properties you want here
    }

    if geom['type'] == 'Point':
        point = Point(geom['coordinates'])
        return [{
            'type': 'Feature',
            'properties': properties_to_include,
            'geometry': mapping(point)
        }]
    elif geom['type'] == 'Polygon':
        polygon = Polygon(geom['coordinates'][0])
        return [{
            'type': 'Feature',
            'properties': properties_to_include,
            'geometry': mapping(polygon)
        }]
    else:
        logging.error(f"Unsupported geometry type: {geom['type']}")
        return []

def load_notams_data(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")
        return {'items': []}  # Fallback to empty data

def main():
    notams_data = load_notams_data('TestData/norman.json')
    features = []

    for item in notams_data['items']:
        try:
            geometry = item.get('geometry', {})
            properties = item['properties']
            
            features += process_geometry(geometry, properties)
        except Exception as e:
            logging.error(f"Error processing NOTAM item: {e}")

    geojson = {
        'type': 'FeatureCollection',
        'features': features
    }

    try:
        with open('transformed_notams.geojson', 'w') as outfile:
            json.dump(geojson, outfile)
        logging.info('GeoJSON file created: transformed_notams.geojson')
    except Exception as e:
        logging.error(f"Error writing GeoJSON file: {e}")

if __name__ == "__main__":
    main()