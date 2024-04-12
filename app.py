from flask import Flask, render_template, request
import Models
import ParseNOTAM
import MinimalCirclesPath
import filterNotam
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

        # get lat/long of airports
        NotamRequest.startLat, NotamRequest.startLong = alc.get_lat_and_lon(NotamRequest.startAirport)
        NotamRequest.destLat, NotamRequest.destLong = alc.get_lat_and_lon(NotamRequest.destAirport)
        
        NotamRequest.radius = int(NotamRequest.radius)
        NotamRequest.pathWidth = int(NotamRequest.pathWidth)

        # get the list of coordinates that need to be called to cover area
        coordList = MinimalCirclesPath.getPath(NotamRequest.startLat, 
                                               NotamRequest.startLong,
                                               NotamRequest.destLat,
                                               NotamRequest.destLong, 
                                               NotamRequest.radius, # circle radius
                                               NotamRequest.pathWidth) # path width
        
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
        apiOutputs = []

        for latitude, longitude in coordList:
            new_data = GetNOTAM.buildNotam(NotamRequest.effectiveStartDate, NotamRequest.effectiveEndDate, longitude, latitude, NotamRequest.radius)
            apiOutputs.extend(new_data)

        # Record end time
        endTime = time.time()    
        print(f"\ntime calling API {endTime - startTime} seconds")
        
        # takes api output and parse it
        startTime = time.time()  # Record start time
        Notams = ParseNOTAM.ParseNOTAM(apiOutputs)
        endTime = time.time()    # Record end time
        print(f"time parsing: {endTime - startTime} seconds\n")

        closed_runways = filterNotam.extract_closed_runways(Notams)

        # Filter out NOTAMs related to the closed runways

        """
        THIS IS FOR THE FUTURE WHEN THE USER WILL BE ABLE TO CHOOSE HOW HE WANTS OBSTACLES TO BE DISPLAYED

        user_pref = request.form.get('user_preference')
        
        if user_pref == 'ignore_all_obstacles':
            filtered_Notams = filterNotam.filter_out_obstacle_notams(filtered_Notams)
        elif user_pref == 'keep_high_obstacles':
            filtered_Notams = filterNotam.filter_keep_high_obstacle_notams(filtered_Notams, 500)
        """
        filtered_Notams = filterNotam.filter_notams(Notams, closed_runways)

        filtered_Notams = filterNotam.filter_out_obstacle_notams(filtered_Notams)

        markingNotams = filterNotam.identify_lighting_marking_notams(filtered_Notams)

        filtered_Notams = filterNotam.filter_out_lighting_marking_notams(filtered_Notams, markingNotams)
        
        filter_Notams = filterNotam.filter_out_keyword(filtered_Notams, 'CANCELED')
        
        return render_template('display.html', notams = filtered_Notams, closedR = closed_runways)
        
    return render_template('form.html', airportIATA = airportIATA)

if __name__ == '__main__':
    app.run(debug=True)
