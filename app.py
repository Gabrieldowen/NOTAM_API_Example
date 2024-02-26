import json
from flask import Flask, render_template, request
import Models
import ParseNOTAM
import MinimalCirclesPath
import AirportsLatLongConverter as alc
import GetNOTAM
import time
# import geoJsonTransformer
# import map

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():

    # If form is submitted
    if request.method == 'POST':
        NotamRequest = Models.NotamRequest(request.form)

        apiOutputs = []
        # get lat/long of airports
        NotamRequest.startLat, NotamRequest.startLong = alc.get_lat_and_lon(NotamRequest.startAirport)
        NotamRequest.destLat, NotamRequest.destLong = alc.get_lat_and_lon(NotamRequest.destAirport)

        # get the list of coordinates that need to be called to cover area
        coordList = MinimalCirclesPath.getPath(NotamRequest.startLat, 
                                               NotamRequest.startLong,
                                               NotamRequest.destLat,
                                               NotamRequest.destLong, 
                                               100, # circle radius
                                               50) # path width

        # start timer
        startTime = time.time() 

        # call the API for each point
        print("LOADING...")

        # apiOutputs = [ GetNOTAM.getNotam( NotamRequest.effectiveStartDate,
        #                                     NotamRequest.effectiveEndDate,
        #                                     longitude, # longitude
        #                                     latitude, # latitude
        #                                     1, # page num
        #                                     NotamRequest.radius) #page num here is one temporarily
        #                                     for latitude, longitude in coordList ]
        for latitude, longitude in coordList:
            radius = 50  # Example radius value, adjust as necessary
            new_data = GetNOTAM.buildNotam(NotamRequest.effectiveStartDate, NotamRequest.effectiveEndDate, longitude, latitude, radius)
            apiOutputs.extend(new_data)  # Assuming apiOutputs is a list


        # Record end time

        endTime = time.time()    
        print(f"\ntime calling API {endTime - startTime} seconds")

                # Save the raw API outputs to a JSON file
        with open('raw_notams.json', 'w') as file:
            json.dump(apiOutputs, file)

        GetNOTAM.removeDupes()
        # geoJsonTransformer.main()
        # map.plot_notams_on_us_map('transformed_notams.geojson', map.us_map, map.area_polygon)
        # takes api output and parse it
        startTime = time.time()  # Record start time
        Notams = ParseNOTAM.ParseNOTAM(apiOutputs)
        endTime = time.time()    # Record end time
        print(f"time parsing: {endTime - startTime} seconds\n")
        return render_template('display.html', notams = Notams)
        


    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)



