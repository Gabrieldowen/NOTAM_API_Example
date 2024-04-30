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
    }, 200);
}

function applyFilters() {
    // Get the value of each checkbox
    var closedRunwaysChecked = document.getElementById("closed_runways").checked;
    var obstacleNotamsChecked = document.getElementById("obstacle_notams").checked;
    var highObstacleNotamsChecked = document.getElementById("high_obstacle_notams").checked;
    var lightingMarkingNotamsChecked = document.getElementById("lighting_marking_notams").checked;
    var cancelledNotamsChecked = document.getElementById("cancelled_notams").checked;
    var keywordToKeepChecked = document.getElementById("with_keyword").checked;
    var keywordToRemoveChecked = document.getElementById("filter_out_keyword").checked;
	
    // Get the keywords entered by the user
    var keywordToKeep = document.getElementById("keyword_to_keep").value;
    var keywordToRemove = document.getElementById("keyword_to_remove").value;

    // Get the order of NOTAM types from the sortable list
    var notamTypesOrder = [];
    var notamTypeItems = document.querySelectorAll("#notamBoxes li");
    notamTypeItems.forEach(function(item) {
        notamTypesOrder.push(item.textContent.trim());
    });

	// Prepare a data object to send to the server
    var filters = {
        closedRunways: closedRunwaysChecked,
        obstacleNotams: obstacleNotamsChecked,
        highObstacleNotams: highObstacleNotamsChecked,
        lightingMarkingNotams: lightingMarkingNotamsChecked,
        cancelledNotams : cancelledNotamsChecked,
        notamTypesOrder: notamTypesOrder,
        keywordToKeep: keywordToKeepChecked  ? keywordToKeep : null,
        keywordToRemove: keywordToRemoveChecked ? keywordToRemove : null
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

function applyRanking() {
	// Get the order of NOTAM types from the sortable list
    var notamTypesOrder = [];
    var notamTypeItems = document.querySelectorAll("#notamBoxes li");
    notamTypeItems.forEach(function(item) {
        notamTypesOrder.push(item.textContent.trim());
    });

	// Prepare a data object to send to the server
    var ranking = {
		notamTypesOrder: notamTypesOrder
    };

	// Convert the filters object to JSON string
    var ranksJson = JSON.stringify(ranking);

	// Send an AJAX request to apply filters
    $.ajax({
        url: '/apply_sorting',
        type: 'POST',
        contentType: 'application/json',
        data: ranksJson,
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
    
    // rebuild map 
    // clearNotams();
    // alert("cleared map");
    var notamCoords = processCoordinates(notams);

    // Create the new content for the replacement
    var newContent = document.createElement('div');
    newContent.className = 'm-2'; // Set the class attribute
    newContent.style.height = '300px'; // Set the height style
    newContent.style.width = '100%'; // Set the width style
    newContent.id = 'map'; // Set the id attribute

    // Replace the div with the new content
    var divToReplace = document.getElementById('map');
    divToReplace.replaceWith(newContent);

    loadMap(notamCoords);


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
    accordion.id = "accordionList";
    notamsContainer.appendChild(accordion);

    // Notam item number for each notam to have a different id
    var notamItemNumber = 1;
	
	// Populate the container with the filtered NOTAMs
    notams.forEach(function(notam) {
        var accordionItem = document.createElement('div');
        accordionItem.id = "accordion_" + notam.id;
        accordionItem.classList.add('accordion-item');

        var checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.classList.add('custom-checkbox');

        // Unique id for each notam
        checkbox.id = notam.id //'item' + notamItemNumber;
        accordionItem.appendChild(checkbox);

        var label = document.createElement('label');
        label.classList.add('accordion-header', 'custom-checkbox-label');
        // Unique id for each notam
        label.setAttribute('for', notam.id);

        label.style.backgroundColor = notam.color;

        // Add the icons for each type of notam.
        var icon;
        if (notam.color === '#ff7f7f') {
            icon = document.createElement('i');
            icon.classList.add('fas', 'fa-exclamation-triangle');
            icon.style.color = 'black';
        } else if (notam.color === '#bad4b7') {
            icon = document.createElement('i');
            icon.classList.add('fas', 'fa-check-square');
            icon.style.color = 'black';
        } else if (notam.color === '#ffd966') {
            icon = document.createElement('i');
            icon.classList.add('fas', 'fa-exclamation-circle');
            icon.style.color = 'black';
        }
        if (icon) {
            label.appendChild(icon);
        }
        label.appendChild(document.createTextNode(' Notam ID: ' + notam.id + " Type: " + notam.type));
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

        var coordinateParagraph = document.createElement('p');
        coordinateParagraph.innerHTML = '<strong>Coordinates: </strong>' + notam.coordinates;
        accordionContent.appendChild(coordinateParagraph);

        var typeParagraph = document.createElement('p');
        typeParagraph.innerHTML = '<strong>Type: </strong>' + notam.type;
        accordionContent.appendChild(typeParagraph);

        var classificationParagraph = document.createElement('p');
        classificationParagraph.innerHTML = '<strong>Classification: </strong>' + notam.classification;
        accordionContent.appendChild(classificationParagraph);

        var sectionParagraph = document.createElement('p');
        sectionParagraph.id = `sectionID${notam.id}`;
        accordionContent.appendChild(sectionParagraph);

        // Create button element for translation
        var translationButton = document.createElement('button');
        translationButton.classList.add('btn', 'custom-btn', 'btn-sm');
        translationButton.innerHTML = '<i class="fa-solid fa-robot"></i>';
        function handleTranslationButtonClick(itemNumber) {
            translationButton.addEventListener('click', function() {
                translateText(itemNumber);
            });
        }
        handleTranslationButtonClick(notam.id);
        sectionParagraph.appendChild(translationButton);

        var textParagraph = document.createElement('a');
        textParagraph.innerHTML = `<strong> Text: </strong><a id="textID${notam.id}">${notam.text}</a>`;
        sectionParagraph.appendChild(textParagraph);

        var translationParagraph = document.createElement('p');
        translationParagraph.id = `translation${notam.id}`;
        accordionContent.appendChild(translationParagraph);

        var startParagraph = document.createElement('p');
        startParagraph.innerHTML = '<strong>Start: </strong>' + notam.effectiveStart;
        accordionContent.appendChild(startParagraph);

        var endParagraph = document.createElement('p');
        endParagraph.innerHTML = '<strong>End: </strong>' + notam.effectiveEnd;
        endParagraph.style.marginBottom = '10px';
        accordionContent.appendChild(endParagraph);

        accordion.appendChild(accordionItem);

        // Increment id number for next notam
        notamItemNumber++
    });
}

var rankListTimeout; // Variable to store the timeout reference

function updateRankNumbers() {
    var listItems = document.querySelectorAll("#notamBoxes li");
    listItems.forEach(function(item, index) {
        var textContent = item.textContent.trim();
        var match = textContent.match(/^\d+\.\s(.+)/);
        if (match) {
            item.textContent = (index + 1) + ". " + match[1];
        } else {
            item.textContent = (index + 1) + ". " + textContent;
        }
    });
}

function showRankList() {
    clearTimeout(rankListTimeout); // Clear any existing timeout
    var rankButton = document.getElementById("rankButton");
    var rankListContainer = document.getElementById("sortableListContainer");
    var buttonRect = rankButton.getBoundingClientRect();

    rankListContainer.style.display = "block";
    rankListContainer.style.top = buttonRect.bottom + "px";
    rankListContainer.style.left = buttonRect.left + "px";
	updateRankNumbers();
    initializeDragAndDrop();
}

function hideRankList() {
    clearTimeout(rankListTimeout);
    rankListTimeout = setTimeout(function() {
        var rankListContainer = document.getElementById("sortableListContainer");
        rankListContainer.style.display = "none";
    }, 200);
}

function showListContainer() {
    clearTimeout(rankListTimeout);
}

function hideListContainer() {
    rankListTimeout = setTimeout(function() {
        var rankListContainer = document.getElementById("sortableListContainer");
        rankListContainer.style.display = "none";
    }, 200);
}

function initializeDragAndDrop() {
    const sortableList = document.getElementById("notamBoxes");
    let draggedItem = null;
	let lastY = 0;

    sortableList.addEventListener("dragstart", (e) => {
        draggedItem = e.target;
        e.target.classList.add("dragging");
        setTimeout(() => {
            e.target.style.display = "none";
        }, 0);
    });

    sortableList.addEventListener("dragend", (e) => {
        e.target.style.display = "";
        e.target.classList.remove("dragging");
        draggedItem = null;
        updateRankNumbers();
    });

    sortableList.addEventListener("dragover", (e) => {
        e.preventDefault();
        const y = e.clientY;

        if (y > lastY + 20 || y < lastY - 20) {
            lastY = y;
            const afterElement = getDragAfterElement(sortableList, y);
            const currentElement = document.querySelector(".dragging");
            if (afterElement == null) {
                sortableList.appendChild(draggedItem);
            } else {
                sortableList.insertBefore(draggedItem, afterElement);
            }
        }
    });

    const getDragAfterElement = (container, y) => {
        const draggableElements = Array.from(container.querySelectorAll("li:not(.dragging)"));
        return draggableElements.reduce(
            (closest, child) => {
                const box = child.getBoundingClientRect();
                const offset = y - box.top - box.height / 2;
                if (offset < 0 && offset > closest.offset) {
                    return {
                        offset: offset,
                        element: child,
                    };
                } else {
                    return closest;
                }
            },
            {
                offset: Number.NEGATIVE_INFINITY,
            }
        ).element;
    };
}

function showKeywordInputKeep() {
    var keywordInput = document.getElementById("keyword_to_keep");
    if (document.getElementById("with_keyword").checked) {
        keywordInput.style.display = "block";
    } else {
        keywordInput.style.display = "none";
		keywordInput.value = ""; // Clear the input field
    }
}

function showKeywordInputRemove() {
    var keywordInput = document.getElementById("keyword_to_remove");
	
	if (document.getElementById("filter_out_keyword").checked) {
        keywordInput.style.display = "block";
    } else {
        keywordInput.style.display = "none";
		keywordInput.value = ""; // Clear the input field
    }
}

// function to translate the text asynchronously. This way you do not need to refresh the page
function translateText(textID) {

  // get the text to be translated
  var text = $('#textID' + textID).text();

  // replace the previous translation if there was one with a loading animation
  document.getElementById("translation"+textID).innerHTML =  '<p id="translationID"'+ textID+'><div class="spinner-border spinner-border-sm" role="status"><span class="visually-hidden">Loading...</span></div></p>';

  // call the server to translate the text
  $.ajax({
      type: 'POST',
      url: '/translateText',
      data: {"text": text},
      success:  function(data) {
        // if successfully translated, replace the loading animation with the translated text
        document.getElementById("translation"+textID).innerHTML = '<p id="translationID"'+ textID+'><strong>Translation: </strong>' + data.text + '</p>';
      },
      error: function(data) {
        // if unsucessful, replace the loading animation with an error message
        document.getElementById("translation"+textID).innerHTML = '<p id="translationID"'+ textID+'><strong>Translation: </strong> There was an error... please try again</p>';
      }
  })

}


// Function to return to the form page.
function returnToForm() {
    window.location.href = "/";
}
