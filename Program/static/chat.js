$(document).ready(function () {
    var pollingActive = false;  // Polling is inactive initially
    var pollInterval = null;    // Poll interval holder

    // Function to show loading indicator
    function showLoadingIndicator() {
        $('#loading-indicator').show();
    }

    // Function to hide loading indicator
    function hideLoadingIndicator() {
        $('#loading-indicator').hide();
    }

    // Function to start polling after the first internal message
    function startPolling() {
        if (!pollingActive) {
            pollingActive = true;  // Activate polling
            showLoadingIndicator(); // Show loading indicator when polling starts

            pollInterval = setInterval(function () {
                console.log('Sending AJAX request to /get_messages'); 
                $.ajax({
                    type: 'GET',
                    url: '/get_messages',
                    success: function (data) {    
                        console.log('Message fetched:', data); 
                        // Clear the chat window
                        $('#chat-window').empty();

                        // Loop through the messages and format them for display
                        var id = 0;
                        data.forEach(function (message) {
                            
                            message.user = message.user.replace(/\n/g, "<br/>")
                            message.response = message.response.replace(/\n/g, "<br/>")

                            var userMessageElement = $('<div class="message user-message"></div>').html("User: " + message.user);
                            var responseMessageElement = $('<div class="message ai-message"></div>').html('<span class="ai-label">AI: </span>' + message.response).attr('id', 'ai-message-' + id);
                            // Adds button if SQL-Agent response
                            
                            $('#chat-window').append(userMessageElement);
                            if ( message.user.toLowerCase().startsWith("list") && message.response.toLowerCase().startsWith("result generated from select")){
                                var context_btn = $('<button class="context-btn"></button>').attr('id', 'context-btn-' + id)
                                $('#chat-window').append(context_btn);
                            }
                    
                            $('#chat-window').append(responseMessageElement);
                            id++;
                        });

                        clearInterval(pollInterval); // Stop polling after receiving a response
                        pollingActive = false; // Reset polling state
                        hideLoadingIndicator(); // Hide loading indicator after receiving response

                    },
                    error: function (error) {
                        console.error('Error fetching messages:', error);
                        hideLoadingIndicator(); // Hide loading indicator on error
                    }
                });
            }, 1000);  // Poll every 1 second
        }
    }

    // Send the message to the chat window and backend
    $('#send-btn').click(function () {
        var message = $('#text-input').val();

        if (message.trim() !== "") {
            // Clear the input field
            $('#text-input').val('');

            var userMessageElement = $('<div class="message user-message"></div>').html("User: " + message);
            $('#chat-window').append(userMessageElement)

            // Show loading indicator when sending message
            showLoadingIndicator();

            // Send the message to the backend
            $.ajax({
                type: 'POST',
                url: '/forward_message',
                data: JSON.stringify({ message: message }),
                contentType: 'application/json',
                success: function (response) {
                    console.log('Message forwarded to backend:', response);

                    // Once the AI responds, start polling if not active
                    startPolling();
                },
                error: function (error) {
                    console.error('Error forwarding message:', error);
                    hideLoadingIndicator(); // Hide loading indicator on error
                }
            });
        }
    });

    // Enable sending the message by pressing 'Enter'
    $('#text-input').keypress(function (e) {
        if (e.which === 13) {  // Enter key
            $('#send-btn').click();
        }
    });
});