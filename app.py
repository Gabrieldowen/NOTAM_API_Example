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
        for destination in NotamRequest.destinations:
            airports.append(destination)
        apiOutputs = []

        #i is used to track where we are in the array of airports
        # start timer
        startTime = time.time() 
        
        
        #len(airports) -1 ensures the loop treats i as the starting location for each iteration and prevents out of index errors
        for i in range(len(airports) - 1):
            
            # get lat/long of airports
            startLat, startLong = alc.get_lat_and_lon(airports[i])
            destLat, destLong = alc.get_lat_and_lon(airports[i+1])
        
            NotamRequest.radius = int(NotamRequest.radius)
            NotamRequest.pathWidth = int(NotamRequest.pathWidth)

            
            coordList = MinimalCirclesPath.getPath(startLat, 
                                                       startLong,
                                                       destLat,
                                                       destLong, 
                                                       NotamRequest.radius, # circle radius
                                                       NotamRequest.pathWidth) # path width
            
            #deletes the first lat and long to prevent double calls
            if i >= 1:
                 del coordList[0]


            # call the API for each point
            print("LOADING...")

            
            #after the lat and longs are gathered in coordList, buildNotam is used to gather all the notams for the path
            for latitude, longitude in coordList:
                new_data = GetNOTAM.buildNotam(NotamRequest.effectiveStartDate, NotamRequest.effectiveEndDate, longitude, latitude, NotamRequest.radius)
                apiOutputs.extend(new_data)
            
             

        
        # takes api output and parse it
        Notams = ParseNOTAM.ParseNOTAM(apiOutputs)
        endTime = time.time()    # Record end time
        print(f"time parsing: {endTime - startTime} seconds\n")


        return render_template('display.html', notams = Notams)
        
    return render_template('form.html', airportIATA = airportIATA)

if __name__ == '__main__':
    app.run(debug=True)
