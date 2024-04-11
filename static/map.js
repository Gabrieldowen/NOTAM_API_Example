// the mapping 
// Check if Leaflet library is imported
// Creating map options
// the mapping 
// Check if Leaflet library is imported
// Creating map options

$(document).ready( function() {
    if (document.getElementById("map")) {
        loadMap();
    }
    else {
        alert("map not found!");
    }
});

function loadMap() {

      // alert("points:: >>" + typeof calledPoints + calledPoints)

    var map = L.map('map').setView([51.505, -0.09], 13);

    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    var myLayer = L.geoJSON().addTo(map);
    myLayer.addData(calledPoints.features[0]);    



}