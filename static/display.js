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