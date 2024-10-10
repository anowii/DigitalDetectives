$(document).ready(function () {
    var pollingActive = false;  // Polling is inactive initially
    var pollInterval = null;    // Poll interval holder

    // Function to start polling after the first internal message
    function startPolling() {
        if (!pollingActive) {
            pollingActive = true;  // Activate polling
            pollInterval = setInterval(function () {
                $.ajax({
                    type: 'GET',
                    url: '/get_messages',
                    success: function (data) {
                        // Clear the chat window
                        $('#chat-window').empty();

                        // Loop through the messages and format them for display
                        data.forEach(function (message) {
                            var userMessageElement = $('<div></div>').text("User: " + message.user);
                            var responseMessageElement = $('<div></div>').text("AI: " + message.response);

                            $('#chat-window').append(userMessageElement);
                            $('#chat-window').append(responseMessageElement);
                        });
                    },
                    error: function (error) {
                        console.error('Error fetching messages:', error);
                    }
                });
            }, 1000);  // Poll every 1 seconds
        }
    }

    // Send the message to the chat window and backend
    $('#send-btn').click(function () {
        var message = $('#text-input').val();

        if (message.trim() !== "") {
            var messageElement = $('<div></div>').text("User: " + message);
            $('#chat-window').append(messageElement);

            // Send the message to the backend
            $.ajax({
                type: 'POST',
                url: '/forward_message',
                data: JSON.stringify({ message: message }),
                contentType: 'application/json',
                success: function (response) {
                    console.log('Message forwarded to backend:', response);
                    
                    // Start polling after the first message is sent
                    startPolling();
                },
                error: function (error) {
                    console.error('Error forwarding message:', error);
                }
            });

            $('#text-input').val('');  // Clear input
        }
    });

    // Enable sending the message by pressing 'Enter'
    $('#text-input').keypress(function (e) {
        if (e.which === 13) {  // Enter key
            $('#send-btn').click();
        }
    });
});