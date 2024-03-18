from flask import Flask, render_template, request
import Models
import ParseNOTAM
import MinimalCirclesPath
import AirportsLatLongConverter as alc
import GetNOTAM
import time
import concurrent.futures
import threading

app = Flask(__name__)
# Semaphore to limit concurrent API calls
api_call_semaphore = threading.Semaphore(40)

# Lock to synchronize access to apiOutputs list
api_outputs_lock = threading.Lock()

airportIATA = alc.airportsdata.load('IATA')
def build_notam(NotamRequest, latitude, longitude):
     # Acquire semaphore before making the API call
     api_call_semaphore.acquire()
     try:
            return GetNOTAM.buildNotam(NotamRequest.effectiveStartDate, NotamRequest.effectiveEndDate, longitude, latitude, NotamRequest.radius)
     finally:
            # Release semaphore after the API call is completed
            api_call_semaphore.release()
            
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

    

        startTime = time.time()  # Record start time
        with concurrent.futures.ThreadPoolExecutor(max_workers=40) as executor:
            # Create list of latitude and longitude tuples for every twenty coordinates
            coord_batches = [coordList[i:i+40] for i in range(0, len(coordList), 40)]
            
            # Submit API calls for each batch of latitude and longitude pairs concurrently
            for batch in coord_batches:
                futures = [executor.submit(build_notam, NotamRequest, latitude, longitude) for latitude, longitude in batch]
                
                # Wait for all API calls in the batch to complete and get results
                for future in concurrent.futures.as_completed(futures):
                    # Acquire lock before modifying apiOutputs list
                    with api_outputs_lock:
                        apiOutputs.extend(future.result())

        
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
