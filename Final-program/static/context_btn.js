document.addEventListener("DOMContentLoaded", function() {
    $('#chat-window').on('click', '.context-btn', function () {
        
        // Check if the clicked button is already active
        if ($(this).hasClass('active')) {
            // If it's active, deactivate it
            $(this).removeClass('active');
            fetch('/reset_json_data', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({})  // Send an empty body for reset
            })
            .then(response => response.json())
            .then(data => {
                console.log('Reset Query Data Success:', data);  // Handle success
            })
            .catch((error) => {
                console.error('Error:', error);  // Handle any errors
            });
        } else {
            // If it's not active, deactivate all buttons and activate the clicked one
            $('.context-btn').removeClass('active');
            $(this).addClass('active');


            // Fetch Query of message the button is attatched to
            var buttonId = $(this).attr('id').replace('context-btn-', '');
            var aiMessageElement = $('#ai-message-' + buttonId);
            var aiMessageText = aiMessageElement.text();
            var start = -1;

            start = aiMessageText.indexOf("SELECT")
            end = aiMessageText.indexOf(":name", start)
            var query = aiMessageText.slice(start, end)
            
            console.log('Button clicked:', $(this).attr('id'), query);
            if (start !== -1){
                fetch('/set_json_data', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ query: query })  // Send query to Flask
                })
                .then(response => response.json())
                .then(data => {
                    console.log('Set Query Data Success:', data);  // Handle success
                })
                .catch((error) => {
                    console.error('Error:', error);  // Handle any errors
                });
            }else{
                console.log('No Query found');
            }

        }
    });
});