run: 
	echo "Fetching NOTAMS..."
	python3 getNorman.py
	echo "Extracting coordinates..." 
	python3 geoJsonTransformer.py
	echo "Plotting the NOTAMS..."
	python3 map.py
transform:
	

clean: 
	# Remove the output JSON file(s)
	echo "Removing output JSON files..."
	rm -f TestData/TestNOTAM.json
	rm -f TestData/norman.json
	rm -f transformed_notams.geojson transformed_notams.log
	echo "Output JSON files removed."