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

    // Create a new destination row
    var destinationRow = document.createElement('div');
    destinationRow.classList.add('row');

    // Create Destination Location input
    var destinationInput = document.createElement('div');
    destinationInput.classList.add('col-md-6', 'mb-3');
    destinationInput.innerHTML = '<label for="destinationLocation' + destinationCounter + '" class="form-label">Destination Location ' + destinationCounter + '</label>' +
    '<input type="text" class="form-control" id="destinationLocation' + destinationCounter + '" name="destinationLocation' + destinationCounter + '" oninput="updateAirportOptions(\'destinationLocation' + destinationCounter + '\', \'destinationLocationDropdown' + destinationCounter + '\')" onclick="updateAirportOptions(\'destinationLocation' + destinationCounter + '\', \'destinationLocationDropdown' + destinationCounter + '\')">' +
    '<div class="dropdown" id="destinationLocationDropdown' + destinationCounter + '"></div>';

    destinationRow.appendChild(destinationInput);
    additionalDestinationsDiv.appendChild(destinationRow);
	
    // Create an error message child for the new destination.
    var destinationErrorMsg = document.createElement('span');
    destinationErrorMsg.id = 'error-message' + (destinationCounter + 3);

    // Get the last destination location input in the row
    var lastDestinationLocationInput = additionalDestinationsDiv.lastChild.lastElementChild;

    // Insert the error message span right after the last destination location input
    lastDestinationLocationInput.insertAdjacentElement('beforeend', destinationErrorMsg);
	
    // Increment the destination counter for the next input
    destinationCounter++;
}

function updateAirportOptions(inputId, dropdownId) {
    var inputElement = document.getElementById(inputId);
    var dropdownElement = document.getElementById(dropdownId);

    // Convert input to uppercase for case-insensitive matching
    var userInput = inputElement.value.toUpperCase();

    // Clear existing options
    dropdownElement.innerHTML = '';

    // Recursive function to traverse the nested structure
    function traverse(obj) {
	var options = [];

	function addOption(node) {
		var option = document.createElement('div');
		option.className = 'dropdown-option';
		option.textContent = `${node.iata} - ${node.name}`;
		option.addEventListener('click', function() {
			inputElement.value = this.dataset.airportCode;
			dropdownElement.style.display = 'none';
		});
		option.dataset.airportCode = node.iata;
		options.push(option);
	}

	for (var key in obj) {
		if (obj.hasOwnProperty(key) && key !== 'name' && key !== 'country') {
			var node = obj[key];

			if (node.hasOwnProperty('airports')) {
				traverse(node.airports);
			} else {
				if (node.iata.includes(userInput) || node.name.toUpperCase().includes(userInput)) {
					addOption(node);
				}
			}
		}
	}

	// Sort the options alphabetically by airport name
	options.sort(function(a, b) {
		return a.textContent.localeCompare(b.textContent);
	});

	// Append sorted options to the dropdown
	options.forEach(function(option) {
		dropdownElement.appendChild(option);
	});
    }

    // Start the recursive traversal from the root
    traverse(airportIATA);

    // Show the dropdown
    dropdownElement.style.display = 'block';
}

// Closes the dropdown when clicking outside
document.addEventListener('click', function (event) {
    var dropdowns = document.querySelectorAll('.dropdown');

    dropdowns.forEach(function (dropdownElement) {
        if (!event.target.closest('.custom-dropdown')) {
            dropdownElement.style.display = 'none';
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
