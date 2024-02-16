Before compiling make sure to create a credentials file named "credentials.py" with variables "clientID" and "clientSecret" and making sure to not commit these confidential keys to the public repository


Need run 'pip install airportsdata' to install the sirportsdata to be able to pull lat and long given airport data. 


To run app:

1) make sure you have flask downloaded on your system
2) run 'python3 app.py'
3) if "Port 5000 is in use by another program" either find and kill whatever is running on that port or specify host
	and port explicitly 'python3 app.py --host=0.0.0.0 --port=8080'
'