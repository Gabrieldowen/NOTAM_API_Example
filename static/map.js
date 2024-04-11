// the mapping 
// Check if Leaflet library is imported
// Creating map options
// the mapping 
// Check if Leaflet library is imported
// Creating map options

// document.addEventListener("DOMContentLoaded", function() {
//     if (document.getElementById("map")) {
//         loadMap();
//     }
//     else {
//         alert("map not found!");
//     }
// });

function loadMap() {

    var map = L.map('map').setView([51.505, -0.09], 13);

    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    L.marker([51.5, -0.09]).addTo(map)
        .bindPopup('A pretty CSS popup.<br> Easily customizable.')
        .openPopup();

}