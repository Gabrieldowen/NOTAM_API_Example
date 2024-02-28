$(document).ready(function () {
  $('.datepicker').datepicker({
      format: 'mm-dd-yyyy',
      autoclose: true,
      todayHighlight: true,
  });
});

var destinationCounter = 2;

function addDestination() {
	var additionalDestinationsDiv = document.getElementById('additionalDestinations');

	// Create a new destination row if there are no rows or the last row is full
	if (!additionalDestinationsDiv.lastChild || additionalDestinationsDiv.lastChild.childElementCount === 2) {
		var destinationRow = document.createElement('div');
		destinationRow.classList.add('row');
        additionalDestinationsDiv.appendChild(destinationRow);
	}

	// Create Destination Location input
	var destinationLocationInput = document.createElement('div');
	destinationLocationInput.classList.add('col-md-6', 'mb-3');
	destinationLocationInput.innerHTML = '<label for="destinationLocation' + destinationCounter + '" class="form-label">Destination Location ' + destinationCounter + '</label>' +
	'<input type="text" class="form-control" id="destinationLocation' + destinationCounter + '" name="destinationLocation' + destinationCounter + '" oninput="updateAirportOptions(\'destinationLocation' + destinationCounter + '\', \'destinationLocationSelect' + destinationCounter + '\')" onclick="updateAirportOptions(\'destinationLocation' + destinationCounter + '\', \'destinationLocationSelect' + destinationCounter + '\')">' +
	'<select class="form-select mt-2" id="destinationLocationSelect' + destinationCounter + '" name="destinationLocation' + destinationCounter + '" style="display: none;" onclick="selectAirport(\'destinationLocation' + destinationCounter + '\', \'destinationLocationSelect' + destinationCounter + '\')"></select>';

	// Append the destination input to the last destination row
	additionalDestinationsDiv.lastChild.appendChild(destinationLocationInput);

	// Increment the destination counter for the next input
	destinationCounter++;
}

function updateAirportOptions(inputId, selectId) {
	var inputElement = document.getElementById(inputId);
	var selectElement = document.getElementById(selectId);
	// Convert input to uppercase for case-insensitive matching
	var userInput = inputElement.value.toUpperCase();

	// Clear existing options and add blank option
	selectElement.innerHTML = '';
	var blankOption = document.createElement('option');
	blankOption.value = '';
	blankOption.text = '';
	selectElement.add(blankOption);
		
	// Recursive function to traverse the nested structure
	function traverse(obj) {
		for (var key in obj) {
			if (obj.hasOwnProperty(key) && key !== 'name' && key !== 'country') {
				var node = obj[key];

				if (node.hasOwnProperty('airports')) {
					// If the node has 'airports', recursively traverse it
					traverse(node.airports);
				} else {
					// Check if the node matches user input
					if (node.iata.includes(userInput) || node.name.toUpperCase().includes(userInput)) {
						var option = document.createElement('option');
						option.value = node.iata;
						option.text = `${node.iata} - ${node.name}`;
						selectElement.add(option);
					}
				}
			}
		}
	}

	// Start the recursive traversal from the root
	traverse(airportIATA);

	// Show the dropdown only if the input field is clicked
	selectElement.style.display = inputElement === document.activeElement ? 'block' : 'none';
}

function selectAirport(inputId, selectId) {
	var inputElement = document.getElementById(inputId);
	var selectElement = document.getElementById(selectId);

	// Check if the selected index is 0 (blank option)
	if (selectElement.selectedIndex === 0) {
		// Prevent event propagation
		event.stopPropagation();
		return;
	}
		
	// Update input field with the selected option
	inputElement.value = selectElement.value;

	// Hide the dropdown
	selectElement.style.display = 'none';
}
	
// Initially hide all dropdown menus
document.addEventListener('DOMContentLoaded', function () {
    var allSelects = document.querySelectorAll('.form-select');
    allSelects.forEach(function (select) {
        if (select) { // Check if the element exists before accessing its style property
            select.style.display = 'none';
        }
    });
});

// Function to reset the body of the page and change it to loading.
function submitForm() {
  // Store the form data.
  const formData = new FormData(document.getElementById('dataForm'));

  // Remvoe all the text and input boxes
  document.getElementById('Title').remove();

  document.getElementById('effectiveStartDate').remove();
  document.querySelector('label[for="effectiveStartDate"]').remove();

  document.getElementById('effectiveEndDate').remove();
  document.querySelector('label[for="effectiveEndDate"]').remove();
      
  document.getElementById('locationRadius').remove();
  document.querySelector('label[for="locationRadius"]').remove();
      
  document.getElementById('sortOrder').remove();
  document.querySelector('label[for="sortOrder"]').remove();
      
  document.getElementById('sortBy').remove();
  document.querySelector('label[for="sortBy"]').remove();
      
  document.getElementById('startAirport').remove();
  document.querySelector('label[for="destAirport"]').remove();
      
  document.getElementById('destAirport').remove();
  document.querySelector('label[for="startAirport"]').remove();

  document.getElementById('submitButton').remove();
  document.getElementById('addButton').remove();

  // Remove all the additional destinations
  document.getElementById('additionalDestinations').remove();

  var hiddenElements = document.querySelectorAll('.hiddenObj');

  // Display loading text for the user.
  hiddenElements.forEach(function (element) {
      element.style.display = 'block';
  });

  // Call the server with the data provided.
  fetch(document.getElementById('dataForm').action, {
      method: 'POST',
      body: formData,
  })
  
  // Update the display page after the call to the server is done.
  .then(response => response.text())
  .then(data => {
      // Replace the entire body with the new content
      document.body.innerHTML = data;
  })
  // Error catching just in case
  .catch(error => console.error('Error:', error))
  .finally(() => {
      // Hide loading elements
      hiddenElements.forEach(function (element) {
          element.style.display = 'none';
      });
  });
  
}

// Function called to check if the airports are of the correct form.
function checkInputAirport(inputId, errorMsg) {
  const inputElement = document.getElementById(inputId);
  const errorMessage = document.getElementById(errorMsg);

  // Use the regular expression pattern ^[A-Z]{3}$ to match three uppercase letters
  const pattern = /^[A-Z]{3}$/;

  // Check if the entered string matches the pattern
  if (!pattern.test(inputElement.value)) {
      errorMessage.textContent = 'Invalid airport. Please enter a valid airport.';
      return false;
  } else if (inputElement.value !== ''){
      errorMessage.textContent = '';
      return true;
  }

}

// Function called when user submits information. Checks each inputted value.
function checkInputs(){
  const isValidStart = checkInputAirport('startAirport', 'error-message3');
  const isValidDest = checkInputAirport('destAirport', 'error-message4');

  let isValidDests = true;
  let isValidDestI = false;
  for (let i = 3; i <= destinationCounter; i++){
      isValidDestI = checkInputAirport('destinationLocation' + (i-1), 'error-message' + (i+2));
      if (!isValidDestI){
          isValidDests = false;
      }
  }

  if (isValidStart && isValidDest && isValidDests){
     submitForm();
  }
}
