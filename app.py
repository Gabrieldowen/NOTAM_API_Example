from flask import Flask, render_template, request
import Models
import ParseNOTAM
import MinimalCirclesPath
import AirportsLatLongConverter as alc
import GetNOTAM
import time

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():

    # If form is submitted
    if request.method == 'POST':
        NotamRequest = Models.NotamRequest(request.form)


        # get lat/long of airports
        NotamRequest.startLat, NotamRequest.startLong = alc.get_lat_and_lon(NotamRequest.startAirport)
        NotamRequest.destLat, NotamRequest.destLong = alc.get_lat_and_lon(NotamRequest.destAirport)

        # get the list of coordinates that need to be called to cover area
        coordList = MinimalCirclesPath.getPath(NotamRequest.startLat, NotamRequest.startLong , NotamRequest.destLat, NotamRequest.destLong, 100, 50)

        # start timer
        startTime = time.time() 

        # call the API for each point
        apiOutputs = []
        print("LOADING...")
        for point in coordList:
            apiOutput = GetNOTAM.getNotam(NotamRequest.effectiveStartDate, NotamRequest.effectiveEndDate, point[1], point[0], 1) # page num here is one temporarily
            apiOutputs.append(apiOutput)

        # Record end time
        endTime = time.time()    
        print(f"\ntime calling API {endTime - startTime} seconds")


        # takes api output and parse it
        startTime = time.time()  # Record start time
        Notams = ParseNOTAM.ParseNOTAM(apiOutputs)
        endTime = time.time()    # Record end time
        print(f"time parsing: {endTime - startTime} seconds\n")

        return render_template('display.html', notams = Notams)
        


    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
