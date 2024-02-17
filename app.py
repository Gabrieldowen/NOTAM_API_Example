from flask import Flask, render_template, request
import Models
import ParseNOTAM
import MinimalCirclesPath
import AirportsLatLongConverter as alc
import GetNOTAM

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():

    # If form is submitted
    if request.method == 'POST':
        NotamRequest = Models.NotamRequest(request.form)


        # get lat/long of airports
        NotamRequest.startLat, NotamRequest.startLong = alc.get_lat_and_lon(NotamRequest.startAirport)
        NotamRequest.destLat, NotamRequest.destLong = alc.get_lat_and_lon(NotamRequest.destAirport)

        coordList = MinimalCirclesPath.getPath(NotamRequest.startLat, NotamRequest.startLong , NotamRequest.destLat, NotamRequest.destLong, 100, 50)

        apiOutputs = []
        for point in coordList:
            # pass the form to getNOTAM to make API request
            apiOutput = GetNOTAM.getNotam(NotamRequest.effectiveStartDate, NotamRequest.effectiveEndDate, point[1], point[0], 1)
            apiOutputs.append(apiOutput)

        # takes api output and parse it
        Notams = ParseNOTAM.ParseNOTAM(apiOutputs)
        return render_template('display.html', notams = Notams)
        


    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
