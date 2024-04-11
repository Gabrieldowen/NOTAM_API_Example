var filterOptionsTimeout; // Variable to store the timeout reference

function showFilterOptions() {
    clearTimeout(filterOptionsTimeout); // Clear any existing timeout
    var filterOptionsDiv = document.getElementById("filterOptions");
    filterOptionsDiv.style.display = "block";
}

function hideFilterOptions() {
    filterOptionsTimeout = setTimeout(function() {
        var filterOptionsDiv = document.getElementById("filterOptions");
        filterOptionsDiv.style.display = "none";
    }, 200); // Adjust the delay as needed
}

function applyFilters() {
    // Get the value of each checkbox
    var closedRunwaysChecked = document.getElementById("closed_runways").checked;
    var obstacleNotamsChecked = document.getElementById("obstacle_notams").checked;
    var highObstacleNotamsChecked = document.getElementById("high_obstacle_notams").checked;
    var lightingMarkingNotamsChecked = document.getElementById("lighting_marking_notams").checked;

    // Prepare a data object to send to the server
    var filters = {
        closedRunways: closedRunwaysChecked,
        obstacleNotams: obstacleNotamsChecked,
        highObstacleNotams: highObstacleNotamsChecked,
        lightingMarkingNotams: lightingMarkingNotamsChecked
    };

    // Convert the filters object to JSON string
    var filtersJson = JSON.stringify(filters);

    // Send an AJAX request to apply filters
    $.ajax({
        url: '/apply_filters',
        type: 'POST',
        contentType: 'application/json',
        data: filtersJson,
        success: function(response) {
            // Update the display with filtered NOTAMs
            updateNotamsList(response);
        },
        error: function(xhr, status, error) {
            // Handle errors
            console.error(error);
        }
    });
}

function updateNotamsList(notams) {
    var notamsContainer = document.getElementById('notamList');
    notamsContainer.innerHTML = ''; // Clear previous list
    
    // Add the title and total number of NOTAMs
    var title = document.createElement('h1');
    title.style.marginLeft = '-2px';
    title.textContent = 'NOTAM Information';
    notamsContainer.appendChild(title);

    var totalNotams = document.createElement('p');
    totalNotams.textContent = 'Total number of Notams fetched: ' + notams.length;
    notamsContainer.appendChild(totalNotams);

    // Create div element for accordion
    var accordion = document.createElement("div");
    accordion.classList.add("accordion");
    notamsContainer.appendChild(accordion);

    // Notam item number for each notam to have a different id
    let notamItemNumber = 1;
	
	// Populate the container with the filtered NOTAMs
    notams.forEach(function(notam) {
        var accordionItem = document.createElement('div');
        accordionItem.classList.add('accordion-item');

        var checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.classList.add('custom-checkbox');
        // Unique id for each notam
        checkbox.id = 'item' + notamItemNumber;
        accordionItem.appendChild(checkbox);

        var label = document.createElement('label');
        label.classList.add('accordion-header', 'custom-checkbox-label');
        // Unique id for each notam
        label.setAttribute('for', 'item' + notamItemNumber);
        label.textContent = 'Notam ID: ' + notam.id;
        label.style.backgroundColor = notam.color;
        accordionItem.appendChild(label);

        var accordionContent = document.createElement('div');
        accordionContent.classList.add('accordion-content');
        accordionItem.appendChild(accordionContent);

        var seriesParagraph = document.createElement('p');
        seriesParagraph.innerHTML = '<strong>Series: </strong>' + notam.series;
        accordionContent.appendChild(seriesParagraph);

        var numberParagraph = document.createElement('p');
        numberParagraph.innerHTML = '<strong>Number: </strong>' + notam.number;
        accordionContent.appendChild(numberParagraph);

        var typeParagraph = document.createElement('p');
        typeParagraph.innerHTML = '<strong>Type: </strong>' + notam.type;
        accordionContent.appendChild(typeParagraph);

        var issuedParagraph = document.createElement('p');
        issuedParagraph.innerHTML = '<strong>Issued: </strong>' + notam.issued;
        issuedParagraph.style.marginBottom = '5px'; // Apply margin-bottom style
        accordionContent.appendChild(issuedParagraph);

        accordion.appendChild(accordionItem);
        
        // Increment id number for next notam
        notamItemNumber++
    });
}


// Function to return to the form page.
function returnToForm() {
    window.location.href = "/";
}