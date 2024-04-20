// the mapping 
// Check if Leaflet library is imported
// Creating map options
// the mapping 
// Check if Leaflet library is imported
// Creating map options

$(document).ready( function() {
    if (document.getElementById("map")) {
        if(calledPoints !== null && calledPoints !== undefined && calledPoints !== ''){
            loadMap();
        }
    }
});

function loadMap() {
    
    // map settings
    var coordinatesLength = calledPoints.features.length;
    middlePoint = parseInt(coordinatesLength/2)
    var zoom  = 4
    
    // centers the map at the middle point of the called points
    var map = L.map('map').setView([ calledPoints.features[middlePoint].geometry.coordinates[1],  calledPoints.features[middlePoint].geometry.coordinates[0]], zoom );

    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);


    // map the points that are called to get NOTAMs
    var myLayer = L.geoJSON().addTo(map);
    var line = [];

    // for each of the called points map a point and save it to a array for a line
    calledPoints.features.forEach(function(feature) {

        myLayer.addData(feature);
        var point = [feature.geometry.coordinates[1], feature.geometry.coordinates[0]]

        // Create a circle marker for each point and add it to the map
        L.circle(point, {
                color: 'blue',
                fillColor: '#0000FF',
                fillOpacity: 0.25,
                radius: 100 * 1852 // nautical miles to meters
            }).addTo(map)

        // save each point to a array for the line
        line.push(point);
        
    });


    // create a line from the points
    var polyline = new L.polyline(line, {
        color: 'blue',
        weight: 3,
        opacity: 0,
        smoothFactor: 1
    });
    polyline.addTo(map);
    
    // map the notams as red dots
    notamCoords.forEach(function(coord) {
        // Split the coordinate string
        var point = coord.toString().split(",");
        
        // Create a circle marker for each point and add it to the map
        var circle = L.circle([parseFloat(point[0]), parseFloat(point[1])], {
            color: 'red',
            fillColor: '#f03',
            fillOpacity: 0.5,
            radius: 500
        }).addTo(map);
    });



}

// this function parses the existing coordinates to a format that can be used by leaflet
function parseCoord(coordString) {
    // Extract degrees and minutes for latitude
    var latDegrees = parseInt(coordString.substring(0, 2), 10);
    var latMinutes = parseInt(coordString.substring(2, 4), 10);
    var latDecimal = latDegrees + latMinutes / 60;

    // Extract degrees and minutes for longitude
    var lonDegrees = parseInt(coordString.substring(5, 8), 10);
    var lonMinutes = parseInt(coordString.substring(8, 10), 10);
    var lonDecimal = lonDegrees + lonMinutes / 60;

    // Determine direction for latitude and longitude
    var latDirection = coordString.charAt(4); // 'N' for north
    var lonDirection = coordString.charAt(10); // 'E' for east

    // Add the direction for latitude
    if (latDirection === 'S') {
        latDecimal = -latDecimal;
    }

    // Add the direction for longitude
    if (lonDirection === 'W') {
        lonDecimal = -lonDecimal;
    }

    var latDecimal = parseFloat(latDecimal);
    var lonDecimal = parseFloat(lonDecimal);

    return [latDecimal, lonDecimal];

}