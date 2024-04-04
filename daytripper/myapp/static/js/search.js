$(function () {
    $("#id_query").autocomplete({
        source: autocompleteUrl,
        minLength: 1, // Minimum characters before autocomplete starts
    });

    $('#query-form').submit(function (event) {
        event.preventDefault();  // Prevent default form submission
        console.log("Form submitted");  // Log form submission
        $.ajax({
            type: 'POST',
            url: returnPlacesUrl,
            data: $(this).serialize(),  // Serialize the form data
            dataType: 'json',
            success: function (response) {
                console.log("Success:", response);  // Log successful response

                var placesHtml = ''; // Initialize an empty string to store HTML for places
                // Loop through each place in the response and create HTML for it
                $.each(response.places, function (index, place) {
                    var placeLink = '/myapp/selected_place/' + encodeURIComponent(place.id) + '/';
                    placesHtml += '<a href="' + placeLink + '">' + place.displayName.text + '<a><br>';
                });
                // Update the nearby_places div with the HTML for places
                $('#nearby_places').html(placesHtml);
            },
            error: function (xhr, status, error) {
                console.error("Error:", xhr.responseText);  // Log error response
            }
        });
    });
});