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
	
	// Populate the container with the filtered NOTAMs
    notams.forEach(function(notam) {
        var accordionItem = document.createElement('div');
        accordionItem.classList.add('accordion-item');

        var checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.classList.add('custom-checkbox');
        checkbox.id = 'item';
        accordionItem.appendChild(checkbox);

        var label = document.createElement('label');
        label.classList.add('accordion-header', 'custom-checkbox-label');
        label.setAttribute('for', 'item');
        label.textContent = 'Notam ID: ' + notam.id;
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
        issuedParagraph.style.marginBottom = '5px';
        accordionContent.appendChild(issuedParagraph);

        notamsContainer.appendChild(accordionItem);
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
        const afterElement = getDragAfterElement(sortableList, e.clientY);
        const currentElement = document.querySelector(".dragging");
        if (afterElement == null) {
            sortableList.appendChild(draggedItem);
        } else {
            sortableList.insertBefore(draggedItem, afterElement);
        }
    });

    const getDragAfterElement = (container, y) => {
        const draggableElements = [...container.querySelectorAll("li:not(.dragging)")];
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
