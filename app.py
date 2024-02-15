from flask import Flask, render_template, request
import Models
import ParseNOTAM
import MinimalCirclesPath

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():

    # If form is submitted
    if request.method == 'POST':
        NotamRequest = Models.NotamRequest(request.form)

        # get lat/long of airports

        # coordList = MinimalCirclesPath.getPath(startLat, startLong, destLat, desLong, radius, pathWidth)

        # for each point in coordList
            # pass the form to getNOTAM to make API request
            # apiOutput = GetNOTAM.getNOTAM(NotamRequest)

        # takes api output and parse it
        Notams = ParseNOTAM.ParseNOTAM()
        return render_template('display.html', notams = Notams)
        


    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
