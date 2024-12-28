$(document).ready(function() {
    $('#search-input').on('input', function() {
        var query = $(this).val();
        console.log(query);
        $.ajax({
            url: '/live_search/',  // This should match the URL configured in urls.py
            data: {
                'query': query
            },
            dataType: 'json',
            success: function(data) {
                if (data.results && Array.isArray(data.results)) {
                $('#results').empty();  
                
                data.results.forEach(function(item) {                    
                    const resultItem = $('<div class="result-item" style="cursor: pointer;">' +
                        '<span class="result-symbol">' + item.symbol + '</span>' + 
                        '<span class="result-name" style="padding-left: 50px;">' + item.name + '</span>' +
                      '</div>');
                    // Set the onclick event to redirect to the result view
                    resultItem.on('click', function() {
                        window.location.href = "{% url 'result' 'placeholder' %}".replace('placeholder', item.symbol);
                    });
        
                    $('#results').append(resultItem);

/*
                    $('#results').append(
                        '<div class="result-item" >' +
                            '<span class="result-symbol">' + item.symbol + '</span>' + 
                            '<span class="result-name" style="padding-left: 50px;">' + item.name + '</span>' +
                        '</div>'
                    );*/
                });
            } else {
                console.error("Expected an array in 'results', but got:", data);
            }
            },
            error: function(xhr, errmsg, err) {
                console.error("Error:", errmsg);  // Log any error to the console
            }
        });
    });
});
