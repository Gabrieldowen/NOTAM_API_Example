
$(document).ready(function () {
  $('.datepicker').datepicker({
      format: 'mm-dd-yyyy',
      autoclose: true,
      todayHighlight: true,
  });
});

var destinationCounter = 2;

function addDestination() {

  let additionalDestinationsDiv = document.getElementById('additionalDestinations');

  // Create a new destination row
  let destinationRow = document.createElement('div');
  destinationRow.classList.add('row');
  destinationRow.id = 'row' + destinationCounter;

  let destinationInput = document.createElement('div');
  destinationInput.classList.add('col-md-6', 'mb-3', 'destination');
  destinationInput.innerHTML = '<label for="destAirport' + destinationCounter + '" class="form-label">Next Destination' + '</label>' +
    '<input type="text" class="form-control" name="destAirport' + destinationCounter + '" placeholder="Airport Code" autocomplete="off">';
  destinationInput.id = 'destAirport' + destinationCounter;
  
  // Checking to see if there is a button needed for deleting.
  if (destinationCounter >= 3){
    let lastDestButtonId = 'deleteButton' + (destinationCounter - 1);
    document.getElementById(lastDestButtonId).remove();
    lastDestButtonId.onclick = null;
  }
  
  let destinationDelete = document.createElement('button');
  destinationDelete.id = 'deleteButton' + destinationCounter;
  destinationDelete.className = 'delete';
  destinationDelete.type = 'button';
  destinationDelete.onclick = function() {
    deleteDestination(destinationRow.id);
  };

  destinationInput.insertAdjacentElement('beforeend', destinationDelete);
  
  destinationRow.appendChild(destinationInput);
  additionalDestinationsDiv.appendChild(destinationRow);

  // Create an error message child for the new destination.
  let destinationErrorMsg = document.createElement('span');
  destinationErrorMsg.id = 'error-message' + (destinationCounter + 3);

  // Get the last destination location input in the row
  let lastDestinationLocationInput = additionalDestinationsDiv.lastChild.lastElementChild;

  // Insert the error message span right after the last destination location input
  lastDestinationLocationInput.insertAdjacentElement('beforeend', destinationErrorMsg);

  // Increment the destination counter for the next input
  destinationCounter++;



}

// Function to delete additional destinations not needed anymore.
function deleteDestination(inputId){
  
  destinationCounter--;
  
  document.getElementById(inputId).remove();

  if (destinationCounter != 2){
    
    let destinationRow = document.getElementById('row' + (destinationCounter - 1));


    let lastDest = document.getElementById('destAirport' + (destinationCounter - 1));

    let destinationDelete = document.createElement('button');
    destinationDelete.id = 'deleteButton' + (destinationCounter - 1);
    destinationDelete.className = 'delete';
    destinationDelete.type = 'button';
    destinationDelete.onclick = function() {
      deleteDestination(destinationRow.id);
    };

    
    lastDest.insertAdjacentElement('beforeend', destinationDelete);
  }
  
}

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

// Function to check for a leap year month.
function getLastDayOfMonth(year, month){
  if (month === 1 && ((year % 4 === 0 && year % 100 !== 0) || (year % 400 === 0))) {
      // February in a leap year
      return 29;
  } else {
      // The rest of the months
      return new Date(year, month + 1, 0).getDate();
  }
}

// Function called to check if the dates are of the correct form.
function checkInputDate(input, errorMsg) {
  const dateInput = document.getElementById(input).value;
  const errorMessage = document.getElementById(errorMsg);
  const dateArray = dateInput.split('-');
  
  const month = parseInt(dateArray[0], 10);
  const day = parseInt(dateArray[1], 10);
  const year = parseInt(dateArray[2], 10);

  // Check if the entered date is valid
  if (
      month >= 1 && month <= 12 &&
      day >= 1 && day <= getLastDayOfMonth(year, month) &&
      year >= 2020 && year <= 2030
  ) {
      errorMessage.textContent = ''; // Clear any previous error message
      return true;
  } else {
      errorMessage.textContent = 'Invalid date. Please enter a valid date (MM-DD-YYYY).';
      return false;
  }
}

// Function to check the inputted radius for the NOTAMs, right now it is 0 to 100, accepting only integers.
function checkInputRadius(inputId, errorMsg){
  const inputElement = document.getElementById(inputId);
  const errorMessage = document.getElementById(errorMsg);

  // Get the entered value and convert it to an integer
  const inputValue = parseInt(inputElement.value, 10);

  // Check if the entered value is a valid integer within the specified range
  if (Number.isInteger(inputValue) && inputValue >= 0 && inputValue <= 100) {
      // Valid input
      errorMessage.textContent = ''; // Clear any previous error message
      return true;
  } else {
      errorMessage.textContent = 'Invalid radius. Please enter a valid radius between 0 and 100.';
      return false;
  }
}

// Function called when user submits information. Checks only inputted value airports.
function checkInputs(){

  //const isValidDate1 = checkInputDate('effectiveStartDate', 'error-message1');
  //const isValidDate2 = checkInputDate('effectiveEndDate', 'error-message2');

  const isValidStart = checkInputAirport('startAirport', 'error-message3');
  const isValidDest = checkInputAirport('destAirport', 'error-message4');

  //const isValidLocationRadius = checkInputRadius('locationRadius', 'error-messageR')

  let isValidDests = true;
  let isValidDestI = false;
  for (let i = 3; i <= destinationCounter; i++){
      isValidDestI = checkInputAirport('destAirport' + (i-1), 'error-message' + (i+2));
      if (!isValidDestI){
          isValidDests = false;
      }
  }

  if (isValidStart && isValidDest && isValidDests){
     submitForm();
  }
}



