from flask import Flask, render_template, request, jsonify, session
from flask_session import Session
import os
from multiprocessing import Pool, cpu_count
import Models
import ParseNOTAM
import MinimalCirclesPath
import filterNotam
import AirportsLatLongConverter as alc
import GetNOTAM
import time
import translateNOTAM

app = Flask(__name__)
app.config['SECRET_KEY'] = '3af24b8e73398f446d45d66961a0bb4f'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = 'Sessions/'
Session(app)

airportIATA = alc.airportsdata.load('IATA')

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('form.html', airportIATA=airportIATA)

@app.route('/submit_form', methods=['POST'])
def submit_form():
    if request.method == 'POST':
        NotamRequest = Models.NotamRequest(request.form)
        airports = [NotamRequest.startAirport, NotamRequest.destAirport] + NotamRequest.destinations
        apiOutputs = []

        startTime = time.time()

        for i in range(len(airports) - 1):
            startLat, startLong = alc.get_lat_and_lon(airports[i])
            destLat, destLong = alc.get_lat_and_lon(airports[i+1])

            coordList = MinimalCirclesPath.getPath(startLat, startLong, destLat, destLong,
                                                  NotamRequest.radius, NotamRequest.pathWidth)

            if i >= 1:
                del coordList[0]

            print("LOADING...")

            inputs = [(NotamRequest.effectiveStartDate, NotamRequest.effectiveEndDate, longitude, latitude, NotamRequest.radius)
                      for latitude, longitude in coordList]
            with Pool(cpu_count()) as pool:
                apiOutputs += pool.starmap(GetNOTAM.buildNotam, inputs)

        endTime = time.time()
        print(f"\ntime calling API {endTime - startTime} seconds")

        Notams = ParseNOTAM.ParseNOTAM(apiOutputs)
        session['initial_notams'] = [notam.to_dict() for notam in Notams]

        return redirect('/display')

@app.route('/display', methods=['GET'])
def display():
    Notams = [Models.Notam(notam_dict) for notam_dict in session.get('initial_notams', [])]
    closedR = filterNotam.extract_closed_runways(Notams)

    return render_template('display.html', notams=Notams, closedR=closedR)

@app.route('/apply_filters', methods=['POST'])
def apply_filters():
    filter_options = request.json
    initial_notams = [Models.Notam(notam_dict) for notam_dict in session.get('initial_notams', [])]
    filtered_Notams = filterNotam.apply_filters(initial_notams, filter_options)
    session['filtered_notams'] = [notam.to_dict() for notam in filtered_Notams]

    return jsonify([notam.to_dict() for notam in filtered_Notams])

@app.route('/translateText', methods=['POST'])
def translateText():
    if request.method == 'POST':
        translatedText = translateNOTAM.callGemini(request.form['text'])
        return jsonify({'text': translatedText})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
