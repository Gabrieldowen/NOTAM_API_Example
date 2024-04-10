from flask import Flask, render_template, request, session, jsonify
from flask_session import Session
import Models
import ParseNOTAM
import MinimalCirclesPath
import filterNotam
import AirportsLatLongConverter as alc
import GetNOTAM
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = '3af24b8e73398f446d45d66961a0bb4f'
app.config['SESSION_TYPE'] = 'filesystem'  # Store sessions on the filesystem
app.config['SESSION_FILE_DIR'] = 'Sessions/'
Session(app)

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

        # Add color filtering here !

        # Record end time
        endTime = time.time()    
        print(f"\ntime calling API {endTime - startTime} seconds")
        
        # takes api output and parse it
        startTime = time.time()  # Record start time
        Notams = ParseNOTAM.ParseNOTAM(apiOutputs)
        endTime = time.time()    # Record end time
        print(f"time parsing: {endTime - startTime} seconds\n")
        
        # Store initial NOTAMs in session
        session['initial_notams'] = [notam.to_dict() for notam in Notams]
        
        return render_template('display.html', notams = Notams)
        
    return render_template('form.html', airportIATA = airportIATA)

@app.route('/apply_filters', methods=['POST'])
def apply_filters():
    filter_options = request.json
    # Retrieve initial NOTAMs from server-side session
    initial_notams = [Models.Notam(notam_dict) for notam_dict in session.get('initial_notams', [])]
    
    # Apply selected filters to the initial NOTAM list
    filtered_Notams = initial_notams
    
    if filter_options.get('closedRunways') == True:
        closed_runways = filterNotam.extract_closed_runways(filtered_Notams)
        filtered_Notams = filterNotam.filter_notams(filtered_Notams, closed_runways)
  
    if filter_options.get('obstacleNotams') == True:
        filtered_Notams = filterNotam.filter_out_obstacle_notams(filtered_Notams)

    if filter_options.get('highObstacleNotams') == True:
        # Assuming the threshold for high obstacle NOTAMs is 500
        filtered_Notams = filterNotam.filter_keep_high_obstacle_notams(filtered_Notams, 500)

    if filter_options.get('lightingMarkingNotams') == True:
        markingNotams = filterNotam.identify_lighting_marking_notams(filtered_Notams)
        filtered_Notams = filterNotam.filter_out_lighting_marking_notams(filtered_Notams, markingNotams)
    
    # Update session with filtered NOTAMs
    session['filtered_notams'] = [notam.to_dict() for notam in filtered_Notams]
    
    # Convert filtered NOTAMs to a list of dictionaries
    filtered_notams_dict = [notam.to_dict() for notam in filtered_Notams]
    
    # Return the filtered NOTAM list as JSON data
    return jsonify(filtered_notams_dict)

if __name__ == '__main__':
    app.run(debug=True)
