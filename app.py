from flask import Flask, render_template, request, session, jsonify
from flask_session import Session
import Models
import ParseNOTAM
import MinimalCirclesPath
import filterNotam
import AirportsLatLongConverter as alc
import GetNOTAM
import time
import translateNOTAM
import os
from collections import defaultdict

app = Flask(__name__)
app.config['SECRET_KEY'] = '3af24b8e73398f446d45d66961a0bb4f'
app.config['SESSION_TYPE'] = 'filesystem'  # Store sessions on the filesystem
app.config['SESSION_FILE_DIR'] = 'Sessions/'
Session(app)

airportIATA = alc.airportsdata.load('IATA')

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('form.html', airportIATA = airportIATA)


@app.route('/submit_form', methods=['POST'])
def submit_form():
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

    

        # Record end time
        endTime = time.time()    
        print(f"\ntime calling API {endTime - startTime} seconds")
        
        # takes api output and parse it
        startTime = time.time()  # Record start time
        Notams = ParseNOTAM.ParseNOTAM(apiOutputs)
        endTime = time.time()    # Record end time
        print(f"time parsing: {endTime - startTime} seconds\n")

        # Assigns color severity to notams
        ParseNOTAM.assign_color_to_notam(Notams)

        # Sorts by color severity
        Notams = ParseNOTAM.sort_by_color(Notams)

        # Remove previous session data
        session.clear()
        # Store initial NOTAMs in session
        session['initial_notams'] = [notam.to_dict() for notam in Notams]

        return ''

@app.route('/display', methods=['GET'])
def display():
    # Get the Notams from the session.
    Notams = [Models.Notam(notam_dict) for notam_dict in session.get('initial_notams', [])]
    closedR = filterNotam.extract_closed_runways(Notams)
    
    return render_template('display.html', notams = Notams, closedR = closedR)


@app.route('/apply_filters', methods=['POST'])
def apply_filters():
    filter_options = request.json
    
    # Retrieve sorted NOTAMs from server-side session if available, otherwise use initial NOTAMs
    filtered_Notams = [Models.Notam(notam_dict) for notam_dict in session.get('sorted_notams', [])]
    if not filtered_Notams:
        filtered_Notams = [Models.Notam(notam_dict) for notam_dict in session.get('initial_notams', [])]
    
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
     
    if filter_options.get('cancelledNotams') == True:
        filtered_Notams = filterNotam.filter_out_keyword(filtered_Notams, "CANCELED")
    
    # Update session with filtered NOTAMs
    session['filtered_notams'] = [notam.to_dict() for notam in filtered_Notams]
    
    # Convert filtered NOTAMs to a list of dictionaries
    filtered_notams_dict = [notam.to_dict() for notam in filtered_Notams]
    
    # Return the filtered NOTAM list as JSON data
    return jsonify(filtered_notams_dict)

@app.route('/apply_sorting', methods=['POST'])
def apply_sorting():
    # Get the sorted order of NOTAM types and extract classifications
    classifications = [order.split('. ')[1] for order in request.json.get('notamTypesOrder', [])]
    
    # Retrieve filtered NOTAMs from server-side session if available, otherwise use initial NOTAMs
    filtered_Notams = [Models.Notam(notam_dict) for notam_dict in session.get('filtered_notams', [])]
    if not filtered_Notams:
        filtered_Notams = [Models.Notam(notam_dict) for notam_dict in session.get('initial_notams', [])]
    
    # Group NOTAMs by type
    notams_by_classification = defaultdict(list)
    for notam in filtered_Notams:
        notams_by_classification[notam.classification].append(notam)

    # Sort NOTAMs within each classification by severity
    for classification, notamList in notams_by_classification.items():
        notams_by_classification[classification] = sorted(notamList, key=lambda x: (
            0 if x.color == '#ff7f7f' else (1 if x.color == '#ffd966' else 2), x.color))
    
    # Sort NOTAMs based on the order of classifications
    sorted_notams = []
    for classification in classifications:
        sorted_notams.extend(notams_by_classification[classification])
    
    # Update session with sorted NOTAMs
    session['sorted_notams'] = [notam.to_dict() for notam in sorted_notams]
    
    # Convert sorted NOTAMs to a list of dictionaries
    sorted_notams_dict = [notam.to_dict() for notam in sorted_notams]
    
    # Return the sorted NOTAM list as JSON data
    return jsonify(sorted_notams_dict)

@app.route('/translateText', methods=['POST'])
def translateText():
    if request.method == 'POST':  
        translatedText = translateNOTAM.callGemini(request.form['text'])
    
        return jsonify({'text' : translatedText})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
