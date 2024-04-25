// the mapping 
// Check if Leaflet library is imported
// Creating map options
// the mapping 
// Check if Leaflet library is imported
// Creating map options

// $(document).ready( function() {
//     if (document.getElementById("map")) {
//         if(calledPoints !== null && calledPoints !== undefined && calledPoints !== ''){
//             loadMap();
//         }
//     }
// });
function loadMap(notamCoords) {
    
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
    myLayer = L.geoJSON().addTo(map);
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

    var notamLayer = L.layerGroup().addTo(map);
    
    // map the notams as red dots
    notamCoords.forEach(function(coord) {
        // Split the coordinate string
        var point = coord.toString().split(",");
        
        // Create a circle marker for each point and add it to the notam layer
        var circle = L.circle([parseFloat(point[0]), parseFloat(point[1])], {
            color: 'red',
            fillColor: '#f03',
            fillOpacity: 0.5,
            radius: 500
        }).addTo(notamLayer);
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
     if (lonDirection === 'W') {
        lonDecimal = -lonDecimal;
    }
    var latDecimal = parseFloat(latDecimal);
    var lonDecimal = parseFloat(lonDecimal);
    return [latDecimal, lonDecimal];
}

function processCoordinates(notams) {

    var processCoords = [];
    notams.forEach(function(notam) {
        if (notam.coordinates != undefined || notam.coordinates != null) {
            // Extract degrees and minutes for latitude
            var latDegrees = parseInt(notam.coordinates.substring(0, 2), 10);
            var latMinutes = parseInt(notam.coordinates.substring(2, 4), 10);
            var latDecimal = latDegrees + latMinutes / 60;

            // Extract degrees and minutes for longitude
            var lonDegrees = parseInt(notam.coordinates.substring(5, 8), 10);
            var lonMinutes = parseInt(notam.coordinates.substring(8, 10), 10);
            var lonDecimal = lonDegrees + lonMinutes / 60;

            // Determine direction for latitude and longitude
            var latDirection = notam.coordinates.charAt(4); // 'N' for north
            var lonDirection = notam.coordinates.charAt(10); // 'E' for east

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

            processCoords.push([latDecimal, lonDecimal]);
        }
    });

    return processCoords;

}

function updateNotamMapPoints(notamCoords){
    // remove the existing points
    map.removeLayer(notamLayer);
    
    // // create a new leaflet layer for the notam points
    // notamLayer = L.layerGroup().addTo(map);

    // // add the new points
    // notamCoords.forEach(function(coord) {
    //     // Split the coordinate string
    //     var point = coord.toString().split(",");
        
    //     // Create a circle marker for each point and add it to the map
    //     var circle = L.circle([parseFloat(point[0]), parseFloat(point[1])], {
    //         color: 'red',
    //         fillColor: '#f03',
    //         fillOpacity: 0.5,
    //         radius: 500
    //     }).addTo(notamLayer);
    // });

}