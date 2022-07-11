// Google autocomplete function for travel search form
$( document ).ready(function() {
    // const google_api_key = document.getElementById('google_api_key');
    const google_api_key = JSON.parse(document.getElementById("google_api_key").textContent);
    $.getScript("https://maps.googleapis.com/maps/api/js?key=" + google_api_key + "&libraries=places")
    .done(function( script, textStatus ) {
        google.maps.event.addDomListener(window, 'click', initAutoComplete)
    })


    let autocomplete;
    var input = document.getElementById('destination_input');
    function initAutoComplete(){
    autocomplete = new google.maps.places.Autocomplete(
        input,
        {
            types: ['country', 'locality'],
        })
    input.addEventListener("change", function (){
        input.value = null;
    })
    
    }

    
});


   