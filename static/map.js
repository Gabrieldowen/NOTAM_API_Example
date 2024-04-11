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

    if (calledPoints.type === "FeatureCollection") {
        // alert("The GeoJSON data has the correct type: FeatureCollection");
    } else {
       alert("The GeoJSON data does not have the correct type: FeatureCollection");
    }
    
    var coordinatesLength = calledPoints.features.length;
    middlePoint = parseInt(coordinatesLength/2)
    var zoom  = 4
    // alert("coordinates" + calledPoints.features[0].geometry.coordinates)
    var map = L.map('map').setView([ calledPoints.features[middlePoint].geometry.coordinates[1],  calledPoints.features[middlePoint].geometry.coordinates[0]], zoom );

    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);


    // map the points that are called
    var myLayer = L.geoJSON().addTo(map);
    calledPoints.features.forEach(function(feature) {
        myLayer.addData(feature);
    });

    // point = notamCoords[0].toString().split(",")
    // alert(point[1] +", " + point[0])
    // var circle = L.circle([parseFloat(point[0]), parseFloat(point[1])], {
    //     color: 'red',
    //     fillColor: '#f03',
    //     fillOpacity: 0.5,
    //     radius: 500
    // }).addTo(map);

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