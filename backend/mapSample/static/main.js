$(document).ready(function () {
    const map = L.map('map').setView([37.8, -96], 4);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

    $('#submit-button').click(function () {
        const formData = {
            institution: $('#institution').val(),
            city: $('#city').val(),
            state: $('#state').val(),
            topic: $('#topic').val(),
            hbcuOnly: $('#search-only-hbcu').is(':checked')
        };

        // Send data to Flask API for filtering
        $.ajax({
            url: '/search',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(formData),
            success: function (data) {
                // Clear previous map layers
                map.eachLayer(function (layer) {
                    if (!layer._url) map.removeLayer(layer);
                });

                // Plot new points based on the filtered data (example assumes latitude, longitude)
                data.forEach(item => {
                    const latlng = [item.latitude, item.longitude];
                    L.marker(latlng).addTo(map).bindPopup(item.description);
                });
            },
            error: function () {
                alert('Error retrieving data');
            }
        });
    });
});
