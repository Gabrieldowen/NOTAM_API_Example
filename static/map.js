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
    
    var coordinatesLength = calledPoints.features[0].geometry.coordinates.length;
    middlePoint = parseInt(coordinatesLength/2)
    // alert("coordinates" + calledPoints.features[0].geometry.coordinates)
    var map = L.map('map').setView([ calledPoints.features[middlePoint].geometry.coordinates[1],  calledPoints.features[middlePoint].geometry.coordinates[0]], (coordinatesLength*10));

    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    var myLayer = L.geoJSON().addTo(map);
    calledPoints.features.forEach(function(feature) {
        myLayer.addData(feature);
    });



}