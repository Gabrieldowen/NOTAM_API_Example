import airportsdata
import logging

def get_lat_and_lon(input_airport):
    # Load airport data
    airports = airportsdata.load('IATA')  # IATA = location code

    # Get lat and lon values
    try:
        lat = airports[input_airport]['lat']
        lon = airports[input_airport]['lon']
        return lat, lon
    except KeyError:
        # Log an error message
        logging.error(f"Airport code {input_airport} not found.")
        return None, None

# Example usage
if __name__ == "__main__":
    airports = airportsdata.load('IATA')  # key is the IATA location code
    print(get_lat_and_lon('JFK'))  # Should print the latitude and longitude of JFK airport
    print(get_lat_and_lon('XYZ'))  # Should log an error and print (None, None) as XYZ is not a valid IATA code
