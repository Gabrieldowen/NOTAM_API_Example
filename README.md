
This project is still in development. Its goal is to fetch and filter relevent NOTAMs for your flight. The data is gathered from the FAA's NOTAM API. This app is built using two frameworks, Flask and Bootstrap.

To run app locally:

1) make sure you have python3 installed
2) refer to setup.py for project dependencies and run 'python3 setup.py install' to install all of them
3) create a credentials file named "credentials.py" with variables "clientID" and "clientSecret"
4) run 'python3 app.py'
5) if "Port 5000 is in use by another program" either find and kill whatever is running on that port or specify host
	and port explicitly. example: 'python3 app.py --host=0.0.0.0 --port=8080'

	