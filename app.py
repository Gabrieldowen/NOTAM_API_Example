from flask import Flask, render_template, request
import Models
import ParseNOTAM
import MinimalCirclesPath
import AirportsLatLongConverter as alc

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():

    # If form is submitted
    if request.method == 'POST':
        NotamRequest = Models.NotamRequest(request.form)


        # get lat/long of airports
        NotamRequest.startLat, NotamRequest.startLong = alc.get_lat_and_lon(NotamRequest.startAirport)
        NotamRequest.destLat, NotamRequest.destLong = alc.get_lat_and_lon(NotamRequest.destAirport)

        print(f"{NotamRequest.startLat}{NotamRequest.startLong}")
        print(f"{NotamRequest.destLat}{NotamRequest.destLong}")


        coordList = MinimalCirclesPath.getPath(NotamRequest.startLat, NotamRequest.startLong , NotamRequest.destLat, NotamRequest.destLong, radius, pathWidth)

        # for point in coordList
            # pass the form to getNOTAM to make API request
            # apiOutput = GetNOTAM.getNOTAM(NotamRequest.effectiveStartDate, NotamRequest.effectiveEndDate, point[1], point[0], NotamRequest.pageNum)

        # takes api output and parse it
        Notams = ParseNOTAM.ParseNOTAM(apiOutput)
        return render_template('display.html', notams = Notams)
        


    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
