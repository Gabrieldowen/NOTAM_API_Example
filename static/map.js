
// This file contains the functions to create the map and the points on the map
function loadMap(notamCoords) {
    
    // map settings
    var coordinatesLength = calledPoints.features.length;

    // save points and swap since they are in the wrong order
    var firstPoint = L.latLng([ calledPoints.features[0].geometry.coordinates[1],  calledPoints.features[0].geometry.coordinates[0]]);
    var lastPoint = L.latLng([ calledPoints.features[coordinatesLength-1].geometry.coordinates[1],  calledPoints.features[coordinatesLength-1].geometry.coordinates[0]]);
    

    // centers the map at the middle point of the called points
    var map = L.map('map').fitBounds(L.latLngBounds(lastPoint, firstPoint));

    // zoom out slightly
    map.zoomOut(1);


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
                radius: circleRadius * 1852 // nautical miles to meters
            }).addTo(map)

        // save each point to a array for the line
        line.push(point);
    
        
    });
    var x =0;


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
        }).addTo(notamLayer).on("click", function(e) {
            // popup for clicked point
            //clickedCircle.bindPopup("some content "+point[2]).openPopup();

            // get the item with the id of the notam id
            var itemID = "accordion_" + point[2];
            var item = document.getElementById(itemID);
            var accordianList = document.getElementById("accordionList");

            // error handling
            if (!item) {
                console.error("Element with ID " + itemID + " not found!");
                return;
            }
            if (!accordianList) {
                console.error("accordianList with ID " + "accordionList" + " not found!");
                return;
            }
            

            if (item && accordianList) {

                // Move the item to the top of its parent container
                accordianList.insertBefore(item, accordianList.firstChild);
                
                // simulate clicking the header to open the accordion
                item.getElementsByClassName("accordion-header")[0].click();
            } 

        });
    });
}



// this function parses the existing coordinates to a format that can be used by leaflet
function parseCoord(coordString, notamId) {

    // seperate the lat from the long
    var coords = coordString.split(/(?<=N|S)/);
    var latString = coords[0];
    var lonString = coords[1];

    // add leading zeros to the minutes if they are missing
    if(lonString.length == 7){
        lonString = '0' + lonString;
    }
    
    
    // Extract degrees and minutes for latitude
    var latDegrees = parseInt(latString.substring(0, 2), 10);
    var latMinutes = parseInt(latString.substring(2, 4), 10);

    // extract seconds if there are some
    if(latString.length > 6){
        var latSeconds = parseInt(latString.substring(4, 6), 10);
    } else {
        var latSeconds = 0;
    }

    var latDecimal = latDegrees + latMinutes / 60 + latSeconds / 3600;

    // Extract degrees and minutes for longitude
    var lonDegrees = parseInt(lonString.substring(0, 3), 10);
    var lonMinutes = parseInt(lonString.substring(3, 5), 10);

    // extract seconds if there are some
    if(lonString.length > 6){
        var lonSeconds = parseInt(lonString.substring(6, 7), 10);
    } else {
        lonSeconds = 0;
    }

    var lonDecimal = lonDegrees + lonMinutes / 60 + lonSeconds / 3600;

    // Determine direction for latitude and longitude
    var latDirection = latString.charAt(latString.length - 1); // 'N' for north
    var lonDirection = lonString.charAt(lonString.length - 1); // 'E' for east


    // Add the direction for latitude
    if (latDirection === 'S') {
        latDecimal = -latDecimal;
    }
     if (lonDirection === 'W') {
        lonDecimal = -lonDecimal;
    }
    var latDecimal = parseFloat(latDecimal);
    var lonDecimal = parseFloat(lonDecimal);

    if (isNaN(latDecimal) || isNaN(lonDecimal)) {
        console.log("Invalid coordinates: " + coordString);
        return [0, 0, notamId];
    }

    return [latDecimal, lonDecimal, notamId];
}

function processCoordinates(notams) {

    var processCoords = [];
    notams.forEach(function(notam) {
        if (notam.coordinates != undefined || notam.coordinates != null) {
            // // Extract degrees and minutes for latitude
            // var latDegrees = parseInt(notam.coordinates.substring(0, 2), 10);
            // var latMinutes = parseInt(notam.coordinates.substring(2, 4), 10);
            // var latDecimal = latDegrees + latMinutes / 60;

            // // Extract degrees and minutes for longitude
            // var lonDegrees = parseInt(notam.coordinates.substring(5, 8), 10);
            // var lonMinutes = parseInt(notam.coordinates.substring(8, 10), 10);
            // var lonDecimal = lonDegrees + lonMinutes / 60;

            // // Determine direction for latitude and longitude
            // var latDirection = notam.coordinates.charAt(4); // 'N' for north
            // var lonDirection = notam.coordinates.charAt(10); // 'E' for east

            // // Add the direction for latitude
            // if (latDirection === 'S') {
            //     latDecimal = -latDecimal;
            // }

            // // Add the direction for longitude
            // if (lonDirection === 'W') {
            //     lonDecimal = -lonDecimal;
            // }

            // var latDecimal = parseFloat(latDecimal);
            // var lonDecimal = parseFloat(lonDecimal);

            processCoords.push(parseCoord(notam.coordinates, notam.id));
        }
    });

    return processCoords;

}
