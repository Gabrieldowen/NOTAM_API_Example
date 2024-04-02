from flask import Flask, render_template, request
import Models
import ParseNOTAM
import MinimalCirclesPath
import AirportsLatLongConverter as alc
import GetNOTAM
import time

app = Flask(__name__)

airportIATA = alc.airportsdata.load('IATA')

@app.route('/', methods=['GET', 'POST'])
def index():
    # If form is submitted
    if request.method == 'POST':
        NotamRequest = Models.NotamRequest(request.form)
        airports = [NotamRequest.startAirport, NotamRequest.destAirport]
        #counts in the number of airports the user is travelling to
        countAirports = 0
        for destination in NotamRequest.destinations:
            airports.append(destination)
            countAirports = countAirports + 1
        apiOutputs = []
        
        #i is used to track where we are in the array of airports
        i = 0
        # start timer
        startTime = time.time() 
        
        while i < countAirports:
            
            # get lat/long of airports
            NotamRequest.startLat, NotamRequest.startLong = alc.get_lat_and_lon(airports[i])
            NotamRequest.destLat, NotamRequest.destLong = alc.get_lat_and_lon(airports[i+1])
        
            NotamRequest.radius = int(NotamRequest.radius)
            NotamRequest.pathWidth = int(NotamRequest.pathWidth)


            #handles every other path thus prevents double calls for the same location being the final location for one path and the start location for the next path
            if i >= 1:
                # updates the start to a be outside of the previous call area from the start being the previous destination
                bearing = MinimalCirclesPath.calculateBearing(NotamRequest.startLat, NotamRequest.startLong, NotamRequest.destLat, NotamRequest.destLong)
                # updatedstart is the lat and long outside of the previous call from being the final location
                updatedStart = MinimalCirclesPath.nextPoint(NotamRequest.startLat, NotamRequest.startLong, bearing, NotamRequest.radius)
                
                coordList = MinimalCirclesPath.getPath(updatedStart[0], 
                                                       updatedStart[1],
                                                       NotamRequest.destLat,
                                                       NotamRequest.destLong, 
                                                       NotamRequest.radius, # circle radius
                                                       NotamRequest.pathWidth) # path width
            #handles the first path thus not needing to ensure double calls 
            else:
                coordList = MinimalCirclesPath.getPath(NotamRequest.startLat, 
                                                       NotamRequest.startLong,
                                                       NotamRequest.destLat,
                                                       NotamRequest.destLong, 
                                                       NotamRequest.radius, # circle radius
                                                       NotamRequest.pathWidth) # path width


            # call the API for each point
            print("LOADING...")

            
            #after the lat and longs are gathered in coordList, buildNotam is used to gather all the notams for the path
            for latitude, longitude in coordList:
                new_data = GetNOTAM.buildNotam(NotamRequest.effectiveStartDate, NotamRequest.effectiveEndDate, longitude, latitude, NotamRequest.radius)
                apiOutputs.extend(new_data)
            #increments i after the path is finished
            i = i+ 1    
        # Record end time
        endTime = time.time()    
        print(f"\ntime calling API {endTime - startTime} seconds")
        
        # takes api output and parse it
        startTime = time.time()  # Record start time
        Notams = ParseNOTAM.ParseNOTAM(apiOutputs)
        endTime = time.time()    # Record end time
        print(f"time parsing: {endTime - startTime} seconds\n")


        return render_template('display.html', notams = Notams)
        
    return render_template('form.html', airportIATA = airportIATA)

if __name__ == '__main__':
    app.run(debug=True)
