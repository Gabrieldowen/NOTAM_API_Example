import airportsdata

#airports = airportsdata.load('IATA')

# Should we add a name to abbreviation converter?
# How will users input their airport?

# Get lat and lon
def get_lat_and_lon(input_airport):
    # Load airport data
    airports = airportsdata.load('IATA')    # IATA = location code

    # Get lat and lon values
    lat = airports[input_airport]['lat']
    lon = airports[input_airport]['lon']

    return [lat, lon]

print(get_lat_and_lon('JFK'))   # returns vector
print(get_lat_and_lon('JFK')[0])    # returns lat
print(get_lat_and_lon('JFK')[1])    # returns lon

